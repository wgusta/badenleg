# BadenLEG Acquisition Plan: Efficient Execution Path
**Target:** Regionalwerke Baden acquisition by Aug 2026
**Current Status:** Phase 0 infrastructure complete, formation wizard coded but not integrated
**Timeline:** 6 months (Feb-Aug 2026)

---

## Executive Summary

BadenLEG has the foundation (PostgreSQL, referral system, GA4, formation wizard code) but needs focused execution on **proof points** Regionalwerke Baden will buy:

1. **Verified demand** (registered, consented households)
2. **Formation capability** (communities ready for activation)
3. **Utility handoff package** (clean export, audit trail, consent management)
4. **Operational dashboard** (internal case management)

**Strategy:** Skip perfection, build acquisition evidence. Minimum viable features that prove the business case.

---

## Current Asset Inventory

### ✅ Completed Infrastructure
- PostgreSQL database with connection pooling
- Referral system with tracking
- Google Analytics 4 integration
- Formation wizard module (670 LOC, not integrated)
- Consent capture (neighbor sharing + utility handoff)
- Audit logging
- Admin endpoints (token-protected)
- Export endpoints (JSON/CSV)
- Security hardening (rate limits, validation, headers)

### ⚠️ Partially Complete
- Admin dashboard exists but basic
- Export format not "utility-ready" (needs specific fields)
- Formation wizard not connected to UI
- Email automation (SendGrid configured but limited flows)

### ❌ Missing (Critical for Acquisition)
- **Formation UI** (wizard frontend)
- **Utility handoff package** (PDF exports, field mapping)
- **Internal ops dashboard** (case management, status tracking)
- **Document generation** (contracts, DSO forms)
- **User dashboard** (community readiness, next steps)

---

## Acquisition-Focused Priorities (Next 6 Months)

### **Phase 1: Demand Proof** (Feb-Mar 2026) - 6 weeks
**Goal:** 500+ verified households with explicit utility handoff consent

**Week 1-2: Marketing Foundation**
- [ ] Update homepage with urgency messaging ("LEG legal now")
- [ ] Add live counter, social proof elements
- [ ] Launch Facebook ads (CHF 2K budget)
- [ ] Partner outreach: 10 solar installers, 5 housing cooperatives
- [ ] Press release to Badener Tagblatt

**Week 3-4: Email Automation**
- [ ] Day 1: Welcome + neighbor matches
- [ ] Day 3: Smart meter question
- [ ] Day 7: Consumption data collection (optional)
- [ ] Day 14: Formation readiness check
- [ ] Implement dashboard "readiness score" widget

**Week 5-6: Growth Acceleration**
- [ ] Referral program promotion (CHF 50 credits)
- [ ] Street-level targeting (Facebook ads for partial clusters)
- [ ] WhatsApp groups for formed clusters (social lock-in)
- [ ] Community confirmation emails

**Success Metrics:**
- 500+ registered addresses
- 60%+ complete energy profiles
- 70%+ utility handoff consent
- 20+ clusters with 3+ confirmed members

---

### **Phase 2: Formation Capability** (Apr-May 2026) - 8 weeks
**Goal:** 10-20 communities reach "handoff-ready" state

**Week 1-3: Formation Wizard UI**
- [ ] Community creation flow (name, admin, members)
- [ ] Member invitation system (email links)
- [ ] Status dashboard (interested → formation-started → ready)
- [ ] Distribution model selection (simple presets only)
- [ ] Integrate formation_wizard.py backend (already coded)

**Week 4-6: Document Generation MVP**
- [ ] Community agreement template (German, Aargau jurisdiction)
- [ ] Participant contract template
- [ ] DSO notification form (Regionalwerke Baden format)
- [ ] PDF generation (simple, not perfect)
- [ ] Electronic signature collection (DocuSign or simple email confirmation)

**Week 7-8: First Wave Activation**
- [ ] Pilot with 5 communities (handpick enthusiastic users)
- [ ] Generate documents, collect signatures
- [ ] Submit DSO notifications
- [ ] Track approval process
- [ ] Document learnings

