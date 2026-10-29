# Barking & Dagenham Local — Changelog

## 2026-10-29 — First business import preparation
- Added a repeatable staging importer for the official Food Standards Agency API.
- Batch 001 defaults to 300 food-premises records for Barking and Dagenham.
- Records retain source IDs/URLs and hygiene rating dates, and remain draft/unverified pending review.
- The importer exports CSV only; it does not write to Supabase or publish listings.

## 2026-10-03 — Continuity baseline

### Added
- `AGENT_INSTRUCTIONS.md` — permanent development/recovery protocol.
- `MASTER_SPEC.md` — consolidated product requirements and future roadmap.
- `ARCHITECTURE.md` — target technical architecture and service boundaries.
- `CURRENT_STATE.md` — explicit recovery status and known limitations.
- `CHANGELOG.md` — durable project history.

### Repository policy
GitHub is now the permanent source of truth. Future development phases must be tested, documented and committed before being considered complete.

### Recovery note
The previous application source was created in a temporary environment and was not committed to GitHub. That environment is no longer available. The documented functionality and architecture have therefore been captured here as a rebuild specification rather than represented as recovered source code.

### Next
Rebuild the application foundation and previously validated directory functionality, committing each completed phase to GitHub before proceeding.
