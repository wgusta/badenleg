# START HERE: BadenLEG Acquisition Strategy
**Date:** Feb 2, 2026
**Timeline:** 6 months (Feb-Aug 2026)
**Goal:** Regionalwerke Baden acquisition for CHF 300-500K

---

## TL;DR

**Situation:** LEG legal since Jan 1, 2026. Platform has foundation (PostgreSQL, referrals, GA4, formation wizard code) but needs proof points Regionalwerke Baden will buy.

**Strategy:** Build acquisition evidence in 6 months:
1. **Feb-Mar:** Prove demand (500+ consented households)
2. **Apr-May:** Prove capability (20+ communities forming)
3. **May-Jun:** Prove operational readiness (utility handoff package)
4. **Jun-Aug:** Negotiate & close acquisition

**Required:** 480 dev hours (20h/week), CHF 10-15K budget, ruthless focus

---

## The 3 Core Documents

### 1. **ACQUISITION_PLAN.md**
Strategic overview:
- Why Regionalwerke will buy (4 proof points)
- 4-phase roadmap with features prioritized by acquisition value
- What NOT to build (skip perfection, build evidence)
- Success metrics & risk mitigation
- Acquisition pitch framework

**Read this for:** Big picture strategy, why we're building each feature

### 2. **TECHNICAL_ROADMAP.md**
Detailed implementation:
- Phase-by-phase breakdown (Feb→Mar→Apr→May→Jun→Aug)
- Exact features with code examples
- File names, API endpoints, database schemas
- Hour estimates per task
- Acceptance criteria

**Read this for:** What to build, how to build it, technical specs

### 3. **WEEK_BY_WEEK_PLAN.md**
Execution timeline:
- 26 weeks of day-by-day tasks
- Monday: Planning, Tuesday-Thursday: Building, Friday: Shipping
- Weekly metrics to track
- Risk triggers & adjustments
- Daily habits & review templates

**Read this for:** What to do this week, today, right now

---

## Current State (Feb 2, 2026)

### ✅ **Done (Phase 0)**
- PostgreSQL database layer
- Referral system with tracking
- Google Analytics 4 integration
- Formation wizard module (670 LOC Python)
- Consent capture (utility handoff + neighbor sharing)
- Audit logging
- Admin endpoints (token-protected)
- Security hardening

### ⚠️ **Partially Done**
- Admin dashboard (basic, needs enhancement)
- Email automation (SendGrid configured, limited flows)
- Formation wizard (backend done, UI not integrated)

### ❌ **Missing (Critical for Acquisition)**
- Formation wizard UI (community creation, invites, signatures)
- Utility handoff package (PDF bundle, CSV exports)
- Internal ops dashboard (case management, pipeline view)
- Document generation (contracts, DSO forms)
- User dashboard (readiness score, next steps)
- Growth engine (email nurture, A/B tests, referral push)

---

## The 4 Proof Points Regionalwerke Needs

### 1. **Demand Proof**
**Goal:** 500+ verified households with explicit utility consent
**Timeline:** Feb-Mar 2026 (8 weeks)
**How:**
- Marketing blitz (Facebook ads, CHF 3K)
- Partnership outreach (10 solar installers)
- Email automation (Day 1, 3, 7, 14 sequences)
- Referral program push (CHF 50 credits)
- Press coverage (Badener Tagblatt)

**Success Metric:** 70%+ utility consent rate, 20+ neighborhoods covered

### 2. **Formation Capability**
**Goal:** 20+ communities reach "handoff-ready" state
**Timeline:** Apr-May 2026 (8 weeks)
**How:**
- Formation wizard UI (create, invite, documents, signatures)
- Document generation (community agreement, contracts, DSO forms)
- Pilot with 5 communities (white-glove support)
- 10+ DSO submissions to Regionalwerke

**Success Metric:** <3 weeks average formation time, 100% signature collection rate

### 3. **Operational Readiness**
**Goal:** Prove platform can handle utility-scale operations
**Timeline:** May-Jun 2026 (6 weeks)
**How:**
- Internal admin console (pipeline view, case management)
- Utility handoff package (PDF bundle + CSV with all required fields)
- API endpoints (programmatic access for utility)
- Audit log (full compliance trail)

**Success Metric:** Complete export package for 20+ communities, API documented

### 4. **Acquisition Pitch**
**Goal:** Close deal with Regionalwerke Baden
**Timeline:** Jun-Aug 2026 (10 weeks)
**How:**
- Proof package (metrics dashboard, testimonials, media coverage)
- Cost avoidance analysis (CHF 300K build cost vs. CHF 400K acquisition)
- First contact (email + pitch deck)
- Negotiation (term sheet, due diligence, closing)

