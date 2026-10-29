#!/usr/bin/env python3
"""Stage a reviewable OpenStreetMap business batch for Barking & Dagenham.

OpenStreetMap data is ODbL licensed. This script preserves OSM object IDs and
attribution and writes a CSV only; it never publishes listings or writes DB rows.
OSM tags are mapped to the closest Google Places type identifier for directory
navigation, not represented as Google's own classification of that business.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
SOURCE_NAME = "OpenStreetMap contributors (ODbL)"
SOURCE_URL = "https://www.openstreetmap.org/copyright"
FIELDS = [
    "name", "slug", "category_google_type", "category_source", "address_line_1",
    "address_line_2", "locality", "postcode", "borough", "phone", "website_url",
    "source_name", "source_url", "source_checked_at", "source_object_id",
    "verification_status", "listing_status", "latitude", "longitude",
]

# Best-effort translation from OSM tagging to our Google-type-aligned taxonomy.
# It is a directory mapping, not a claim that Google classified the record.
TAG_MAP = {
    ("amenity", "dentist"): "dentist",
    ("amenity", "doctors"): "doctor",
    ("amenity", "pharmacy"): "pharmacy",
    ("amenity", "veterinary"): "veterinary_care",
    ("amenity", "restaurant"): "restaurant",
    ("amenity", "cafe"): "cafe",
    ("amenity", "fast_food"): "fast_food_restaurant",
    ("amenity", "pub"): "bar",
    ("amenity", "bank"): "bank",
    ("amenity", "school"): "school",
    ("amenity", "childcare"): "child_care_agency",
    ("shop", "hairdresser"): "hair_salon",
    ("shop", "beauty"): "beauty_salon",
    ("shop", "chemist"): "pharmacy",
    ("shop", "florist"): "florist",
    ("shop", "supermarket"): "supermarket",
    ("shop", "convenience"): "convenience_store",
    ("shop", "clothes"): "clothing_store",
    ("shop", "hardware"): "hardware_store",
    ("shop", "car_repair"): "car_repair",
    ("shop", "car"): "car_dealer",
    ("shop", "pet"): "pet_store",
    ("shop", "bakery"): "bakery",
    ("shop", "butcher"): "butcher_shop",
    ("shop", "books"): "book_store",
    ("shop", "florist"): "florist",
    ("craft", "roofer"): "roofing_contractor",
    ("craft", "plumber"): "plumber",
    ("craft", "electrician"): "electrician",
    ("craft", "painter"): "painter",
    ("craft", "locksmith"): "locksmith",
    ("office", "lawyer"): "lawyer",
    ("office", "accountant"): "accounting",
    ("office", "estate_agent"): "real_estate_agency",
    ("office", "insurance"): "insurance_agency",
    ("office", "company"): "corporate_office",
    ("leisure", "fitness_centre"): "fitness_center",
    ("tourism", "hotel"): "hotel",
    ("tourism", "guest_house"): "guest_house",
}

def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()

def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "business"

def category_for(tags: dict) -> str:
    for key in ("amenity", "shop", "craft", "office", "leisure", "tourism"):
        value = clean(tags.get(key)).lower()
        if (key, value) in TAG_MAP:
            return TAG_MAP[(key, value)]
    return "business"

def overpass_query() -> str:
    return """
[out:json][timeout:90];
area["name"="London Borough of Barking and Dagenham"]["boundary"="administrative"]->.searchArea;
(
  nwr["name"]["shop"](area.searchArea);
  nwr["name"]["amenity"](area.searchArea);
  nwr["name"]["craft"](area.searchArea);
  nwr["name"]["office"](area.searchArea);
  nwr["name"]["leisure"="fitness_centre"](area.searchArea);
  nwr["name"]["tourism"~"hotel|guest_house"](area.searchArea);
);
out center tags;
"""

def fetch_data() -> dict:
    body = urllib.parse.urlencode({"data": overpass_query()}).encode()
    request = urllib.request.Request(
        OVERPASS_URL, data=body, method="POST",
        headers={"User-Agent": "BarkingLocalDirectory/1.0 (ODbL attributed import)", "Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))

def normalise(element: dict, checked_at: str) -> dict | None:
    tags = element.get("tags") or {}
    name = clean(tags.get("name"))
    if not name:
        return None
    center = element.get("center") or element
    obj_type = clean(element.get("type"))
    obj_id = clean(element.get("id"))
    if not obj_id or not obj_type:
        return None
    address1 = clean(tags.get("addr:housenumber"))
    street = clean(tags.get("addr:street"))
    line1 = " ".join(part for part in (address1, street) if part)
    postcode = clean(tags.get("addr:postcode")).upper()
    locality = clean(tags.get("addr:suburb") or tags.get("addr:city") or tags.get("addr:town"))
    phone = clean(tags.get("contact:phone") or tags.get("phone"))
    website = clean(tags.get("contact:website") or tags.get("website"))
    return {
        "name": name,
        "slug": f"{slugify(name)}-osm-{obj_type}-{obj_id}",
        "category_google_type": category_for(tags),
        "category_source": "OSM tag mapping (not Google-verified)",
        "address_line_1": line1,
        "address_line_2": "",
        "locality": locality,
        "postcode": postcode,
        "borough": "Barking and Dagenham",
        "phone": phone,
        "website_url": website,
        "source_name": SOURCE_NAME,
        "source_url": f"https://www.openstreetmap.org/{obj_type}/{obj_id}",
        "source_checked_at": checked_at,
        "source_object_id": f"{obj_type}/{obj_id}",
        "verification_status": "unverified",
        "listing_status": "draft",
        "latitude": center.get("lat", ""),
        "longitude": center.get("lon", ""),
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=300, help="Maximum records to stage (default: 300)")
    parser.add_argument("--output", default="data/imports/barking-dagenham-osm-batch-001.csv")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be at least 1")
    checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    try:
        payload = fetch_data()
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"OpenStreetMap query failed: {exc}", file=sys.stderr)
        return 1
    rows, seen = [], set()
    for element in payload.get("elements", []):
        row = normalise(element, checked_at)
        if not row:
            continue
        key = row["source_object_id"]
        if key in seen:
            continue
        seen.add(key)
        rows.append(row)
        if len(rows) >= args.limit:
            break
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Staged {len(rows)} OSM records to {output}")
    print("All records are draft/unverified. Attribute OpenStreetMap contributors when displaying OSM-derived data.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
