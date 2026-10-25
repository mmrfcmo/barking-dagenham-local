# Barking Local — Site Architecture & Product Blueprint

**Document status:** Working specification  
**Version:** 1.0  
**Last updated:** 25 October 2026  
**Repository:** `mmrfcmo/barking-dagenham-local`  
**Current development branch:** `feature/working-homepage-foundation`  
**Preview:** https://barking-local-homepage-preview.onrender.com

## 1. Product vision

Barking Local is a community-first local information platform for Barking, Dagenham and the wider London Borough of Barking and Dagenham. It should help residents discover useful local information and independent businesses, take part in community life, and subscribe to a useful local newsletter.

The platform should also become a sustainable local media and discovery business through clearly labelled sponsored content, featured business listings and display advertising.

**Guiding principle:** residents should have a reason to visit even when they are not looking at an advert. Trust, usefulness and local relevance come first.

## 2. Status labels — do not confuse mockups with working features

Every feature must be described as one of:
- **Live and verified:** implemented and tested in the deployed environment.
- **Presentational preview:** visible in the static homepage but not connected to a production data source or workflow.
- **Planned:** agreed direction, not implemented yet.
- **Future option:** possible later; not a requirement for the first release.

At the time of this document, the deployed homepage is a **static HTML preview**. Directory search does not query a live listings database. Newsletter calls to action currently use a placeholder mailto address and do not collect or store subscribers. Community submission links are placeholders. No advertising admin, ad database, campaign scheduler, payment workflow, or analytics dashboard is implemented.

Do not claim any preview-only feature is operational. Replace placeholder email addresses before public launch.

## 3. Audience and core journeys

### Residents
1. Land on the homepage and understand what Barking Local offers.
2. Find local businesses, stories, events or practical guides.
3. Subscribe to the newsletter.
4. Suggest an event, story, local hero or community contribution.

### Local businesses
1. Find the business directory and understand how to be listed.
2. Submit or claim a listing, subject to verification and moderation.
3. Keep business information accurate.
4. In future, buy a featured placement or sponsored campaign.

### Site administrator/editor
1. Sign in to a protected admin area.
2. Manage listings, editorial content, events, submissions and newsletter settings.
3. Upload and manage hero images and advertising creatives.
4. Preview, schedule, publish, pause and archive campaigns.
5. Review basic audience and campaign performance when analytics is implemented.

## 4. Information architecture

### Public-facing pages
- **Home** — clear local proposition, hero image, newsletter invitation, directory search, featured businesses, local stories, what's on, local guides and community participation.
- **Business directory** — search, category browse, relevant filters and verified listing results.
- **Business profile** — business name, category, description, address/service area, contact details, website/social links, opening hours where supplied, images, verification/claim status and clearly labelled paid placements.
- **Local stories/news** — article index, category/topic pages and individual articles.
- **What's on / events** — event index and individual event pages with date, venue, organiser, details and source.
- **Local guides** — practical evergreen guides, local recommendations and curated collections.
- **Sponsored content** — editorial-style paid features with clear sponsorship disclosure.
- **Community** — local hero nominations, community notices, story suggestions, poetry/creative submissions and event submissions.
- **Newsletter** — explanation of what subscribers receive, signup form, consent/privacy wording and confirmation state.
- **About / Contact** — purpose, editorial approach, contact details and corrections process.
- **Privacy / Cookie / Terms** — required policies, including newsletter data handling and advertising disclosure.

### Admin pages (planned)
- **Dashboard** — summary of pending submissions, scheduled content and active campaigns.
- **Listings** — create/edit, categories, verification, duplicate review, claim requests and status.
- **Editorial** — stories, guides, events, authors, images, drafts and scheduled publication.
- **Community submissions** — moderation queue, approve/reject/request edits and contributor permissions.
- **Newsletter** — subscriber export/access controls, consent records, signup source and integration status.
- **Advertising** — placements, creative builder, campaigns, scheduling, destination links, status and reporting.
- **Media library** — reusable images/assets, alt text, source/rights notes and crop variants.
- **Settings** — branding, navigation, contact details, integrations and admin access.

## 5. Homepage layout and design system

Recommended homepage order:
1. **Header/navigation** — brand, key sections and a prominent “Join our newsletter” link.
2. **Hero** — distinctive local image, clear headline and primary discovery actions.
3. **Newsletter invitation** — high visibility near the top of the page, not buried at the bottom. Heading: “Join the Barking Local newsletter.” Heading and CTA should share the same destination.
4. **Local stories / what's on / local guides** — useful, regularly refreshed content.
5. **Business directory** — a prominent, visually distinct discovery block and search entry point.
6. **Featured locally** — selected business cards, with paid placements labelled.
7. **Reserved advertising placements** — only where they do not disrupt reading or directory discovery.
8. **Community participation** — local heroes, event/story suggestions and creative contributions.
9. **Newsletter reminder / footer** — secondary opportunity to subscribe.

