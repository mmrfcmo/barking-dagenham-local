# Google-type-aligned local business import

## Category strategy
The directory uses Google Places API (New) Table A identifiers as its canonical category vocabulary (for example `dentist`, `roofing_contractor`, `plumber`, `restaurant`, `beauty_salon`). Reference: https://developers.google.com/maps/documentation/places/web-service/place-types

This does **not** mean we bulk-copy Google Maps listings. Google Places policies restrict prefetching/caching/storing most Places API content; place IDs are a stated exception. Reference: https://developers.google.com/maps/documentation/places/web-service/policies

## First alternative-source pilot
`scripts/import_osm_barking_dagenham.py` stages up to 300 named business/place records from OpenStreetMap for the borough into a review CSV. OSM tags are mapped to the closest matching Google type identifier where possible; the category source is explicitly labelled as an OSM mapping, not a Google classification.

OpenStreetMap is ODbL licensed and requires attribution. If using or distributing a derived database, review the ODbL obligations and attribution requirements: https://www.openstreetmap.org/copyright

Run locally with Python 3.10+:

```bash
python scripts/import_osm_barking_dagenham.py --limit 300
```

Default output: `data/imports/barking-dagenham-osm-batch-001.csv`.

## Validation before publication
- Inspect record count and category distribution.
- Deduplicate by OSM object ID and then review likely same-business duplicates across objects.
- Check names, borough boundary, addresses and postcodes.
- Keep all records as draft/unverified until reviewed.
- Do not assume every mapped record is open or trading; OSM coverage is incomplete.
- Keep source attribution and source URL. Do not publish a Google-derived claim or rating unless lawfully sourced.
- This script stages CSV only. It does not write to Supabase or publish to the website.
