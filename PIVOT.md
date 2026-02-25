# OpenLEG: Pivot to Public Infrastructure

**Version:** 2026-02-25
**Status:** Active. Replaces commercial strategy from open-strategy.md.

---

## The Pivot

OpenLEG is no longer a B2B SaaS product selling to energy providers. It is free, open-source public infrastructure for Swiss Lokale Elektrizitätsgemeinschaften.

**Old model:** Sell compliance tooling to EVUs (CHF 500-9900/month) + sell aggregated citizen meter data as B2B insights.

**New model:** Free platform for LEGs and municipalities. Open-source code. Open data API. Professional services for those who need help. No data selling.

---

## Why

1. The B2B revenue model had <35% probability of working on its stated timeline (our own assessment)
2. Selling citizen smart meter data to energy providers contradicts the mission of citizen energy autonomy
3. CHF 500/month for 0-2 LEG requests/year is negative ROI for small Gemeindewerke
4. "Do nothing / Excel" is the real competitor, and free beats CHF 500/month
5. Making citizens more autonomous from energy providers while selling their data to those same providers is a structural contradiction
6. Infrastructure costs are CHF 500/month total. Revenue is not a survival requirement if grant-funded or personally funded.

---

## What Changed

### Killed
- B2B Insights API tiers (CHF 990/2990/9900/month): no longer selling citizen data
- EVU SaaS subscription (CHF 500+/month): EVU compliance portal remains but free
- VNB sales pipeline and outreach automation: LEA no longer a sales engine
- Formation fees (CHF 199) and servicing fees (CHF 14.90/month)

### Kept
- Free public API (ElCom tariffs, Sonnendach, Energie Reporter, value-gap, financial model)
- Municipality onboarding (free, always was)
- Resident registration + DBSCAN clustering
- Formation wizard + document generation
- Smart meter parsing (data stays with LEG)
- All data pipelines (ElCom SPARQL, Sonnendach, Energie Reporter)
- OpenClaw/LEA (repurposed)

### New
- GitHub repo (AGPL-3.0 license)
- LEA as autonomous open-source contributor (community support, data updates, transparency monitoring)
- VNB transparency scores (public ranking of DSO cooperation)
- Municipality-first positioning (Gemeinden as primary acquisition channel)
- Data sovereignty promise: "Ihre Daten bleiben bei Ihnen"
- Self-hosting instructions

---

## LEA's New Role

LEA (OpenClaw AI) operates autonomously with one goal: maximize the number of functioning LEGs in Switzerland.

### Daily (autonomous)
- Community health check: identify stuck formations, suggest next steps
- Data pipeline maintenance: ElCom, Sonnendach, Energie Reporter refresh
- Respond to community questions

### Weekly (autonomous)
- Seed 50 new municipalities via `upsert_tenant`
- Refresh public data for all active cantons
- Check formation progress across all tenants

### Monthly (autonomous)
- VNB transparency scoring: rate all 631 DSOs on LEG cooperation
- Regulatory watch: track BFE/ElCom changes
- Open source health: review repo, update docs

### Continuous
- GitHub issue triage
- Community discussions
- Documentation updates
- Data quality monitoring

---

## Revenue Model (Hybrid)

### Free tier (everyone)
- Platform access for residents, municipalities, LEGs
- All document generation
- Smart meter data processing (data stays local)
- Public data API
- Community matching and formation

### Professional services (optional, for municipalities/cantons that want support)
- Onboarding support and training
- SDAT-CH integration consulting
- Custom formation workflows
- SLA-backed hosting
- Pricing: project-based, not subscription

### Grant funding (applied for)
- BFE Pilot/Lighthouse programs
- Cantonal energy office digitalization budgets
- Pronovo renewable energy support
- Foundation grants (Mercator, Ernst Göhner, Engagement Migros)

### Target: CHF 50K BFE grant covers 8+ years of operations

---

## Go-to-Market: Municipality First