The exact order may be refined after user testing, but newsletter visibility and the directory are core priorities.

### Visual identity
- Keep the established dark navy/charcoal base with light text, blue accents and orange highlights.
- Yellow may be used sparingly for a key newsletter headline or high-priority callout.
- Use rounded corners and softer shapes for cards, panels, buttons and content containers. Avoid a grid of harsh square-corner boxes.
- Maintain consistent spacing, typography, border treatment, hover/focus states and accessible contrast.
- Make mobile layouts first-class: no clipped text, crowded controls or oversized banners.
- Use the real historic Barking town-centre / East Street archive photograph as the preferred hero direction, **only after locating the original file and verifying reuse permission, credit and image quality**. Do not substitute an unverified image or assume online availability means permission to reuse.
- Current Unsplash images are illustrative placeholders, not verified local photography. Replace or label them appropriately before public launch.

### Reusable UI components
Header/navigation, hero, newsletter CTA, directory search panel, story card, business card, event card, sponsored label, display-ad slot, form field, consent notice, pagination/filter controls, footer and admin status badges should be reusable components rather than separately styled one-offs.

## 6. Advertising architecture

Advertising space should be anticipated in the layout now; a full advertising system is a later implementation phase.

### Planned placement types
- **Hero/banner campaign:** large, high-visibility campaign placement. The editorial/heritage hero image is managed separately from paid hero campaigns so changing one does not unintentionally overwrite the other.
- **Leaderboard:** horizontal display banner, commonly 728 × 90 desktop; responsive variants must be provided for narrow screens.
- **MPU / medium rectangle:** commonly 300 × 250, placed beside or between relevant content where the layout permits.
- **Featured business card:** paid or promoted directory card with clear disclosure.
- **Sponsored content:** sponsored article, local guide, event or business story.
- **Campaign banner:** temporary promotion for a local event, seasonal campaign or borough-wide initiative.

Sizes are standard starting points, not hard-coded promises that every creative will fit every screen. The frontend should render responsive variants and preserve image aspect ratio.

### Advertising manager — planned MVP
Admin should be able to:
1. Create a campaign and internal name.
2. Select one or more available placements.
3. Upload artwork (JPG, PNG, WebP) or compose a creative from a template.
4. Enter advertiser name, headline/alt text, destination URL and optional CTA.
5. Preview desktop and mobile placements.
6. Choose crop/focal point and upload a separate mobile creative when needed.
7. Save draft, publish, pause, schedule start/end dates and archive.
8. Clearly mark paid content as “Sponsored” or “Featured”.
9. Prevent expired or paused campaigns from showing.
10. Later review impressions, clicks and click-through rate.

Do not stretch one image indiscriminately into all formats. Prefer responsive creative templates that rearrange logo, image, headline and CTA, with manual overrides for each placement. Do not introduce automatic payments or a self-service advertiser portal in the first MVP unless separately approved.

### Advertising records (conceptual)
Campaign: id, name, advertiser, status, start/end time, destination URL, disclosure label, created/updated timestamps.  
Creative: id, campaign id, asset reference, headline, body, CTA, alt text, desktop/mobile variants, crop/focal settings.  
Placement: id, name, format, page/slot, responsive rules, active status.  
CampaignPlacement: campaign id, placement id, creative id, priority/rotation settings.  
Metrics (later): date, campaign/creative/placement id, impressions, clicks.

## 7. Data model (conceptual)

Use stable IDs, timestamps, validation, and explicit status fields. Do not treat this conceptual list as proof that a database already exists.

- **Business:** name, slug, category IDs, description, address/service area, contact channels, website/social URLs, opening hours, image references, source, verification status, claim status, listing tier, timestamps.
- **Category:** name, slug, parent category, description and synonyms/search terms.
- **Article/Guide:** title, slug, summary, body, author, topic, image/alt text, publication status/date, source/rights notes, sponsorship disclosure.
- **Event:** title, summary, start/end time, venue/address, organiser, booking URL, image, status, source and timestamps.
- **CommunitySubmission:** type, contributor contact/consent, content, attachments, moderation status, reviewer notes and timestamps. Restrict access to personal data.
- **Subscriber:** email, consent text/version, consent timestamp, signup source, subscription status, unsubscribe timestamp and integration/provider reference. Minimise collected data and protect it.
- **Campaign/Creative/Placement:** as described in Section 6.
- **AdminUser/Role:** identity, role, permissions, authentication reference and audit trail.

Avoid collecting unnecessary personal information. Provide unsubscribe capability, appropriate consent/privacy information, and secure access to subscriber data.

## 8. Directory search requirements

