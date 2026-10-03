# Barking & Dagenham Local — Agent Instructions

## Source of truth
GitHub is the permanent source of truth for this project. Conversation history is supporting context only. Never assume code exists because it was discussed previously; inspect the repository first.

Repository: `mmrfcmo/barking-dagenham-local`
Default branch: `main`

## Mandatory workflow
Before every build phase:
1. Read `AGENT_INSTRUCTIONS.md`, `MASTER_SPEC.md`, `ARCHITECTURE.md`, `CURRENT_STATE.md`, and `CHANGELOG.md`.
2. Inspect the existing repository and preserve working functionality.
3. Identify the exact scope of the requested phase.
4. Do not rebuild or overwrite existing functionality without inspection.

For every completed phase:
1. Implement in small, testable increments.
2. Run the production build and relevant route/feature QA.
3. Update `CURRENT_STATE.md`.
4. Update `CHANGELOG.md`.
5. Commit all completed work to GitHub.
6. Report the commit SHA and what remains outstanding.

Never leave a completed phase only in a temporary workspace.

## Data and infrastructure rules
- Persistent application data must use the agreed database architecture; do not rely on in-memory state for production functionality.
- GitHub stores source code and project continuity documents.
- Render is deployment/hosting, not source control.
- Supabase/Postgres is the intended persistent data layer.
- Never put passwords, API keys, access tokens, or secrets into source files, commits, documentation, or chat.
- Use environment variables and `.env.example` for configuration templates.

## Product principles
- Build the fastest practical workflow for the directory owner and local businesses.
- Prefer automation and pre-population over asking businesses to re-enter information.
- Keep claim flows simple and mobile-first.
- Public directory pages should be useful to residents and commercially useful to businesses.
- SEO is a core acquisition channel, but avoid thin/duplicate pages and uncontrolled indexation.
- The site should feel like a local media/community channel, not merely a static business directory.
- AI may assist internal research, content generation, enrichment and publishing, but do not make unsupported claims about AI recommendations or guaranteed rankings.

## Change discipline
Do not add major features merely because they are technically possible. Maintain the phase boundaries in `MASTER_SPEC.md`. If a requested change materially alters architecture, update the architecture document before implementation.
