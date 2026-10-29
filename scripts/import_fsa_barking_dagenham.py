#!/usr/bin/env python3
"""Stage a first Barking & Dagenham business batch from the official FSA API.

This deliberately writes a review CSV rather than publishing records directly.
FSA records cover food-related premises only; they are not the full business
population. No credentials or third-party scraping are required.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_URL = "https://api.ratings.food.gov.uk/Establishments"
SOURCE_NAME = "Food Standards Agency FHRS API"
BOROUGH = "Barking and Dagenham"
PAGE_SIZE = 500
FIELDS = [
    "name", "slug", "summary", "description", "address_line_1",
    "address_line_2", "locality", "postcode", "borough", "phone",
    "public_email", "website_url", "source_name", "source_url",
    "source_checked_at", "verification_status", "listing_status",
    "category", "fhrs_id", "food_hygiene_rating", "food_hygiene_rating_date",
]


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "business"


def category_for(record: dict) -> str:
    business_type = clean(record.get("BusinessType")).lower()
    name = clean(record.get("BusinessName")).lower()
    if "restaurant" in business_type or "takeaway" in business_type or "cafe" in business_type:
        return "Food & Drink"
    if "retail" in business_type or "supermarket" in business_type or "convenience" in business_type:
        return "Shops & Retail"
    if "hotel" in business_type or "pub" in business_type:
        return "Food & Drink"
    if any(word in name for word in ("restaurant", "cafe", "café", "takeaway", "grill", "pizza", "kebab", "chicken")):
        return "Food & Drink"
    if "caring" in business_type or "childcare" in business_type:
        return "Health, Care & Childcare"
    return "Food & Drink"


def request_page(local_authority_id: int, page: int) -> dict:
    query = urllib.parse.urlencode({
        "localAuthorityId": local_authority_id,
        "pageSize": PAGE_SIZE,
        "pageNumber": page,
    })
    req = urllib.request.Request(
        f"{API_URL}?{query}",
        headers={
            "x-api-version": "2",
            "Accept": "application/json",
            "User-Agent": "BarkingLocalDirectoryImporter/1.0 (open-data import)",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def normalise(record: dict, checked_at: str) -> dict:
    name = clean(record.get("BusinessName"))
    address1 = clean(record.get("AddressLine1"))
    address2 = clean(record.get("AddressLine2"))
    address3 = clean(record.get("AddressLine3"))
    address4 = clean(record.get("AddressLine4"))
    postcode = clean(record.get("PostCode")).upper()
    locality = next((v for v in (address4, address3, address2) if v), BOROUGH)
    fhrs_id = clean(record.get("FHRSID"))
    rating = clean(record.get("RatingValue"))
    rating_date = clean(record.get("RatingDate"))
    source_url = f"https://ratings.food.gov.uk/business/{fhrs_id}" if fhrs_id else "https://ratings.food.gov.uk/"
    return {
        "name": name,
        "slug": f"{slugify(name)}-{fhrs_id}" if fhrs_id else slugify(name),
        "summary": "",
        "description": "",
        "address_line_1": address1,
        "address_line_2": address2,
        "locality": locality,
        "postcode": postcode,
        "borough": BOROUGH,
        "phone": "",
        "public_email": "",
        "website_url": "",
        "source_name": SOURCE_NAME,
        "source_url": source_url,
        "source_checked_at": checked_at,
        "verification_status": "unverified",
        "listing_status": "draft",
        "category": category_for(record),
        "fhrs_id": fhrs_id,
        "food_hygiene_rating": rating,
        "food_hygiene_rating_date": rating_date,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=300, help="Maximum rows to stage (default: 300)")
    parser.add_argument("--local-authority-id", type=int, default=501, help="FSA authority ID for Barking and Dagenham (official authority page: ratings.food.gov.uk/authority-search-landing/501)")
    parser.add_argument("--output", default="data/imports/barking-dagenham-fsa-batch-001.csv")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be at least 1")

    checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    rows: list[dict] = []
    page = 1
    seen: set[str] = set()
    try:
        while len(rows) < args.limit:
            payload = request_page(args.local_authority_id, page)
            establishments = payload.get("establishments") or payload.get("Establishments") or []
            if not establishments:
                break
            for record in establishments:
                row = normalise(record, checked_at)
                key = row["fhrs_id"] or (row["name"].casefold(), row["postcode"].casefold())
                if not row["name"] or key in seen:
                    continue
                seen.add(key)
                rows.append(row)
                if len(rows) >= args.limit:
                    break
            meta = payload.get("meta") or {}
            total_pages = int(meta.get("totalPages") or meta.get("TotalPages") or page)
            if page >= total_pages:
                break
            page += 1
            time.sleep(0.2)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError) as exc:
        print(f"Import stopped before completion: {exc}", file=sys.stderr)
        return 1

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Staged {len(rows)} records to {output}")
    print("All records remain draft/unverified; review before any public publishing.")
    if len(rows) < args.limit:
        print(f"Note: API returned {len(rows)} unique records, fewer than the requested {args.limit}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
