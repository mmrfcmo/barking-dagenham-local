# Barking & Dagenham Local — Current State

## Repository status
- Repository: `mmrfcmo/barking-dagenham-local`
- Branch: `main`
- GitHub is the permanent source of truth.
- This continuity baseline was created after the previous development container was lost.

## Recovery status
The original Phase 1–3 source code is not currently present in this repository or the available workspace. The previous conversation documents that Phase 1–3 were built and tested in a temporary container, but that source was not committed to GitHub and therefore cannot be recovered from the current environment.

The conversation also documents that Phase 4A had begun in the lost workspace, including a Supabase/Postgres schema/client/repository direction, but that work is not available here.

Therefore this repository currently contains the durable specification/continuity layer, not the recovered application source.

## Previously established product functionality
The prior build was reported to include:
- public local directory
- locality/category SEO architecture
- business profiles
- Barking and Dagenham locality pages
- listing tiers: Free, Verified, Premium, Growth
- admin business management
- business editing UI
- CSV export
- 30-second business claim flow
- claim admin/approval flow
- claim lead capture concept
- canonical/sitemap/robots/noindex SEO controls

These are **specification/history**, not proof that the corresponding source code exists in the current repository. Rebuild and verify rather than assuming.

## Next implementation priority
1. Recreate the application foundation in GitHub.
2. Rebuild the proven Phase 1–3 functionality systematically.
3. Commit each completed phase.
4. Implement Phase 4A persistent Supabase/Postgres repository architecture.
5. Verify persistence across restart/deploy.
6. Continue with CRM, scanner, outreach, publishing and social capabilities in later phases.

## Infrastructure decisions
- GitHub: source control and continuity.
- Render: deployment/hosting.
- Supabase/Postgres: persistent database.
- External email/social/scanning providers: adapters with environment-based credentials.

## Important limitation
Do not claim that the application is currently deployed or that Phase 1–4A source has been recovered. The repository must be rebuilt and tested from this point unless code is subsequently restored into GitHub.
