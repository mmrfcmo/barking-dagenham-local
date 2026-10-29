# First business import — FSA batch

This import is intentionally a **staging step**, not automatic public publishing.

## What batch 001 contains
- Up to 300 records from the Food Standards Agency (FSA) register for Barking and Dagenham.
- Food premises only (for example restaurants, takeaways, cafés and food shops), not all business categories in the borough.
- Source URL, FSA ID and available hygiene-rating/date fields for traceability.
- Every row starts with `verification_status=unverified` and `listing_status=draft`. Do not mark an owner or listing as verified merely because it appears in an official register.

The FSA provides a free API and requires the `x-api-version: 2` header. See the [official API guidance](https://api.ratings.food.gov.uk/help) and [open-data page](https://ratings.food.gov.uk/open-data). The rating is a dated inspection result, not a general quality score.

## Run locally

Requires Python 3.10+ and internet access; no third-party Python packages are needed.

```bash
python scripts/import_fsa_barking_dagenham.py --limit 300
```

Optional output path:

```bash
python scripts/import_fsa_barking_dagenham.py --limit 300 --output /tmp/barking-fsa-batch.csv
```

Default output: `data/imports/barking-dagenham-fsa-batch-001.csv`.

## Review before loading into Supabase
1. Check the count and sample records; remove closed, duplicated or unsuitable entries.
2. Confirm the local authority ID and that addresses are inside the borough.
3. Match the category names against the categories actually present in the database.
4. Import into Supabase as draft/unverified records using a server-side/admin process.
5. Do not expose private contact data or invent missing phone numbers, websites or emails.
6. Keep source attribution and refresh dates. Follow the FSA API terms, including its requirements for displaying rating information and imagery.

This script does not write to Supabase because no database connection has been configured in the repository. It also does not publish any records to the public directory.