The current search is a placeholder. Planned search should:
- Match business names, categories, descriptions, services and relevant synonyms.
- Support partial words and sensible typo tolerance.
- Understand common variants (for example, “accountant”, “accounting” and “tax adviser”).
- Rank results by relevance and local service area, without silently implying paid results are the best match.
- Clearly label sponsored results.
- Show useful empty states and category suggestions.
- Work well on mobile and with keyboard/screen-reader navigation.

Start with ordinary indexed database search and a synonym/category map. Add a search service or AI only if real usage shows it is necessary.

## 9. Technical architecture principles

The current deliverable is static HTML hosted on Render and deployed from GitHub branch `feature/working-homepage-foundation`. Do not assume there is an application backend.

Target logical layers:
1. **Presentation:** responsive public website and protected admin interface.
2. **Application/API:** listings/search, content, submissions, newsletter integration and campaign management.
3. **Data/storage:** relational data store for structured records and object storage for images/creative assets.
4. **Integrations/operations:** email delivery/newsletter provider, hosting, analytics, backups, monitoring and access control.

Technology choices should favour low operating cost, straightforward maintenance, portability and the ability for an AI development agent to work from a documented repository. Select specific services only after checking existing Render/GitHub configuration and expected cost. Never put secret keys in client-side HTML or commit them to Git.

## 10. Phased implementation roadmap

### Phase 0 — Foundation and specification
- Keep the approved homepage preview stable.
- Version this architecture document and update it when decisions change.
- Verify repository branch, deployment source and current live commit.
- Establish a simple test checklist and record preview-only placeholders.

### Phase 1 — Audience capture
- Implement a real newsletter signup form and connect a newsletter/email provider.
- Store or synchronize subscriber consent and subscription status appropriately.
- Add success/error states, unsubscribe support and privacy information.
- Test a full signup and unsubscribe journey end-to-end.

### Phase 2 — Directory MVP
- Choose and configure a database.
- Import a reviewed seed dataset with source and last-verified date.
- Build category browsing, useful search, individual business pages and moderation.
- Add listing submission/claim process and duplicate handling.
- Never present invented or unverified data as verified.

### Phase 3 — Editorial and community
- Build admin content editing for stories, guides and events.
- Add moderation workflows for user-submitted content.
- Implement source/rights tracking and clear corrections/contact paths.

### Phase 4 — Advertising MVP
- Add secure admin access and media storage.
- Build campaign, creative and placement management.
- Support upload, preview, crop/focal point, mobile variant, scheduling, pause/publish and clear sponsorship labels.
- Begin with administrator-managed campaigns; defer self-service advertiser accounts and payments.
- Test that expired/paused campaigns stop appearing and that normal editorial content remains separate.

### Phase 5 — Reporting and commercial growth
- Add basic campaign impression/click reporting, with appropriate privacy controls.
- Consider featured listing packages, paid campaign booking and payment processing only after demand and operational needs are understood.
- Improve the site based on real audience and advertiser feedback.

## 11. Acceptance criteria and quality gates

A feature is not “done” just because it looks right in a screenshot. Verify:
- Responsive behaviour at desktop, tablet and mobile widths.
- Links and buttons go to the intended destination.
- Forms validate input and display success/error states.
- Data persists where persistence is promised.
- Admin-only operations require authentication and authorization.
- Advertisements are clearly disclosed and respect schedule/status.
- Images have appropriate alt text and usage rights.
- Keyboard focus, readable contrast and semantic headings are maintained.
- No placeholder addresses, demo content or unverified listings are represented as production-ready.
- Deployment is live on the intended branch and the changed feature has been checked in the deployed environment.

## 12. Instructions for Energentic AI or any development agent

Treat this file as the product-level source of truth, together with explicit newer user-approved decisions.

Before changing code:
1. Inspect the repository, current branch, latest commits and Render deployment settings.
2. Report what is actually implemented versus this specification.
3. Propose the smallest coherent implementation for the current phase.
4. Preserve approved design decisions and unrelated functionality.
5. Do not silently change production or a different branch.
6. Do not add paid infrastructure, third-party services or API costs without approval.
7. Keep secrets out of code and logs.
8. Make incremental commits with clear messages.
9. Test changed behaviour and report exact commit/deployment status.
10. Update this document when architecture or approved product behaviour changes.

If requirements conflict, stop and ask rather than guessing. Do not implement every future feature in one pass.

## 13. Decisions to confirm later

These remain open and should not be guessed:
- Newsletter provider and whether subscriber records live with that provider, in the app database, or both.
- Database and image/object storage choice.
- Exact admin authentication and roles.
- Listing verification and claim policy.
- Advertising rates, inventory limits, rotation and campaign reporting.
- Whether the historic hero photograph can be licensed for reuse.
- Editorial approval policy, retention policy and legal/privacy review.
- Exact production domain and launch criteria.

---

**North star:** build a useful, trustworthy local community platform first, with newsletter audience capture and directory discovery at its core, and a maintainable advertising system that can be added without redesigning the entire site.
