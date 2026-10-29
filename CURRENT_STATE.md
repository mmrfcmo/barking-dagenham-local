# Barking & Dagenham Local — Current State

## Repository status
- Repository: `mmrfcmo/barking-dagenham-local`
- Working import branch: `feature/first-business-import-fsa`
- GitHub is the permanent source of truth.

## First import batch
- A staging script is available at `scripts/import_fsa_barking_dagenham.py`.
- It requests up to 300 premises from the Food Standards Agency API for Barking and Dagenham and exports a review CSV.
- Rows preserve FSA identifiers, source URLs and available hygiene-rating dates.
- Imported rows are deliberately marked `unverified` and `draft`.
- The script does not write to Supabase or publish public listings.
- The CSV is generated when the script is run with network access; no populated CSV is committed as if it had been downloaded or validated.

## Remaining work
1. Run the importer in a network-enabled environment and inspect the first 300 records.
2. Validate the local authority ID and borough boundaries; review duplicates and missing addresses.
3. Align category names with the live database taxonomy.
4. Configure Supabase securely and load approved records as drafts.
5. Build additional data-source importers for non-food businesses (for example, OpenStreetMap under its applicable attribution/licence) to broaden the directory.

## Important limitation
The FSA batch covers food-related premises only; it is not the full borough business directory. No claim is made that records have been imported into Supabase or are live on the public website.
