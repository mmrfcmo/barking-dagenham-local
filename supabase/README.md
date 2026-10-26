# Supabase setup — Barking Local directory

This folder is a reviewed starting point, not a live database connection yet.

## What the schema does
- Creates business categories, businesses, and business/category links.
- Tracks source and last-checked date for evidence-led verification.
- Enables Row Level Security (RLS).
- Lets public visitors read only active categories used by verified, published listings and those verified, published business records.
- Deliberately disables direct public writes. Listing submissions and claims should be handled by a server-side Edge Function with validation and anti-spam protection.

## Before applying
1. Create a Supabase project for Barking Local when ready.
2. Open **SQL Editor** in the project dashboard.
3. Review `schema.sql`, then run it in the new project.
4. Add categories and listings only from sources that can be recorded and checked. Set `verification_status = 'verified'` only after checking the business and recording `source_checked_at`.
5. Keep the service-role key server-side only. Never put it in `index.html` or `directory.html`.

## Current state
- `directory.html` is a front-end design preview with working client-side search/filter controls over clearly labelled fictional sample cards.
- It is not connected to Supabase and does not store submissions.
- The existing homepage remains unchanged.
- Before using real listings, implement server-side data access, import validation, duplicate handling, and a moderation/claim workflow.