**Success Metrics:**
- 10-20 communities in formation process
- 5+ DSO submissions completed
- Full document package generated for each
- 100% signature collection rate (pilot group)

---

### **Phase 3: Utility Ops Layer** (May-Jun 2026) - 6 weeks
**Goal:** Prove operational readiness to Regionalwerke Baden

**Week 1-2: Internal Dashboard**
- [ ] Pipeline view: interested → verified → forming → handoff-ready → active
- [ ] Filter/search by status, address, cluster
- [ ] Community detail view (members, documents, timeline)
- [ ] Export controls (consented users only, date ranges)
- [ ] Audit log viewer

**Week 3-4: Utility Handoff Package**
- [ ] Define exact fields Regionalwerke needs (engage DSO contact)
- [ ] CSV format: household data, meter IDs, consumption profiles
- [ ] PDF bundle: contracts, community details, member list
- [ ] Consent verification (explicit utility sharing flag)
- [ ] Metadata: formation date, readiness score, contact info

**Week 5-6: Integration Surface**
- [ ] REST API endpoints (read-only, token-authenticated)
- [ ] Webhook support (status change notifications)
- [ ] GIS export (KML/GeoJSON for territory visualization)
- [ ] Documentation (API specs, integration guide)

**Success Metrics:**
- Complete utility handoff package for 20+ communities
- Internal dashboard used daily (track usage)
- API documentation ready
- Export format validated with DSO contact (informal)

---

### **Phase 4: Acquisition Approach** (Jun-Aug 2026) - 10 weeks
**Goal:** Negotiate and close acquisition deal

**Week 1-2: Proof Package Assembly**
- [ ] Metrics dashboard: registrations, formations, activations
- [ ] Customer testimonials (5-10 video/written)
- [ ] Media coverage compilation
- [ ] Cost avoidance analysis (RW build cost vs. acquisition price)
- [ ] Platform demo video (5 min)
- [ ] Technical documentation audit

**Week 3-4: First Contact**
- [ ] Identify decision-maker (CEO, COO, or Head of New Services)
- [ ] Intro email with proof package
- [ ] Request meeting (pitch as partnership/licensing, not acquisition)
- [ ] Prepare presentation (15 slides max)

**Week 5-6: Negotiation**
- [ ] Present business case
- [ ] Highlight acquisition value (customers, cost savings, time to market)
- [ ] Discuss deal structures (acquisition, licensing, partnership)
- [ ] Request term sheet

**Week 7-10: Due Diligence & Closing**
- [ ] Legal review (contracts, IP, liabilities)
- [ ] Technical review (code audit, security assessment)
- [ ] Financial audit (costs, revenue potential)
- [ ] Finalize terms (price, earnout, transition services)
- [ ] Sign agreements

**Target Valuation:** CHF 300K-500K (base + earnout)

---

## Feature Scope: What NOT to Build

### ❌ Skip These (Pre-Acquisition)
- **Mobile apps** (web-first sufficient)
- **15-minute billing calculator** (utility has meter data)
- **SEPA integration** (not needed until post-DSO approval)
- **Chat/messaging** (WhatsApp sufficient)
- **Multi-language** (German only for Baden)
- **Complex distribution models** (simple/equal split only)
- **Smart meter API integration** (manual upload acceptable)
- **Advanced analytics** (basic metrics sufficient)

### ✅ Focus on These (Acquisition Evidence)
- **Verified household count** (quantity over quality)
- **Formation throughput** (communities reaching "ready" state)
- **Document generation** (prove process automation)
- **Utility handoff package** (exactly what they need)
- **Consent management** (regulatory compliance)
- **Operational dashboard** (internal case handling)

---

## Development Resource Allocation

### Solo Developer Capacity (Assumed)
- **20 hours/week** development time
- **6 months** = ~480 hours total
- **Priority:** Features that prove acquisition value

### Time Budget by Phase
1. **Demand Proof** (Feb-Mar): 120 hours
   - 40h marketing/content
   - 40h email automation
   - 40h referral/growth features

2. **Formation Capability** (Apr-May): 160 hours
   - 80h formation wizard UI
   - 60h document generation
   - 20h pilot support