### Why municipalities, not EVUs
- Political motivation: Gemeindepräsident wants press for enabling energy transition
- Budget authority: Gemeinde can sponsor or promote without procurement
- Citizen contact: Gemeinde reaches residents directly (Gemeindeblatt, website)
- No adversarial dynamic: unlike EVUs, municipalities benefit from LEG formation

### The funnel
1. LEA seeds municipality as tenant (automated)
2. Municipality discovers OpenLEG (organic, referral, or outreach)
3. Gemeinde registers at /gemeinde/onboarding (free, 2 minutes)
4. Gemeinde promotes to residents (their own channels)
5. Residents register, clusters form, LEGs emerge
6. LEA monitors and supports formations

### No sales team needed
The product is free. The barrier is awareness, not price. LEA seeds all 2'131 municipalities. Organic discovery and word-of-mouth between Gemeindepräsidenten at conferences does the rest.

---

## Technical Changes

### Website
- Hero: citizen-first (Bewohner tab default, Gemeinde second, no EVU tab)
- Pricing: "Kostenlos. Open Source. Für immer." (three CHF 0 cards)
- How-it-works: 5-step LEG formation journey for citizens
- Nav: "Stromgemeinschaft gründen", "Für Gemeinden", "Open Source", "API"
- Footer: GitHub link, data sovereignty tagline

### OpenClaw (LEA)
- SOUL.md: rewritten for public infrastructure mission
- AGENTS.md: rewritten with LEG-enablement standing objectives
- Sales pipeline tools: repurposed for transparency monitoring
- New focus: community health, municipality seeding, regulatory watch

### Code (deferred, not blocking)
- api_b2b.py: endpoints remain but repurposed for LEG member dashboards (not sold to EVUs)
- insights_engine.py: outputs served to LEG members, not B2B API
- data_consents: simplified (no tier system needed if data isn't sold)
- GitHub repo setup: push code, AGPL-3.0, contributor guide, CI

---

## Metrics

| Metric | Target (6 months) | Target (12 months) |
|--------|-------------------|---------------------|
| Municipalities seeded | 500 | 2'131 (all) |
| Municipalities active (with registrations) | 50 | 200 |
| Resident registrations | 500 | 5'000 |
| Active LEGs | 5 | 50 |
| GitHub stars | 100 | 500 |
| Public API requests/day | 1'000 | 10'000 |
| VNBs with transparency score | 100 | 631 |

---

## Risks

### Risk 1: Nobody uses it even though it's free
**Probability:** Medium. Free removes price objection but not awareness/motivation.
**Mitigation:** Municipality-first. Gemeindepräsidenten promote to residents. LEA seeds data so every municipality has a pre-populated profile.

### Risk 2: Development stalls without revenue
**Probability:** Medium. One developer, no income from the platform.
**Mitigation:** BFE grant application. Professional services revenue. Personal runway. The codebase is functional today; it needs maintenance, not rebuilding.

### Risk 3: EVUs soft-block formations through OpenLEG
**Probability:** Low. The platform doesn't antagonize EVUs, it simply doesn't prioritize them.
**Mitigation:** VNB transparency scores create accountability. ElCom complaint path for non-compliance.

### Risk 4: Open source but no community
**Probability:** High initially. Swiss energy tech is niche.
**Mitigation:** Start with data contributions (municipality profiles, tariff updates). Lower the bar for contribution. Academic partnerships (ETH, ZHAW, HSLU energy programs).

---

## Decision Filter (New)

Before building anything, ask: "Does this help a citizen form or improve a LEG?"

Yes: build it now.
No: skip it.
Maybe: check if a resident or municipality requested it.

---

## Relationship to open-strategy.md

The original strategy document contains valuable regulatory analysis, competitive landscape data, and legal references that remain accurate. This pivot document replaces the business model, go-to-market, and revenue sections. The regulatory context (Section: "What the Law Actually Says") and competitive landscape (Section: "The Competitive Landscape") in open-strategy.md remain the canonical references.

---

*Last updated: 2026-02-25.*
