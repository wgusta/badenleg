# BadenLEG Strategy (Acquisition Goal)
**Primary goal:** become the obvious acquisition (or exclusive licensing) target for **Regionalwerke Baden** or **Eniwa** by delivering a utility-grade “LEG onboarding + formation + ops” platform with proven local traction.

**Principle:** optimize for what a regulated utility will buy: **compliance readiness, low risk, integration friendliness, trusted brand posture, and verified demand**.

---

## 1) Acquisition Thesis (What They Buy)

Utilities will buy BadenLEG if it becomes the fastest, lowest-risk path to:

1. **Regulatory readiness** for LEG customer onboarding and community formation workflows.
2. **Operational readiness** (status tracking, case handling, auditable processes).
3. **Integration readiness** (CRM/billing/GIS exports + clean APIs).
4. **Proven local demand** (verified households + formation-ready clusters).
5. **Transferable consent** (explicit user consent to share data with the utility for LEG activation).

**Non-goal:** positioning as “anti-utility” disruptor. That may create short-term adoption but reduces acquisition probability.

---

## 2) What Regionalwerke Baden / Eniwa Likely Value

### Must-haves (deal blockers if missing)
- **Data protection & consent**: clear consent flows, retention rules, delete/export requests, audit trail.
- **Reliability**: persistent DB, backups, monitoring, and repeatable deployments.
- **Security posture**: rate limits, input validation, secure headers, logging (see `SECURITY.md`).
- **Operational tooling**: internal dashboard for case/status management.
- **Integration**: exports/APIs that fit existing utility workflows.

### Differentiators (increase price + urgency)
- **Territory intelligence**: formation readiness by neighborhood/grid area + PV/consumption estimates.
- **Formation acceleration**: document workflows, checklists, pre-filled templates, and status tracking.
- **White-label readiness**: utility branding + multi-territory configuration (Baden + Aarau region).

---

## 3) Product Positioning (Acquisition-Friendly)

**BadenLEG = the customer experience + formation pipeline layer** that sits *in front of* utility systems:

- **Front-door**: helps residents understand LEG, register interest, and form communities.
- **Qualification**: turns “interest” into **formation-ready** communities with complete metadata.
- **Handoff**: exports a clean, consented “LEG-ready package” to the utility for activation/operations.

This makes BadenLEG valuable even **without** building a full billing stack pre-acquisition.

---

## 4) Phased Feature Roadmap (Built for Acquisition)

Time horizons are intentionally relative; tighten once a pilot schedule is set with either utility.

### Phase 0 — “Acquisition Hygiene” (0–4 weeks)
**Objective:** remove deal blockers (reliability, compliance, operational visibility).

**Features**
- **Persistence + backups**: move from “best effort” storage to a clear production standard (PostgreSQL preferred; volume+JSON acceptable short-term if hardened).
- **Admin dashboard (internal)**: view registrations, verification status, clusters, exports, and basic audit events.
- **Consent & privacy controls (user-facing)**:
  - consent to “share my data with the local utility for LEG activation”
  - granular opt-ins (newsletter, updates, contact exchange)
  - retention + delete/export request path
- **Observability**: error monitoring + basic metrics (funnel, email delivery, cluster readiness).
- **Operational logs**: minimal audit trail for registration/confirmation/export actions.

**Done criteria**
- Can prove: “no data loss, auditable exports, explicit consent, reproducible deploy”.

---

### Phase 1 — “Demand Engine + Trust” (1–2 months)
**Objective:** maximize verified demand while staying privacy-safe and acquisition-friendly.

**Features**
- **Progressive profiling** (low friction now, richer data later):
  - owner/renter + landlord approval status
  - solar status + rough kWp + consumption band (already in pipeline docs)
  - optional meter ID / connection info (only when needed)
- **User dashboard**: community readiness, next steps, clear expectations, opt-in to “utility handoff”.
- **Referral system (privacy-safe)**:
  - keep sharing links and tracking
  - avoid public street-level leaderboards unless privacy impact is proven safe and acceptable
- **Territory gates**: explicitly support Baden territory + add framework for Eniwa territory (config-driven).

**Done criteria**
- Verified household growth with measurable funnel improvements (visit → register → confirm → “formation-ready”).

---

### Phase 2 — “Formation Accelerator (MVP)” (2–4 months)
**Objective:** turn clusters into communities with structured, auditable steps the utility will recognize.

**Features**
- **Formation wizard MVP** (from `PLATFORM-PIPELINE.md`):
  - community setup (roles, admin, start date)
  - participant invitation + confirmation
  - distribution model selection (simple presets first)
  - checklist + “readiness score”
- **Document package generation**:
  - participant agreement + community agreement templates (Baden/Aargau variants)
  - DSO notification/registration forms
  - export bundle (PDFs + CSV metadata)
- **Community workspace**:
  - tasks, status, participant list
  - secure messaging/email updates (lightweight)

**Done criteria**
- Communities can reach “handoff-ready” state with a standardized export package and audit log.

---

### Phase 3 — “Utility Ops + Integration” (4–8 months)
**Objective:** make BadenLEG operationally indispensable and easy to integrate.

**Features**
- **Utility console (role-based access)**:
  - pipeline view: interested → verified → formation-started → handoff-ready → activated
  - internal notes + status transitions
  - outbound messaging templates (utility-branded)
- **Integration surface**
  - CSV exports (CRM import-ready)
  - webhooks / REST API for status + lead ingestion
  - GIS-friendly exports for territory/cluster visualization
- **White-label / multi-tenant**
  - theming, domains, content overrides
  - territory configuration (Baden vs Eniwa region)
  - tariff/config adapters as data inputs (not hard-coded)