3. **Utility Ops Layer** (May-Jun): 120 hours
   - 50h internal dashboard
   - 40h handoff package
   - 30h API/integration

4. **Acquisition Prep** (Jun-Aug): 80 hours
   - 30h proof package
   - 20h presentation/demo
   - 30h due diligence support

**Total:** 480 hours (exactly capacity)

---

## Technology Decisions (Lock In Now)

### Frontend
- **Stick with current:** Vanilla JS, TailwindCSS, Leaflet
- **Why:** No React/Vue overhead, faster iteration
- **Trade-off:** Less maintainable long-term (but acquisition solves this)

### Backend
- **Keep Flask:** Already built, works fine
- **PostgreSQL:** Already migrated, sufficient
- **SendGrid:** Already configured, scales to 1000s emails

### Documents
- **WeasyPrint or ReportLab:** Python PDF generation
- **Jinja2 templates:** HTML → PDF pipeline
- **No external services:** Avoid DocuSign cost (email confirmation sufficient)

### Deployment
- **Railway or Infomaniak VPS:** Current setup works
- **Don't change:** Stability > optimization

---

## Risk Mitigation

### Risk 1: Not Enough Registrations
**Mitigation:**
- Front-load marketing budget (Feb-Mar)
- Partnership blitz (installers, cooperatives)
- Aggressive referral incentives
- **Kill criteria:** <200 by Mar 15 → pivot to direct utility sales

### Risk 2: Formation Process Too Complex
**Mitigation:**
- Pilot with 5 handpicked communities first
- Simplify: equal distribution only, standard templates
- Manual fallback (PDF email if automation fails)
- **Acceptance:** 80% success rate acceptable (not 100%)

