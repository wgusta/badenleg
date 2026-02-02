# Planning Complete: BadenLEG Acquisition Strategy

**Date:** February 2, 2026
**Status:** ✅ Comprehensive 6-month acquisition plan ready
**Committed:** All planning documents in git

---

## What Was Analyzed

**Strategy Documents Reviewed:**
1. `strategy.md` - Main acquisition-focused strategy (utility buyer positioning)
2. `BLITZ-STRATEGY-CORRECTED.md` - 6-month blitz timeline (Nov 2025 perspective)
3. `README.md` - Current technical state
4. `formation_wizard.py` - 670 LOC backend code (completed but not integrated)
5. `database.py` - PostgreSQL layer (completed)

**Current Situation:**
- LEG legal since Jan 1, 2026 (we're 1 month into critical window)
- Foundation infrastructure complete (PostgreSQL, referral system, GA4, consent management)
- Formation wizard coded but not integrated into UI
- Missing: growth engine, formation UI, utility ops layer, acquisition proof package

**Key Insight:** Platform has solid technical foundation but needs focused execution on acquisition proof points, not feature perfection.

---

## What Was Created

### 📋 **4 Comprehensive Planning Documents**

#### 1. **START_HERE.md** (8,500 words)
**Purpose:** Executive summary & quick orientation

**Contents:**
- TL;DR (strategy in 3 paragraphs)
- Current state audit (✅ done, ⚠️ partial, ❌ missing)
- The 4 proof points Regionalwerke needs
- Week 1 action items (start Monday)
- Resource requirements (480h, CHF 15K)
- Critical success factors (focus, speed, metrics, support, resilience)
- Risk management (triggers & responses)
- Decision framework (3 questions for any decision)
- Mental models (acquisition evidence > product perfection)
- Success visualization (what Aug 31 looks like)

**Use:** Read first (30 min) to understand entire strategy. Return to when stuck or questioning direction.

---

#### 2. **ACQUISITION_PLAN.md** (15,000 words)
**Purpose:** Strategic roadmap with business case

**Contents:**
- Acquisition thesis (what utilities buy)
- What Regionalwerke Baden values (must-haves vs. differentiators)
- Product positioning (customer experience layer, not billing replacement)
- 4-phase feature roadmap:
  - Phase 0: Acquisition hygiene (persistence, consent, admin dashboard)
  - Phase 1: Demand engine (verified households, progressive profiling)
  - Phase 2: Formation accelerator (wizard MVP, document generation)
  - Phase 3: Utility ops (console, integration surface, white-label)
  - Phase 4: Servicing modules (optional pre-acquisition)
- Evaluation of existing strategy docs (what works, what needs adjustment)
- Success metrics (demand, formation throughput, compliance, operational readiness)
- Risks & mitigations (adversarial positioning, privacy, integration scope)
- Next 30 days highest leverage actions
- Current implementation snapshot (what's done, what's needed)

**Use:** Understand WHY each feature matters for acquisition. Reference when stakeholders ask "why not build X instead?"

---

#### 3. **TECHNICAL_ROADMAP.md** (42,000 words)
**Purpose:** Detailed implementation specifications

**Contents:**

**Phase 1: Demand Proof (120h)**
- Landing page optimization (countdown, live counter, savings calculator)
- Email automation (Day 1/3/7/14 sequences, gradual data collection)
- Referral program enhancement (dashboard, QR codes, leaderboard)
- User dashboard with readiness score (progress bar, checklist, incentives)
- WhatsApp group templates (auto-generation, privacy-safe)
- Partnership materials (flyers, email templates)
- Analytics dashboard (funnel metrics, A/B testing framework)

**Phase 2: Formation Capability (160h)**
- Formation wizard UI (community creation, member invitation, status tracking)
- Document generation (3 types: community agreement, participant contracts, DSO notification)
- Signature collection (electronic signature capture, email workflows)
- Legal review (Swiss energy lawyer, template refinement)
- Pilot community activation (5 communities white-glove support)

**Phase 3: Utility Ops Layer (120h)**
- Internal admin console (pipeline view, community detail, timeline visualization)
- Audit log viewer (filters, pagination, export)
- Export controls (utility handoff CSV, community ZIP packages, GIS GeoJSON)
- Utility handoff package (field mapping, validation, PDF bundle generation)
- API endpoints (REST API, webhook support, authentication)

**Phase 4: Acquisition Approach (80h)**
- Proof package assembly (metrics dashboard, testimonials, media compilation, cost avoidance model)
- First contact (decision-maker research, outreach email, pitch deck)
- Negotiation (term sheet, valuation defense, alternative buyers)
- Due diligence & closing (data room, technical audit support, integration planning)

**Each feature includes:**
- Exact file names & code examples
- API endpoints with request/response formats
- Database schema changes
- Hour estimates per task
- Acceptance criteria
- Testing approach

**Use:** Reference when building features. Copy-paste code examples. Check acceptance criteria before marking tasks complete.

---

#### 4. **WEEK_BY_WEEK_PLAN.md** (18,000 words)
**Purpose:** Day-by-day execution timeline

**Contents:**
- 26 weeks mapped (Feb 3 - Aug 31, 2026)
- Each week shows:
  - Monday: Planning (4h)
  - Tuesday-Thursday: Building (12h)
  - Friday: Shipping & review (3h)
  - Weekend: Optional (marketing, growth)
- Specific tasks with hour estimates per day
- Weekly goals (registrations, features shipped, partnerships)
- Monthly milestones (Feb: 200 users, Mar: 500 users, etc.)
- Success metrics to track every Monday
- Risk triggers (when to pivot, when to accelerate)
- Weekly review template (what went well, what didn't, key metrics, next priorities)
- Daily habits (morning check, evening log, weekly/monthly reviews)
- Emergency contacts (technical, legal, strategic)

**Example Week (Week 1: Feb 3-9):**
- Monday: Homepage updates, live counter API
- Tuesday: Facebook ads setup & launch (CHF 500)
- Wednesday: Research solar installers, draft partnership emails
- Thursday: Send 10 installer emails, 5 cooperative emails
- Friday: Review metrics, plan Week 2
- Goal: 20 new registrations, 1-2 partnership responses

**Use:** Open every Monday morning. Follow day-by-day tasks. Update Friday with actual results. Adjust if behind/ahead of plan.

---

## The Core Strategy (In 3 Sentences)

1. **BadenLEG is not building a product company** - we're building acquisition evidence (proof that Regionalwerke Baden should buy vs. build).

2. **Focus on 4 proof points:** (1) Demand = 500+ consented households, (2) Capability = 20+ communities forming, (3) Operations = utility handoff package, (4) Pitch = cost avoidance + time savings.

3. **Timeline is aggressive but achievable:** 480 dev hours (20h/week × 24 weeks), CHF 15K budget, ruthless prioritization (say no to 90% of ideas), ship fast & iterate, close acquisition by Aug 2026 for CHF 300-500K.

---

## What NOT to Build (Critical for Success)

The plan explicitly identifies features to **SKIP** pre-acquisition:

❌ **Skip These:**
- Mobile apps (web-first sufficient)
- 15-minute billing calculator (utility has meter data)
- SEPA integration (not needed until post-DSO approval)
- Chat/messaging (WhatsApp sufficient)
- Multi-language (German only for Baden)
- Complex distribution models (simple/equal split only)
- Smart meter API integration (manual upload acceptable)
- Advanced analytics (basic metrics sufficient)
- Perfect UX/design (functional > beautiful)
- Scalability optimization (500 users != scale problem)

✅ **Focus on These:**
- Verified household count (quantity proves demand)
- Formation throughput (communities reaching "ready" state)
- Document generation (proves process automation)
- Utility handoff package (exactly what they need)
- Consent management (regulatory compliance)
- Operational dashboard (internal case handling)

**Principle:** Every feature must answer "Does this prove acquisition value?" YES = build, NO = skip.

---

## Timeline & Milestones

```
FEB 2026: Demand Engine
├─ Week 1-2: Marketing foundation (homepage, ads, emails)
├─ Week 3-4: User dashboard, partnerships, WhatsApp
└─ Goal: 200 registrations by Feb 28

MAR 2026: Growth Acceleration
├─ Week 5-6: A/B testing, analytics deep dive
├─ Week 7-8: Press coverage, testimonials, sprint finish
└─ Goal: 500 registrations by Mar 31

APR 2026: Formation Capability
├─ Week 9-10: Formation wizard UI (create, invite)
├─ Week 11-12: Document generation, signatures
└─ Goal: 10 communities forming by Apr 30

MAY 2026: Pilot & Operations
├─ Week 13-14: Pilot activation, DSO submissions
├─ Week 15-17: Legal review, admin console, exports
└─ Goal: 5 DSO submissions, 20 communities by May 31

JUN 2026: Utility Integration
├─ Week 18-19: Utility handoff package, API endpoints
├─ Week 20-21: Acquisition prep, first contact
└─ Goal: Pitch delivered, interest confirmed

JUL 2026: Negotiation
├─ Week 22-23: Pitch meeting, follow-up
├─ Week 24: Term sheet negotiation
└─ Goal: Term sheet signed, price agreed

AUG 2026: Closing
├─ Week 25: Due diligence (legal, technical, financial)
├─ Week 26: Sign contracts, receive payment, celebrate! 🎉
└─ Goal: Deal closed, CHF 300-500K received
```

---

## Resource Requirements

### Time Investment
- **480 hours total** over 6 months
- **20 hours/week** average (equivalent to 1 day/week if working another job)
- **Peak weeks:** 25-30 hours (formation wizard, acquisition prep)
- **Light weeks:** 15 hours (waiting for lawyer, due diligence)

**Feasibility Check:**
- ✅ If solo founder with flexible hours or no full-time job
- ⚠️ If working full-time job (need very flexible employer)
- ❌ If working full-time + family obligations (not enough time)

### Financial Budget
| Category | Amount | Purpose |
|----------|--------|---------|
| Marketing | CHF 5,000 | Facebook ads, partnerships, materials |
| Legal | CHF 3,000 | Contract review, term sheet, lawyer consult |
| Tools/Hosting | CHF 2,000 | SendGrid, Railway/VPS, domains, services |
| Contingency | CHF 5,000 | Unexpected costs, buffer |
| **TOTAL** | **CHF 15,000** | 6-month runway |

**ROI:** CHF 15K investment → CHF 300-500K exit = **20-33x return**

### Skills Required
**Must-Have:**
- ✅ Python/Flask (you have - code exists)
- ✅ Frontend (HTML/CSS/JS - you have)
- ✅ PostgreSQL (database layer done)
- ✅ Git/Deployment (Railway or Infomaniak)

**Nice-to-Have (can learn or outsource):**
- Marketing/ads (tutorials available, CHF 500 for VA if needed)
- Design (Canva sufficient, CHF 500 for designer if needed)
- Legal (hire lawyer for CHF 3K - mandatory)

**Most Critical Skill:**
- 🎯 **Ruthless prioritization** (say no to 90% of ideas)

---

## Risk Management Strategy

### Red Flags (Monitor Weekly)
| Week | Trigger | Response |
|------|---------|----------|
| Week 8 | <200 registrations | Pivot to direct B2B sales (license to utilities) |
| Week 12 | <300 registrations | Reduce feature scope, double marketing spend |
| Week 16 | 0 DSO submissions | Simplify formation process, offer manual support |
| Week 21 | No Regionalwerke response | Contact alternative buyers (Eniwa, Axpo, EKZ) |
| Week 24 | Negotiation stalled | Activate plan B (independent growth or alternative buyer) |

### Green Lights (Accelerate)
| Week | Trigger | Response |
|------|---------|----------|
| Week 8 | >300 registrations | Increase marketing budget by 50% |
| Week 12 | >500 registrations | Accelerate formation features, hire part-time help |
| Week 16 | >10 DSO submissions | Prepare for scale, higher valuation (CHF 500-600K) |
| Week 21 | Strong Regionalwerke interest | Negotiate hard, don't discount |
| Week 24 | Multiple buyers interested | Create auction dynamic, maximize price |

---

## Decision Framework (Use Daily)

When faced with ANY decision, ask these 3 questions:

### Question 1: Does this prove acquisition value?
**Examples:**
- More verified households? ✅ YES → Build it
- Better UX polish? ❌ NO → Skip it
- Utility handoff package? ✅ YES → Build it
- Mobile app? ❌ NO → Skip it
- Formation automation? ✅ YES → Build it
- Advanced analytics? ❌ NO → Skip it

### Question 2: Can this be done faster/simpler?
**Trade-offs:**
- MVP vs. Perfect (choose MVP)
- Manual vs. Automated (choose manual if faster initially)
- Buy vs. Build (choose buy if faster)

**Example:** Document signatures
- Perfect: DocuSign integration (5 days)
- MVP: Email + signature capture canvas (2 days)
- **Choose:** MVP (saves 3 days, works fine)

### Question 3: What's the opportunity cost?
**Ask:**
- Is there something MORE important to work on?
- Will this materially impact the 4 proof points?
- Is this "nice-to-have" or "must-have"?

**Example:** Should I refactor database code?
- Impact on proof points: None (already works)
- Opportunity cost: HIGH (could build email automation instead)
- **Answer:** No, defer until post-acquisition

---

## Success Metrics (Track Weekly)

### Leading Indicators (Every Monday)
- [ ] Total registrations (target growth: +30/week Feb-Mar)
- [ ] Verification rate (target: >70%)
- [ ] Profile completion (target: >60%)
- [ ] Utility consent rate (target: >70%)
- [ ] Referral rate (target: >15%)
- [ ] Communities forming (target: 1-2/week Apr-May)

### Lagging Indicators (Monthly)
- [ ] Total verified households (Feb: 200, Mar: 500, May: 600+)
- [ ] Communities in formation (Apr: 10, May: 20+)
- [ ] DSO submissions (May: 5+, Jun: 10+)
- [ ] Media mentions (Target: 5+ by Jun)
- [ ] Customer satisfaction NPS (Target: >50)

### Acquisition Readiness Scorecard (Jun 30)
- [ ] >500 verified Baden households
- [ ] >20 communities in formation
- [ ] >10 DSO submissions
- [ ] 70%+ utility consent rate
- [ ] Complete utility handoff package
- [ ] Internal ops dashboard functional
- [ ] Security/privacy audit passed
- [ ] Acquisition deck complete

**Target:** 15/17 boxes checked = strong acquisition position

---

## What Makes This Plan Different

### ❌ Traditional SaaS Approach
- Build perfect product (12-24 months)
- Scale to 10,000+ users
- Optimize every metric (conversion, retention, LTV)
- Monetize via subscriptions (MRR growth)
- Exit in 3-5 years (if successful)

### ✅ Acquisition-Focused Approach (This Plan)
- Build proof of concept (6 months)
- 500 users sufficient (if consented + activated)
- Optimize for acquisition value (demand proof, capability proof)
- Acquisition IS monetization (no revenue needed)
- Exit in 6 months (by design)

**Key Insight:** Utilities don't buy perfect products. They buy solutions to urgent problems with proven demand. Regionalwerke Baden's problem: LEG legal requirement + customer expectations + no internal solution. BadenLEG solves all 3.

---

## Next Steps (Start Monday, Feb 3)

### Today (Sunday evening - 1h)
1. [ ] Read `START_HERE.md` completely (30 min)
2. [ ] Skim `ACQUISITION_PLAN.md` for strategy (15 min)
3. [ ] Review `WEEK_BY_WEEK_PLAN.md` Week 1 tasks (15 min)

### Monday Morning (4h)
1. [ ] Update homepage: urgency messaging, countdown timer
2. [ ] Deploy live user counter API endpoint
3. [ ] Test on mobile + desktop browsers
4. [ ] Commit changes

### Monday Afternoon (plan week)
1. [ ] Review full Week 1 plan in WEEK_BY_WEEK_PLAN.md
2. [ ] Block calendar for development time (Tue-Thu)
3. [ ] Set up Friday 3pm recurring review
4. [ ] Create Week 1 checklist

### Tuesday (4h)
1. [ ] Set up Facebook Ads account
2. [ ] Create first ad campaign (CHF 500 budget)
3. [ ] Target: Baden homeowners, 30-70, solar/energy interests
4. [ ] Launch ads, monitor performance

### Wednesday (4h)
1. [ ] Research 10 solar installers in Baden (get emails)
2. [ ] Research 5 housing cooperatives
3. [ ] Draft partnership email template
4. [ ] Design partnership flyer concept (Canva)

### Thursday (4h)
1. [ ] Send 10 installer partnership emails
2. [ ] Send 5 cooperative partnership emails
3. [ ] Track responses in spreadsheet
4. [ ] Create referral tracking links

### Friday (3h)
1. [ ] Weekly review using template in WEEK_BY_WEEK_PLAN.md
2. [ ] Check metrics: registrations, ad performance, partnership responses
3. [ ] Celebrate wins, identify issues
4. [ ] Plan Week 2 priorities

### Week 1 Goal
- **20+ new registrations**
- **1-2 partnership responses**
- **Facebook ads running efficiently**
- **Week 2 plan ready**

---

## Emergency Support

### When Stuck on Technical Issues
1. Check `TECHNICAL_ROADMAP.md` for code examples
2. Search existing codebase (`app.py`, `database.py`, `formation_wizard.py`)
3. Railway/PostgreSQL documentation
4. Stack Overflow (specific error messages)
5. Claude/ChatGPT (paste error, ask for solution)

### When Stuck on Strategic Decisions
1. Re-read decision framework in `START_HERE.md`
2. Ask: "Does this prove acquisition value?"
3. Check `ACQUISITION_PLAN.md` for rationale
4. Bias toward simpler/faster (MVP > perfect)
5. When in doubt: ship it, iterate later

### When Behind Schedule
1. Review `WEEK_BY_WEEK_PLAN.md` for current week
2. Identify what's blocking (time, skills, dependencies)
3. Simplify scope (cut features, not proof points)
4. Ask for help (hire VA, designer, or consultant for CHF 500-1000)
5. Adjust timeline (better late than never)

### When Losing Motivation
1. Re-read success visualization in `START_HERE.md`
2. CHF 300-500K in 6 months = worth the push
3. Calculate hourly rate: CHF 400K / 480h = CHF 833/hour
4. Take a break (1-2 days), then resume
5. Talk to advisor/friend who believes in you

---

## Final Reminders

### ✅ Do This
- **Focus ruthlessly** (acquisition value only)
- **Ship weekly** (done > perfect)
- **Track metrics** (every Monday)
- **Say no often** (90% of ideas are distraction)
- **Ask for help** (lawyer, advisor, VA when needed)
- **Trust the plan** (it's comprehensive, just execute)

### ❌ Don't Do This
- **Feature creep** (mobile app, advanced analytics, billing calculator)
- **Perfectionism** (good enough IS good enough)
- **Analysis paralysis** (re-planning instead of executing)
- **Ignoring metrics** (if <200 users Week 8, pivot immediately)
- **Burning out** (take breaks, this is a sprint)
- **Deviating from plan** (unless metrics say pivot)

---

## Success Definition

**August 31, 2026:**

✅ **Deal closed** with Regionalwerke Baden
✅ **CHF 300,000+** upfront payment received
✅ **CHF 100,000** earnout secured (pays in 12 months if retention >80%)
✅ **Transition started** (3-6 months consulting at CHF 10-20K)

**Total value:** CHF 400-520K over 12-18 months
**Time invested:** 480 hours (6 months × 20h/week)
**Effective hourly rate:** CHF 833-1083/hour

**What you achieved:**
- Proved demand (500+ verified, consented households)
- Proved capability (20+ communities formed)
- Proved operational readiness (utility handoff package)
- Negotiated successfully (strong proof = strong price)

**What's next:**
- Take earned break (2-4 weeks)
- Decide: repeat in another canton? Build something new? Invest earnings?
- You have capital, experience, network, options

**This is achievable. The plan is sound. Start Monday. Execute. Win.**

---

*Planning complete: February 2, 2026*
*Execution begins: Monday, February 3, 2026*
*Target close: August 31, 2026*

**LET'S GO! 🚀**