**Done criteria**
- Either utility can pilot BadenLEG without major internal IT projects (export-first, API second).

---

### Phase 4 — “Servicing-Ready Modules” (optional pre-acquisition, strong post-acquisition) (8–12+ months)
**Objective:** increase strategic value without taking on unnecessary integration risk.

**Features (modular)**
- **Reporting & transparency** first: community performance reports, savings estimates, CO₂ impact.
- **Billing calculation engine** only if data access exists:
  - design for “utility billing integration” rather than replacing billing
  - keep it as a separable module to reduce acquisition integration risk

**Done criteria**
- A clear “post-acquisition roadmap” exists that the buyer can execute with their meter/billing access.

---

## 5) Evaluation of Existing Strategy Considerations (Against This Goal)

This project already contains several strategic drafts; below is how they perform specifically for **utility acquisition**.

### `ACQUISITION-STRATEGY-16112025.md`
**Effective**
- Correct north star: build a three-stage pipeline (matchmaking → creation → servicing).
- Strong framing: “avoid internal build cost/time” and “bring verified demand”.

**Needs adjustment**
- The roadmap assumes large, heavy integrations (billing/SEPA/meter APIs) early. For acquisition, prefer **export-first + utility-console** before deep billing.
- Some timelines/budgets are optimistic; convert to pilot-based milestones with clear “done criteria”.

### `PLATFORM-PIPELINE.md`
**Effective**
- Detailed, utility-friendly user journey and data model ideas.

**Needs adjustment**
- Add an explicit “utility handoff” layer: consent, export bundle, internal statuses, and audit logs.

### `BLITZ-STRATEGY-*.md`
**Effective**
- Adoption focus is valuable: a verified user base is acquisition leverage.
- Partnerships (installers/cooperatives) build distribution without heavy ad spend.

**Needs adjustment**
- “Anti-utility / middleman” positioning increases reputational risk and reduces buyer willingness.
- Public leaderboards/FOMO mechanics must be privacy-safe; utilities are conservative here.
- “Free everything” is fine for end-users, but the business framing should shift to **B2B licensing / acquisition** (utility pays, customers don’t).

### `REFERRAL-PRICING-SYSTEM.md`
**Effective**
- Transparency + DIY path builds trust and reduces perceived lock-in.

**Needs adjustment**
- Complex consumer pricing/referral discounts matter less for acquisition than **clean utility procurement** (license, pilot, SLA).
- Keep referrals as growth engine; simplify pricing narrative toward B2B.

### `strategic-meeting-16112025.md`
**Effective**
- Correctly identifies “toy vs product” blockers (persistence, SMTP, analytics).

**Needs adjustment**
- Shift messaging from “competition” to “utility-grade enablement layer” while staying user-trustworthy.

---

## 6) Success Metrics (Acquisition-Ready Proof)

**Demand**
- Verified households in target territory (Baden + optional Eniwa territory)
- Formation-ready clusters (count + average time to readiness)

**Formation throughput**
- Communities started → handoff-ready → activated (by utility or pilot partner)
- Median time from “ready” to “handoff-ready”

**Trust / compliance**
- Consent rates for “utility handoff”
- Data deletion/export requests handled within SLA
- Security incident rate (target: zero; track attempts and mitigations)

**Operational readiness**
- Utility console usage (cases handled, exports delivered)
- Reliability metrics (uptime, backup restores tested)

---

## 7) Risks & Mitigations (Acquisition Lens)

- **Adversarial positioning** → adopt neutral/pro-compliance messaging; avoid “utility enemy” framing.
- **Privacy risk from gamification** → privacy review before publishing rankings/leaderboards.
- **Integration scope creep** → export-first, pilot-first; keep billing as modular.
- **Regulatory ambiguity** → make checklists configurable; document assumptions and update cadence.

---

## 8) Next 30 Days (Highest Leverage)

1. Ship Phase 0 items (persistence, consent, audit, admin dashboard).
2. Define the “utility handoff package” (exact fields + PDF/CSV bundle).
3. Prepare a pilot pitch that is operationally simple: export-first, minimal IT effort for the utility.

---

## Current Implementation Snapshot (Dec 2024)

- ✅ Added explicit consent capture (neighbor sharing + utility handoff) in registration flows; server blocks registration if missing.
- ✅ Added lightweight audit log (`/data/audit.log`) for registration events.
- ✅ Added token-protected admin overview (`/admin/overview`) with counts + audit tail; requires `ADMIN_TOKEN` env.
- ✅ Added EVU-ready export endpoints (`/admin/export?format=json|csv`) filtered to consented users by default.
- ✅ Kept persistence via JSON/volume (no Railway changes).

### Needs You / Not Done (no Railway changes applied)
- Set `ADMIN_TOKEN` in the environment to use `/admin/overview`.
- Decide on production persistence path: keep volume+JSON or migrate to PostgreSQL (recommended for acquisition readiness).
- Add monitoring/alerts (Sentry/GA/Metrics) and backup verification in production.
- Define and render the “utility handoff package” (PDF exports + field list) and an admin UI for export/download.
- Configure SendGrid/SMTP with domain auth for production deliverability (currently optional/soft-fail).

### Still Pending (needs environment/owner decisions)
- Set `ADMIN_TOKEN` in prod/stage env; verify `/admin/overview` and `/admin/export`.
- Choose persistence backend and migrate (PostgreSQL recommended) + backup/restore drills.
- Add monitoring/alerting (Sentry/GA/Metrics) and test backup restores.
- Define and generate a formal “utility handoff package” (PDF export + field list) and add a simple admin UI for downloads.
- Configure SendGrid/SMTP with domain authentication for reliable delivery.