### Risk 3: DSO Approval Delays
**Mitigation:**
- Pre-engage DSO contact (informal consultation)
- Standard templates reviewed by DSO before bulk submission
- **Plan B:** Present communities as "ready to submit" (don't need approved)

### Risk 4: Regionalwerke Ignores Outreach
**Mitigation:**
- PR pressure (media coverage creates urgency)
- Alternative buyers (Eniwa, Axpo, EKZ)
- Continue independent growth path
- **Backup:** Licensing model to multiple utilities

### Risk 5: Technical Failures at Scale
**Mitigation:**
- Start small (50 → 200 → 500 users)
- Manual backup processes for critical flows
- Monitor errors (Sentry), fix fast
- **Acceptable:** 95% uptime (not 99.9%)

---

## Success Definition (Acquisition Readiness)

### Must-Have Proof Points
✅ **500+ verified households** (Baden territory)
✅ **20+ communities** in formation (documented pipeline)
✅ **10+ DSO submissions** (proof of operational throughput)
✅ **Utility handoff package** (complete, tested export)
✅ **Consent compliance** (70%+ utility sharing consent)
✅ **Internal dashboard** (case management operational)
✅ **Security/privacy audit** (no major vulnerabilities)
✅ **Acquisition deck** (metrics, testimonials, integration plan)

### Nice-to-Have (Strengthen Position)
- 1000+ registered households
- 50+ communities formed
- Media coverage (5+ articles)
- Alternative buyer interest
- Revenue (CHF 10K+ from formation fees)

---

## Weekly Execution Rhythm

### Monday (Planning)
- Review metrics (registrations, formations, activations)
- Set weekly goals (3-5 specific outcomes)
- Prioritize features (acquisition value score)

### Tuesday-Thursday (Building)
- Feature development (focus time)
- User support (email, questions)
- Partnership outreach

### Friday (Shipping)
- Deploy week's work
- QA/testing
- Document progress

### Weekend (Growth)
- Marketing campaigns
- Social media
- Community engagement

---

## Next 2 Weeks: Immediate Actions

### Week 1 (Feb 3-9)
1. **Update homepage** (urgency messaging, live counter)
2. **Launch Facebook ads** (CHF 500 initial)
3. **Email 10 solar installers** (partnership outreach)
4. **Set up email automation** (Day 1, 3, 7, 14 flows)
5. **Create referral promotion** (landing page, social posts)

### Week 2 (Feb 10-16)
1. **Implement dashboard readiness score** (user-facing widget)
2. **Create WhatsApp group templates** (cluster communication)
3. **Partner with 2 installers** (confirmed, flyer distribution)
4. **Press release** (Badener Tagblatt submission)
5. **Review metrics, adjust marketing** (A/B test messaging)

**Target by Feb 16:** 100 registrations, 2 partnerships, press coverage initiated

---

## Metrics Dashboard (Track Weekly)

### Leading Indicators
- **Registration rate:** visitors → registrations (target: 5%+)
- **Verification rate:** registrations → email confirmed (target: 70%+)
- **Profile completion:** full energy data (target: 60%+)
- **Utility consent:** explicit sharing permission (target: 70%+)
- **Referral rate:** users who invite others (target: 15%+)

### Lagging Indicators
- **Total verified households** (target: 500 by Mar 31)
- **Communities forming** (target: 20 by May 31)
- **DSO submissions** (target: 10 by Jun 15)
- **Media mentions** (target: 5 by Jun 30)
- **Customer satisfaction** (NPS target: 50+)

### Acquisition Value Metrics
- **Cost avoidance:** RW build cost (CHF 300K+) vs. acquisition price
- **Time to market:** 6 months faster than internal build
- **Customer acquisition cost:** CHF 20-40/household vs. CHF 100+ typical
- **Verified demand:** 500+ households wanting LEG activation

---

## Acquisition Pitch Framework (Preview)

### Slide 1: The Problem
Regionalwerke Baden legally required to support LEG (Jan 1, 2026). Building platform internally: CHF 300K+, 12+ months, risky.

### Slide 2: Our Solution
BadenLEG: turnkey LEG onboarding + formation platform. 500+ verified Baden households ready to activate. 20+ communities in pipeline.

### Slide 3: Proven Demand
- 500+ registered, consented households (your customers)
- 70%+ explicit consent to share data with utility
- 20+ neighborhoods ready for activation
- 10+ DSO submissions processed

### Slide 4: Platform Capabilities
- Community formation wizard (automated)
- Document generation (contracts, DSO forms)
- Consent management (GDPR-compliant)
- Utility handoff package (CSV + PDF exports)
- Internal ops dashboard (case management)

### Slide 5: Integration Plan
- White-label (badenleg.ch → regionalwerke-baden.ch/leg)
- API integration (your CRM/billing)
- Data migration (clean, consented exports)
- Transition: 3 months with support

### Slide 6: Business Case
- **Acquisition cost:** CHF 300-400K
- **Avoided cost:** CHF 300-500K (internal build)
- **Time saved:** 12 months to market
- **Revenue potential:** CHF 50K+ ARR (servicing fees)
- **Net benefit:** CHF 0-200K cost + 12 months faster

### Slide 7: Deal Structure (Options)
A. Full acquisition (CHF 300K + earnout)
B. Exclusive license (CHF 100K + CHF 30K/year)
C. Strategic partnership (CHF 150K for 40% equity)

### Slide 8-15: Details
- Technical architecture
- Security/privacy compliance
- Customer testimonials
- Media coverage
- Roadmap (post-acquisition features)
- Team/transition plan
- References (DSO contacts, pilot users)
- Next steps

---

## Conclusion: Ruthless Focus

**Acquisition = Evidence, Not Perfection**

Every feature decision asks: "Does this prove acquisition value?"
- More verified households? ✅ Build it
- Better UX polish? ❌ Skip it
- Utility handoff package? ✅ Build it
- Mobile app? ❌ Skip it
- Formation automation? ✅ Build it
- Advanced analytics? ❌ Skip it

**6-Month Sprint:**
Feb: Demand proof (500 households)
Mar: Formation capability (20 communities)
Apr-May: Utility ops layer (handoff package)
Jun-Aug: Acquisition (close deal)

**Success = CHF 300-500K exit by August 2026**

Anything not directly supporting this goal is distraction.

---

*Last updated: Feb 2, 2026*
*Next review: Weekly (every Monday)*
