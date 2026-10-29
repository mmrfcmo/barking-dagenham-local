# Barking & Dagenham Local — Current State

## Repository status
- Repository: `mmrfcmo/barking-dagenham-local`
- Working import branch: `feature/first-business-import-fsa`
- GitHub is the permanent source of truth.

## First import batch — validation status
- Importer: `scripts/import_fsa_barking_dagenham.py`
- Default target: up to 300 FSA food-premises records.
- The default FSA authority ID has been corrected to `501`, matching the official [Barking and Dagenham authority page](https://ratings.food.gov.uk/authority-search-landing/501).
- Unit tests have been added at `tests/test_import_fsa_barking_dagenham.py` for normalisation, source fields, draft/unverified status and CSV output.
- Source review confirms the FSA publishes food hygiene data for this borough; the official open-data page listed 1,469 premises in its latest update observed during this review.
- **Live batch not yet downloaded or validated row-by-row:** the execution environment used for this review could not resolve the FSA API host. Do not describe the first 300 records as imported or validated yet.
- No records have been written to Supabase or published to the directory.

## Remaining work
1. Run the unit tests in a Python environment.
2. Run the importer with network access and inspect the generated CSV for row count, duplicates, missing names/postcodes, category distribution and borough scope.
3. Confirm category names against the actual database taxonomy.
4. Configure Supabase securely and load approved records as drafts.
5. Build additional importers for non-food businesses (for example, OpenStreetMap under its applicable attribution/licence).

## Important limitation
The FSA batch covers food-related premises only; it is not the full borough business directory. A hygiene rating is an inspection result from a particular date, not a general business-quality score.