**Success Metric:** CHF 300-500K acquisition by Aug 31, 2026

---

## What Makes This Different

### ❌ **Traditional SaaS Playbook:**
- Build perfect product
- Optimize every feature
- Scale to 10,000+ users
- Monetize via subscriptions
- Exit in 3-5 years

### ✅ **Acquisition-Focused Playbook:**
- Build proof of concept
- Ship fast, iterate
- 500 users sufficient (if consented + activated)
- Revenue optional (acquisition is monetization)
- Exit in 6 months

**Key Insight:** Utilities don't buy perfect products. They buy solutions to urgent problems with proven demand.

Regionalwerke Baden's problem:
- LEG legal requirement (since Jan 1, 2026)
- Customer expectations (households want LEG)
- No internal solution (would take 12+ months, CHF 300K+)
- BadenLEG solves all 3 (ready now, proven demand, CHF 400K)

---

## Resource Requirements

### Time
- **480 hours total** over 6 months
- **20 hours/week** average
- **Peak weeks:** 25-30 hours (formation wizard, acquisition prep)
- **Light weeks:** 15 hours (waiting for lawyer, due diligence)

**Feasible if:** No other full-time job OR very flexible hours

### Money
- **Marketing:** CHF 5K (Facebook ads, partnerships)
- **Legal:** CHF 3K (contract review, term sheet)
- **Tools/Hosting:** CHF 2K (SendGrid, Railway/VPS, domains)
- **Contingency:** CHF 5K (unexpected costs)
- **Total:** CHF 15K

**Feasible if:** You have runway for 6 months

### Skills
**Must-have:**
- Python/Flask (you have this - code exists)
- Frontend (HTML/CSS/JS with Tailwind - you have this)
- PostgreSQL (database layer done)
- Git/deployment (Railway or Infomaniak)

**Nice-to-have:**
- Marketing (can learn or outsource)
- Design (Canva/Figma sufficient)
- Legal (hire lawyer for CHF 3K)

**Biggest skill:** Ruthless prioritization (say no to 90% of ideas)

---

## Critical Success Factors

### 1. **Focus**
Every feature decision asks: **"Does this prove acquisition value?"**
- More verified households? ✅ Build it
- Better UX polish? ❌ Skip it (for now)
- Utility handoff package? ✅ Build it
- Mobile app? ❌ Skip it (web sufficient)
- Formation automation? ✅ Build it
- Advanced analytics? ❌ Skip it (basic metrics sufficient)

**Rule:** If it doesn't directly support acquisition, it's distraction.

### 2. **Speed**
Ship every week. Minimum viable features. Iterate based on feedback.

**Bad:**
- Spend 4 weeks perfecting formation wizard UI
- Launch when "perfect"
- No user feedback until complete

**Good:**
- Ship basic form in Week 1 (ugly but works)
- Get pilot users to test Week 2
- Fix bugs & iterate Week 3-4
- Feature complete by Week 4

**Mantra:** "Done is better than perfect"

### 3. **Metrics**
Track weekly. Adjust quickly. Kill what doesn't work.

**Every Monday morning:**
- Total registrations (target growth: +30/week in Feb-Mar)
- Verification rate (target: >70%)
- Utility consent rate (target: >70%)
- Communities forming (target: 1-2/week in Apr-May)

**If behind target:** Adjust immediately (more marketing, fix funnel, simplify UX)

### 4. **Support**
Don't do everything alone.

**Get help for:**
- Legal review (hire lawyer, CHF 2-3K)
- Document design (hire designer if needed, CHF 500)
- Partnership outreach (VA for email follow-ups, optional)
- Pitch practice (advisor, friend, mentor)

**Your unique value:** Technical execution + strategic vision

### 5. **Resilience**
Setbacks will happen:
- Marketing doesn't convert → Try new channels
- Formation wizard confusing → Simplify UX
- Regionalwerke ignores email → Contact Eniwa
- Negotiation stalls → Activate plan B

**Success = persistence + adaptability**

---

## Week 1 Action Items (Feb 3-9)

Start here on Monday:

### Monday (4h)
- [ ] Read all 3 planning docs (ACQUISITION_PLAN, TECHNICAL_ROADMAP, WEEK_BY_WEEK_PLAN)
- [ ] Set up weekly review ritual (every Friday 3pm)
- [ ] Update homepage with urgency messaging
- [ ] Deploy live user counter API

### Tuesday (4h)
- [ ] Set up Facebook Ads account
- [ ] Create first ad campaign (CHF 500 budget)
- [ ] Target: Baden homeowners, age 30-70

### Wednesday (4h)
- [ ] Research 10 solar installers in Baden
- [ ] Draft partnership email template
- [ ] Prepare partnership flyer concept

