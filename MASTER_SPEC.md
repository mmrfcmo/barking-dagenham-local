# Barking & Dagenham Local — Master Specification

## 1. Product vision
Barking & Dagenham Local is a local directory and media platform for Barking & Dagenham. It combines searchable local business listings, locality/category landing pages, business claiming, commercial listing tiers, local editorial content, prospecting/CRM, website auditing, and automated publishing.

The long-term objective is to create a useful local media channel that can monetise business relationships while remaining valuable to residents.

## 2. Public directory
Core public routes/architecture include:
- `/`
- `/businesses`
- `/business/[slug]`
- `/barking`
- `/dagenham`
- `/businesses/[category]`
- `/barking/[category]`
- `/dagenham/[category]`

Locality/category pages should only be indexed when there is sufficient useful inventory, using the agreed indexation threshold rather than generating large numbers of thin pages.

## 3. Business listings
Businesses have structured information including identity, category, locality, address, postcode, phone, website, opening hours, description, claim state and listing status/tier.

Commercial listing tiers established in Phase 3:
- Free
- Verified
- Premium
- Growth

Tier configuration and pricing should remain centrally managed rather than hard-coded across components.

Admin functionality should support:
- search
- filtering
- viewing business records
- editing business records
- changing listing tiers/status
- claim management
- CSV export
- future import/bulk operations

## 4. Claim experience
The claim journey is intentionally designed to take roughly 30 seconds:
1. Owner receives a unique `/claim/[slug]` link.
2. Page is mobile-first and pre-populated with existing listing information.
3. Owner can confirm with a one-tap primary action.
4. A secondary correction path allows edits where information is wrong.
5. Claim captures useful lead information, including owner first name, last name, email/company email and mobile number where appropriate.
6. Successful claim leads to a confirmation/success page.
7. The success page can introduce a relevant lead magnet such as a free website growth/audit check.
8. Admin can review and approve claims.
9. Verified state is reflected on the public profile.

Claim pages must be `noindex` and excluded from the sitemap.

## 5. Prospecting and CRM
The platform should evolve into the operator's daily prospecting tool. It should eventually support:
- business prospect records
- lead/source information
- scan status
- website audit results
- claim status
- contact/owner details
- call tasks and follow-ups
- notes on conversations
- next action/date
- outreach status
- campaign/sequence membership
- lead scoring/prioritisation
- daily prospecting queue
- import/export, including bulk business lists

Target operating model discussed: process approximately 100 prospect records per day across selected business types and locations, subject to data-provider, rate-limit and legal/compliance constraints.

## 6. Website scanner/audit layer
A website audit/scanner should become part of the architecture rather than a separate manual process. It should be able to scan prospect websites and produce actionable business insight that can feed the CRM and outreach workflow.

The scanner should be designed as a reusable service with deterministic diagnostics, validity classification, structured observations and a client-friendly report layer. Avoid overstating what an automated scan can prove.

## 7. Local media/content engine
Content is a core strategic component. The site should be capable of operating as a local media channel rather than only a directory.

Planned publishing capabilities include:
- local news
- events
- food and drink
- business/local-interest articles
- locality content
- category content
- seasonal content
- guides and roundups
- business-generated/assisted articles for paying listings

Content can be sourced or enriched from approved RSS/XML feeds, public event sources, structured data and editorial inputs. External content must respect source licensing, attribution and terms; do not blindly copy third-party articles.

## 8. Publishing agent
A publishing workflow/agent should eventually:
1. Discover candidate stories/events/topics from approved sources.
2. Create a draft.
3. Apply local relevance and quality checks.
4. Add source/attribution information where required.
5. Publish or queue for human approval according to configured rules.
6. Generate appropriate SEO metadata.
7. Optionally distribute approved content to the platform's social channels.

Open-source libraries/tools may be used where appropriate. Paid APIs/services should only be introduced where they provide material value or are required for reliable production operation.

## 9. Social integration
Future architecture should support two distinct social workflows:

### Platform-owned channels
The directory/media brand may connect its own social accounts for distribution of approved local content.

### Business-owned channels
A claimed business may optionally connect authorised social accounts so that agreed content can be created/scheduled/distributed for that business.

This requires explicit business authorisation, secure OAuth/token handling, platform-specific API support and clear separation between the directory's accounts and each business's accounts.

## 10. Commercial content services
Potential monetisable services include:
- enhanced listings
- review/reputation management
- social media management
- blog setup
- recurring topical articles
- social distribution of articles
- creation/setup of missing social profiles where appropriate and authorised
- website audits
- lead generation/campaign services

Pricing and packaging should remain configurable rather than hard-coded until validated commercially.

## 11. Email/outreach
The platform should eventually support individualised outreach based on each business record, including a unique claim link and relevant report/audit. Bulk campaigns should be possible through a compliant email provider rather than by directly sending large volumes from a personal mailbox.

The system should support personalisation, campaign sequencing, unsubscribe/suppression handling, delivery status and audit trails.

## 12. SEO/technical requirements
Maintain:
- canonical URLs
- correct sitemap at `/sitemap.xml`
- robots at `/robots.txt`
- appropriate metadata/Open Graph
- controlled indexation
- noindex for private/admin/claim workflows
- useful structured internal linking
- no thin doorway/page-generation strategy

## 13. Persistence
The production architecture should use Supabase/Postgres through a repository/data-access layer. In-memory stores are acceptable only for temporary development/test fixtures, never as the production source of truth.

## 14. Non-negotiable continuity rule
GitHub is the source of truth. Every meaningful completed phase must be committed. The project must remain recoverable without relying on any single conversation thread or temporary agent container.
