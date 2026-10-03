# Barking & Dagenham Local — Architecture

## Current target architecture

```text
                    GitHub
                      |
               Source of truth
                      |
              Next.js application
                 /           \
          Public web       Admin/CRM
             |                 |
        SEO/content       Prospecting/audits
             \                 /
              Repository layer
                      |
                Supabase/Postgres
                      |
       ---------------------------------
       |               |               |
   Businesses       Claims          Content
       |               |               |
   Listings        Contacts       Publishing
   Tiers           Outreach       Sources

External services are connected through explicit adapters:
- email provider
- website scanning/data providers
- social platform APIs
- approved RSS/XML/event sources
- Render for deployment
```

## Application layers

### Presentation
Next.js App Router pages/components for public directory, business profiles, locality/category pages, claim flow, admin and future CRM/media interfaces.

### Domain/data
Typed business, listing, claim, contact, campaign, audit and content models. Keep business rules out of individual UI components where practical.

### Repository layer
All persistent reads/writes go through repositories. This prevents UI pages from becoming coupled to Supabase/Postgres implementation details.

### Database
Supabase/Postgres is the intended production persistence layer. Database migrations must be versioned in the repository.

### Automation/services
Use service modules/adapters for scanner jobs, email campaigns, publishing, social distribution and scheduled processing. External credentials belong in environment variables/secrets.

## Key entities
At minimum the architecture needs to support:
- Business
- BusinessCategory
- Locality
- ListingTier
- Claim
- Contact/Owner
- Prospect/Lead
- Activity/Call/Note
- WebsiteAudit
- Campaign
- OutreachEvent
- ContentItem
- ContentSource
- SocialConnection
- PublishingJob

Exact schema should be normalised only as far as useful; avoid premature complexity.

## Claim architecture
Public business profile -> `/claim/[slug]` -> submit handler -> persistent claim record -> admin review -> business verification/listing state -> success/lead-magnet flow.

Claim links must not expose secrets beyond a suitably random/unguessable identifier if tokenised links are introduced.

## CRM architecture
The CRM should not be a separate disconnected application. It should share the business/contact/audit data layer with the directory. A prospect can become a claimed business and later a paying customer without duplicating records.

Suggested lifecycle:

`Discovered -> Enriched -> Scanned -> Contacted -> Follow-up -> Claimed -> Qualified -> Customer -> Retention`

This is configurable and should not be hard-coded as an irreversible state machine.

## Scanner architecture
Recommended pipeline:

`Target selection -> Fetch/crawl -> Crawl diagnostics -> Validity classification -> Signal/issue extraction -> Scoring -> Recommendations -> Report -> CRM attachment`

The scanner must distinguish technical failure from genuine negative findings. Invalid/limited scans must not be presented as reliable audits.

## Publishing architecture
Recommended pipeline:

`Source discovery -> Candidate -> Draft -> QA -> Approval rule -> Publish -> Distribution -> Analytics`

Support both human approval and configured automatic publishing, but default to safe approval rules until quality is validated.

## Social architecture
Use OAuth and platform APIs where supported. Store connection metadata and encrypted/provider-managed credentials appropriately. Never store raw access tokens in normal business records or logs.

## Deployment
Render hosts the application. GitHub remains the source repository. Database is external persistent infrastructure. Production secrets are configured in Render/Supabase rather than committed.

## Recovery principle
A fresh agent must be able to reconstruct the intended architecture by reading this document plus `MASTER_SPEC.md` and `CURRENT_STATE.md` without relying on the old conversation.