### Thursday (4h)
- [ ] Send 10 installer partnership emails
- [ ] Send 5 housing cooperative emails
- [ ] Track responses

### Friday (3h)
- [ ] Weekly review (use template in WEEK_BY_WEEK_PLAN)
- [ ] Check metrics (registrations, ads performance)
- [ ] Plan Week 2

**Week 1 Goal:** 20 new registrations, 1-2 partnership responses

---

## Monthly Milestones

### February: Demand Engine
- [ ] Feb 28: 200+ registrations
- [ ] Email automation live (4 sequences)
- [ ] 2+ partnerships active
- [ ] User dashboard with readiness score

### March: Growth Acceleration
- [ ] Mar 31: 500+ registrations
- [ ] 70%+ utility consent rate
- [ ] Press mention (Badener Tagblatt)
- [ ] A/B testing showing 5-10% conversion improvements

### April: Formation UI
- [ ] Apr 30: 10+ communities forming
- [ ] Formation wizard UI complete
- [ ] Document generation working (3 types)
- [ ] 5 pilot communities started

### May: Documents & Operations
- [ ] May 31: 5+ DSO submissions
- [ ] Legal review complete (lawyer sign-off)
- [ ] Admin console deployed
- [ ] Utility handoff package defined

### June: Utility Integration
- [ ] Jun 30: Pitch delivered to Regionalwerke Baden
- [ ] API endpoints functional
- [ ] Proof package complete (metrics, testimonials, media)
- [ ] Integration guide written

### July: Negotiation
- [ ] Jul 31: Term sheet signed
- [ ] Valuation agreed (target: CHF 300-400K + earnout)
- [ ] Due diligence started

### August: Closing
- [ ] Aug 31: Deal closed! 🎉
- [ ] Payment received
- [ ] Transition begun

---

## Risk Management

### High-Risk Scenarios

**Risk 1: Not enough registrations**
- **Kill criteria:** <200 by Mar 15
- **Mitigation:** Front-load marketing (CHF 3K in Feb-Mar), aggressive partnerships
- **Plan B:** Pivot to direct B2B sales (license to multiple utilities)

**Risk 2: Formation process too complex**
- **Kill criteria:** <50% completion rate in pilot
- **Mitigation:** Simplify UX, manual fallback, white-glove support
- **Plan B:** Offer formation as service (charge CHF 199/household)

**Risk 3: Regionalwerke ignores outreach**
- **Kill criteria:** No response after 3 follow-ups
- **Mitigation:** PR pressure (media creates urgency), alternative contacts
- **Plan B:** Eniwa, Axpo, EKZ (other utilities)

**Risk 4: Valuation gap (they offer CHF 100K)**
- **Kill criteria:** Below CHF 200K walk-away price
- **Mitigation:** Show alternative buyer interest, emphasize cost avoidance
- **Plan B:** Continue independent, grow to 2000+ users, sell in 2027

### Green Light Scenarios

**Scenario 1: >500 registrations by Mar 31**
- **Action:** Increase marketing budget, accelerate formation features

**Scenario 2: >20 communities forming by May 31**
- **Action:** Prepare for scale, higher valuation (CHF 500-600K)

**Scenario 3: Multiple utilities interested**
- **Action:** Create auction dynamic, negotiate aggressively

**Scenario 4: Regionalwerke proposes partnership instead**
- **Action:** Evaluate carefully (CHF 150K for 40% equity = CHF 375K valuation)

---

## Decision Framework

When faced with any decision, ask these 3 questions:

### 1. **Does this prove acquisition value?**
- YES → Prioritize
- NO → Defer or skip

### 2. **Can this be done faster/simpler?**
- MVP version vs. perfect version
- Manual vs. automated (manual is faster initially)
- Buy vs. build (buy if faster)

### 3. **What's the opportunity cost?**
- Is there something more important to work on?
- Will this materially impact the 4 proof points?
- Is this a "nice-to-have" or "must-have"?

**Example:**
- **Decision:** Should I build a mobile app?
- **Q1:** Does this prove acquisition value? NO (web works fine)
- **Q2:** Can this be done faster? N/A
- **Q3:** Opportunity cost? HIGH (would take 40+ hours)
- **Answer:** Skip it

**Example:**
- **Decision:** Should I build email automation?
- **Q1:** Does this prove acquisition value? YES (increases registrations)
- **Q2:** Can this be done faster? YES (simple triggers, basic templates)
- **Q3:** Opportunity cost? LOW (16h for high-ROI feature)
- **Answer:** Build it

---

## Mental Models

### Model 1: Acquisition Evidence Builder
You're not building a product company. You're building acquisition evidence.

**Product Company:**
- Focus: Perfect UX, scalability, retention
- Timeline: 3-5 years to exit
- Users: 10,000+
- Metrics: MRR, churn, LTV/CAC

**Acquisition Evidence:**
- Focus: Proof points that reduce buyer risk
- Timeline: 6 months to exit
- Users: 500+ (sufficient if consented)
- Metrics: Consent rate, formation throughput, utility readiness

**Implication:** Features that don't prove acquisition value are waste.

### Model 2: Regulatory Arbitrage
Utilities are slow. You're fast.

**LEG legal:** Jan 1, 2026 (6 weeks ago)
**Utility response:** 3-6 months (March-June 2026)
**Your window:** NOW to June 2026

**Strategy:** Move so fast they can't ignore you.
- 500 households registered → They have to respond
- 20 DSO submissions → They can't process without you
- PR coverage → Customers expect utility to offer LEG

**Pressure Point:** "You're legally required to offer LEG. We've built the solution. Acquire or build (12 months, CHF 300K+)."

### Model 3: Proof Over Perfection
Good enough is good enough.

**Perfect formation wizard:**
- Beautiful UI, animations, mobile app
- Complex workflows, edge cases handled
- 6 months to build

**Good enough formation wizard:**
- Basic forms, works on desktop + mobile web
- Happy path only, manual fallback for edge cases
- 4 weeks to build

**Result:** 5 months saved, acquisition happens earlier

**Lesson:** Optimize for "does it work?" not "is it beautiful?"

---

## Success Visualization

**August 31, 2026:**

You receive CHF 300,000 in your bank account.

Regionalwerke Baden owns BadenLEG. They're integrating it into their systems. You're providing 3 months of transition support (CHF 20K additional).

Earnout of CHF 100K kicks in after 12 months if retention >80% (likely).

**Total:** CHF 420K in 6 months from now.

**What you did:**
- Built proof of demand (500+ households)
- Built proof of capability (20+ communities)
- Built proof of operational readiness (utility handoff)
- Pitched convincingly (cost avoidance + time savings)
- Negotiated successfully (CHF 300K + earnout)

**What you didn't do:**
- Perfect every feature
- Scale to 10,000 users
- Build mobile app
- Implement 15-minute billing
- Raise VC funding

**Why it worked:**
- Focused on acquisition from day 1
- Shipped fast, iterated quickly
- Said no to 90% of ideas
- Proved value at every phase
- Negotiated from strength

**Now:** You have capital, experience, and options.

**Next:** Repeat in another canton? Build something new? Take a break? Your choice.

---

## Final Checklist

Before you start, confirm:

- [ ] I have 20 hours/week for 6 months (120h/month)
- [ ] I have CHF 15K budget (or can fundraise it)
- [ ] I have technical skills (Python, web development)
- [ ] I'm willing to focus ruthlessly (say no to distractions)
- [ ] I understand this is a sprint, not a marathon
- [ ] I have support (advisor, lawyer, friend who believes in me)
- [ ] I'm ready to start Monday (Feb 3, 2026)

**If all checked: Start Monday. Execute plan. Close by August.**

---

## Quick Reference

**Planning Docs:**
- `ACQUISITION_PLAN.md` - Strategy & why
- `TECHNICAL_ROADMAP.md` - What & how
- `WEEK_BY_WEEK_PLAN.md` - When & execution

**Current Status:**
- `README.md` - Technical overview
- `strategy.md` - Original acquisition strategy
- `formation_wizard.py` - Coded but not integrated
- `database.py` - PostgreSQL layer (done)

**Weekly Review:**
- Every Friday 3pm
- Template in `WEEK_BY_WEEK_PLAN.md`
- Track metrics, adjust plan

**Support:**
- Legal: [Hire lawyer Week 15]
- Technical: Railway support, PostgreSQL docs
- Strategic: [Your advisors]

---

## Get Started

**Right now:**
1. Read `ACQUISITION_PLAN.md` (30 min)
2. Skim `TECHNICAL_ROADMAP.md` (20 min)
3. Review `WEEK_BY_WEEK_PLAN.md` Week 1 (10 min)

**Monday:**
1. Start Week 1 tasks
2. Update homepage with urgency
3. Launch Facebook ads

**This week:**
1. Complete Week 1 checklist
2. Get 20 new registrations
3. Send partnership emails

**This month:**
1. Hit 200 registrations by Feb 28
2. Email automation live
3. 2+ partnerships active

**6 months from now:**
1. Deal closed
2. CHF 300K+ in bank
3. Celebrate! 🎉

---

**You can do this.**

**The plan is clear. The path is defined. The prize is worth it.**

**Start Monday. Execute ruthlessly. Close by August.**

**Let's go.**

---

*Last updated: Feb 2, 2026*
*Next review: Every Friday at 3pm*
*Questions? Re-read the plan. Answer is there.*
