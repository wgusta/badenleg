# BadenLEG: Week-by-Week Execution Plan
**Period:** Feb 3 - Aug 31, 2026 (26 weeks)
**Goal:** Regionalwerke Baden acquisition by Aug 2026

---

## FEBRUARY 2026: Demand Engine

### Week 1 (Feb 3-9): Launch Preparation
**Focus:** Get growth infrastructure running

**MON (4h):**
- Update homepage: urgency messaging, countdown timer
- Deploy live user counter API endpoint
- Test on mobile + desktop

**TUE (4h):**
- Set up Facebook Ads account
- Create first ad campaign (CHF 500 budget)
- Target: Baden homeowners, age 30-70, interests: solar/energy/sustainability

**WED (4h):**
- Draft partnership email template
- Research 10 solar installers in Baden (get contact emails)
- Research 5 housing cooperatives

**THU (4h):**
- Send 10 installer partnership emails
- Send 5 cooperative partnership emails
- Create partnership flyer PDF (simple design)

**FRI (3h):**
- Review week metrics
- Adjust homepage based on analytics
- Plan week 2

**WEEKEND:**
- Monitor Facebook ads
- Respond to partnership inquiries

**GOAL:** 20 new registrations, 1-2 partnership responses

---

### Week 2 (Feb 10-16): Email Automation
**Focus:** Build nurture sequences

**MON (5h):**
- Create `email_automation.py` module
- Write Day 1 welcome email template
- Write Day 3 smart meter email template

**TUE (5h):**
- Write Day 7 consumption data email
- Write Day 14 formation readiness email
- Set up cron job (every 6 hours)

**WED (4h):**
- Test email sequences with 3 test accounts
- Fix bugs, adjust timing
- Deploy to production

**THU (3h):**
- Create referral dashboard page
- Add referral link copy button
- Generate QR codes for users

**FRI (3h):**
- Review week metrics
- Respond to user questions
- Plan week 3

**GOAL:** Email automation live, referral system enhanced, 50 total registrations

---

### Week 3 (Feb 17-23): User Dashboard
**Focus:** Build readiness score widget

**MON (5h):**
- Design dashboard layout (HTML/CSS)
- Create readiness score calculation function
- Add to database queries

**TUE (5h):**
- Build progress bar component
- Add checklist (email verified, profile complete, etc.)
- Show incentives (CHF 50 discount at 100%)

**WED (4h):**
- Integrate savings estimate display
- Show neighbor matches on mini-map
- Add "invite more neighbors" button

**THU (3h):**
- Add inline data collection forms (AJAX)
- Energy profile form
- Smart meter ID field

**FRI (3h):**
- Test dashboard on mobile
- Fix bugs
- Deploy

**GOAL:** User dashboard live, 100 total registrations

---

### Week 4 (Feb 24 - Mar 2): WhatsApp & Partnerships
**Focus:** Social lock-in mechanisms

**MON (4h):**
- Create WhatsApp group templates
- Auto-generation function for cluster groups
- Test with 1-2 pilot clusters

**TUE (4h):**
- Build admin interface for WhatsApp group creation
- Track group status in database
- Email invites with WhatsApp links

**WED (4h):**
- Design homeowner flyer (Canva/Figma)
- Export to PDF
- Make downloadable for partners

**THU (4h):**
- Follow up with installer partnerships
- Send flyers to confirmed partners
- Create tracking links (UTM parameters)

**FRI (4h):**
- Review month metrics
- Analyze funnel (visitor → registration → verified)
- Identify bottlenecks

**GOAL:** 150 total registrations, 2+ active partnerships

---

## MARCH 2026: Growth & Optimization

### Week 5 (Mar 3-9): A/B Testing
**Focus:** Optimize conversion rates

**MON (4h):**
- Set up A/B testing framework
- Create variant A/B for homepage headline
- Deploy with 50/50 split

**TUE (4h):**
- Test CTA button variants (color, text)
- Test social proof messaging
- Track conversions

**WED (4h):**
- Analyze first results (minimum 100 visitors per variant)
- Deploy winner if statistically significant
- Start next test

**THU (4h):**
- Re-engagement email campaign
- Target: registered but not verified (Day 3 trigger)
- Test 2 subject line variants

**FRI (4h):**
- Abandoned cart email campaign
- Target: verified but profile <60% complete
- Test messaging

**GOAL:** 5-10% conversion rate improvement, 250 total registrations

---

### Week 6 (Mar 10-16): Analytics Deep Dive
**Focus:** Build acquisition metrics dashboard

**MON (5h):**
- Create admin analytics page
- Funnel visualization (Plotly/Chart.js)
- Growth trend line (daily registrations)

**TUE (5h):**
- Add geographic heatmap (clusters by neighborhood)
- Calculate acquisition readiness metrics
- Track consent rates

**WED (4h):**
- Build export functionality (CSV/PDF)
- Weekly report auto-generation
- Email to self every Monday

**THU (3h):**
- Review all metrics
- Identify weak points
- Plan optimization

**FRI (3h):**
- Adjust marketing spend based on CAC
- Increase budget if CAC < CHF 40
- Pause underperforming channels

**GOAL:** Clear visibility on all metrics, 350 total registrations

---

### Week 7 (Mar 17-23): Press & Content
**Focus:** Build credibility

**MON (4h):**
- Write press release ("BadenLEG enables LEG from day 1")
- Submit to Badener Tagblatt
- Contact 3 regional journalists

**TUE (4h):**
- Create "About Us" page (if missing)
- Add team bios, mission, story
- Build trust

**WED (4h):**
- Film user testimonial videos (Zoom calls)
- Ask 3-5 most engaged users
- Edit basic cuts

**THU (4h):**
- Write 3 blog posts:
  - "How to Form a LEG in Baden" (SEO)
  - "LEG vs. ZEV: What's the Difference?" (Education)
  - "5 Households Share Their LEG Journey" (Social proof)

**FRI (4h):**
- Publish blog posts
- Share on social media
- Monitor press response

**GOAL:** 1+ press mention, 450 total registrations

---

### Week 8 (Mar 24-30): March Sprint Finish
**Focus:** Hit 500 registration target

**MON (4h):**
- Analyze what's working (highest ROI channels)
- Double down on winners
- Pause losers

**TUE (4h):**
- Street-level targeting (Facebook ads)
- Target specific streets with 2-3 registrations
- "Your neighbors on Musterstrasse are forming LEG"

**WED (4h):**
- Email all registered users: "Refer a neighbor, get CHF 50"
- Leaderboard announcement
- FOMO tactics ("Only X spots left in your cluster")

**THU (4h):**
- Partnership push: contact 5 more installers
- Offer better terms (higher commission?)
- Get flyers distributed

**FRI (4h):**
- Final March push (social media blitz)
- Review month performance
- Celebrate if hit 500!

**GOAL:** 500 total registrations (stretch: 600)

---

## APRIL 2026: Formation Capability

### Week 9 (Mar 31 - Apr 6): Formation Wizard UI (Part 1)
**Focus:** Community creation flow

**MON (6h):**
- Design community creation form (HTML)
- Name, description, distribution model
- Integrate with formation_wizard.py backend

**TUE (6h):**
- Build community creation API endpoint
- Validation logic
- Error handling

**WED (4h):**
- Test community creation
- Fix bugs
- Deploy

**THU (2h):**
- User documentation (how to create community)
- FAQ updates

**FRI (2h):**
- Monitor first community creations
- Support users via email

**GOAL:** Community creation live, 1-2 communities created

---

### Week 10 (Apr 7-13): Formation Wizard UI (Part 2)
**Focus:** Member invitation system

**MON (6h):**
- Build invitation UI (suggested neighbors)
- List registered users within radius
- "Invite" button functionality

**TUE (6h):**
- Email invitation system (registered users)
- Email invitation for unregistered users
- Track invitation status

**WED (4h):**
- Confirmation flow (accept/decline invitation)
- Update member status in database
- Notify admin of confirmations

**THU (2h):**
- WhatsApp invite integration
- Share link to WhatsApp groups
- QR code generation

**FRI (2h):**
- Test full invitation flow
- Fix bugs

**GOAL:** Invitation system working, 5+ communities with invitations sent

---

### Week 11 (Apr 14-20): Document Generation (Part 1)
**Focus:** PDF templates

**MON (6h):**
- Install WeasyPrint/ReportLab
- Create HTML template: community agreement
- Test PDF generation

**TUE (6h):**
- Create HTML template: participant contracts
- Create HTML template: DSO notification
- Ensure legal language correct (from strategy docs)

**WED (4h):**
- Test all 3 document types
- Verify PDF formatting (margins, fonts, pages)
- Fix rendering issues

**THU (2h):**
- Create document storage system
- Encryption at rest
- Version tracking

**FRI (2h):**
- Integration test: create community → generate docs
- Verify documents accessible

**GOAL:** Document generation working, 3 PDF types

---

### Week 12 (Apr 21-27): Document Generation (Part 2)
**Focus:** Signature collection

**MON (6h):**
- Build signature capture page (HTML canvas)
- Signature pad library integration
- Test on mobile + desktop

**TUE (6h):**
- Signature submission API
- Store signatures in database
- Link to documents

**WED (4h):**
- Email signature requests to members
- Unique token per member per document
- Track completion status

**THU (2h):**
- Build admin view: signature progress
- Show which members signed, which pending
- Reminder functionality

**FRI (2h):**
- Test full signature flow
- Fix bugs

**GOAL:** Signature system working, ready for pilot

---

## MAY 2026: Pilot Communities & Ops Layer

### Week 13 (Apr 28 - May 4): Pilot Activation
**Focus:** Get 5 communities through formation

**MON (4h):**
- Select 5 pilot communities (handpick engaged users)
- Email kickoff invitations
- Schedule kickoff calls (30 min each)

**TUE (4h):**
- Conduct 5 kickoff calls
- Walk through formation wizard
- Answer questions

**WED (4h):**
- Monitor pilot progress
- Troubleshoot technical issues
- Provide white-glove support

**THU (4h):**
- Help collect signatures
- Follow up with slow responders
- Encourage completion

**FRI (4h):**
- Review pilot progress
- Document feedback
- Plan improvements

**GOAL:** 5 communities complete formation wizard

---

### Week 14 (May 5-11): DSO Submissions
**Focus:** Submit to Regionalwerke Baden

**MON (4h):**
- Generate final documents for 5 communities
- Review for completeness
- Get admin sign-off

**TUE (4h):**
- Prepare DSO submission packages
- Cover letters
- Mailing labels (registered mail)

**WED (4h):**
- Submit 5 DSO notifications
- Track submission (email + registered mail)
- Record submission dates

**THU (4h):**
- Follow up with DSO team (informal)
- Ask about processing time
- Note any requested changes

**FRI (4h):**
- Document submission process
- Note improvements needed
- Write post-mortem

**GOAL:** 5 DSO submissions completed, process documented

---

### Week 15 (May 12-18): Legal Review
**Focus:** Get lawyer sign-off on templates

**MON (4h):**
- Research Swiss energy lawyers
- Request quotes (3 lawyers)
- Select one (budget: CHF 2000)

**TUE (4h):**
- Send all document templates to lawyer
- Provide context (StromVG Art. 17a, Aargau)
- Request review

**WED-FRI (12h buffer):**
- Wait for lawyer feedback
- Meanwhile: work on admin console (next task)
- Respond to lawyer questions

**GOAL:** Lawyer engaged, review in progress

---

### Week 16 (May 19-25): Admin Console (Part 1)
**Focus:** Pipeline dashboard

**MON (6h):**
- Design admin console layout
- Pipeline stages visualization
- Key metrics cards

**TUE (6h):**
- Build community list view
- Filters (status, neighborhood, search)
- Sortable table

**WED (4h):**
- Build community detail view
- Timeline visualization
- Member list

**THU (2h):**
- Internal notes functionality
- Add/view notes per community

**FRI (2h):**
- Test admin console
- Deploy behind admin token

**GOAL:** Admin console MVP live

---

### Week 17 (May 26 - Jun 1): Admin Console (Part 2)
**Focus:** Audit log & exports

**MON (5h):**
- Build audit log viewer
- Filters (date, event type, user)
- Pagination (50 events/page)

**TUE (5h):**
- CSV export functionality
- Utility handoff export format
- Filter to consented users only

**WED (5h):**
- PDF bundle generation (per community)
- ZIP package creation
- Document storage organization

**THU (3h):**
- Test all export formats
- Verify data completeness
- Check for PII leaks

**FRI (2h):**
- Deploy export features
- Update admin documentation

**GOAL:** Full export capability ready

---

## JUNE 2026: Utility Integration & Outreach

### Week 18 (Jun 2-8): Utility Handoff Package
**Focus:** Define exact format Regionalwerke needs

**MON (4h):**
- Research Regionalwerke DSO requirements
- Check existing forms/APIs
- Document required fields

**TUE (4h):**
- Build validation rules (meter ID format, etc.)
- Test with sample data
- Ensure consent check mandatory

**WED (4h):**
- Create utility handoff PDF template
- Cover page with summary
- Member data sheets

**THU (4h):**
- Test PDF generation
- Review formatting
- Get feedback from pilot users

**FRI (4h):**
- Finalize utility package format
- Document field specifications
- Prepare for demo

**GOAL:** Utility handoff package ready, validated

---

### Week 19 (Jun 9-15): API Endpoints
**Focus:** Programmatic access for utility

**MON (5h):**
- Design REST API structure
- Endpoints: list communities, detail, documents
- Authentication (API key)

**TUE (5h):**
- Implement API endpoints
- Rate limiting (100 req/hour)
- Error handling

**WED (5h):**
- Webhook support (status updates from utility)
- Test bidirectional flow
- Log all API access

**THU (3h):**
- Write API documentation
- Examples (curl, Python)
- Integration guide

**FRI (2h):**
- Deploy API endpoints
- Test with Postman
- Share docs with test partner (if available)

**GOAL:** API ready for utility integration

---

### Week 20 (Jun 16-22): Acquisition Prep
**Focus:** Build proof package

**MON (5h):**
- Generate acquisition metrics dashboard
- All key metrics auto-updating
- Export to PDF/slides

**TUE (5h):**
- Collect customer testimonials
- 5-10 video interviews (Zoom)
- Basic editing

**WED (5h):**
- Compile media coverage
- Create "Press Kit" page
- Screenshot all mentions

**THU (3h):**
- Build cost avoidance financial model
- Regionalwerke build cost vs. acquisition
- Create comparison chart

**FRI (2h):**
- Review all proof materials
- Ensure data accuracy
- Package for pitch

**GOAL:** Complete proof package ready

---

### Week 21 (Jun 23-29): First Contact
**Focus:** Reach out to Regionalwerke Baden

**MON (4h):**
- Research decision-makers
- LinkedIn, org chart, press releases
- Identify 2-3 contacts

**TUE (4h):**
- Draft outreach email
- Refine messaging
- Get feedback from advisors

**WED (2h):**
- Send outreach email to primary contact
- CC secondary if appropriate
- Track email opens (if tool available)

**THU (4h):**
- Create 15-slide pitch deck
- Follow framework from ACQUISITION_PLAN.md
- Professional design

**FRI (4h):**
- Practice pitch (record yourself)
- Refine based on feedback
- Prepare for meeting

**SAT-SUN:**
- Monitor email response
- Prepare to follow up

**GOAL:** Outreach sent, pitch deck ready

---

## JULY 2026: Negotiation

### Week 22 (Jun 30 - Jul 6): Meeting Preparation
**Focus:** Get ready for first meeting

**MON (4h):**
- Follow up if no response (Day 3)
- LinkedIn connection
- Alternative contact attempt

**TUE (4h):**
- Prepare demo environment
- Clean data (remove test entries)
- Test all features

**WED (4h):**
- Prepare answers to likely questions
- Valuation defense
- Objection handling

**THU (4h):**
- Mock pitch with friend/advisor
- Time it (30 minutes)
- Refine based on feedback

**FRI (4h):**
- Final pitch preparation
- Print materials (if in-person)
- Confirm meeting logistics

**GOAL:** Fully prepared for pitch meeting

---

### Week 23 (Jul 7-13): Pitch & Follow-up
**Focus:** Deliver pitch, gauge interest

**MON-WED (varies):**
- Deliver pitch meeting (target: this week)
- Answer questions
- Demonstrate platform

**THU (4h):**
- Send follow-up email
- Thank you note
- Additional materials requested
- Proposal/term sheet draft

**FRI (4h):**
- Debrief: what went well, what didn't
- Identify concerns raised
- Prepare responses

**WEEKEND:**
- Research backup options (Eniwa, others)
- Prepare alternative approaches

**GOAL:** Pitch delivered, interest level assessed

---

### Week 24 (Jul 14-20): Term Sheet
**Focus:** Negotiate deal structure

**MON (4h):**
- Review any counter-proposals
- Discuss with lawyer
- Determine walk-away terms

**TUE (4h):**
- Draft term sheet (with lawyer)
- Price: CHF 300K + CHF 100K earnout
- Terms: transition, IP, etc.

**WED (4h):**
- Present term sheet
- Discuss earnout conditions
- Negotiate price/structure

**THU (4h):**
- Address objections
- Highlight value (again)
- Push for commitment

**FRI (4h):**
- Finalize term sheet
- Sign (if agreed)
- Or: continue negotiation next week

**GOAL:** Term sheet agreed in principle

---

## AUGUST 2026: Due Diligence & Closing

### Week 25 (Jul 21-27): Due Diligence
**Focus:** Support buyer's review process

**MON (5h):**
- Organize data room
- Legal, technical, financial docs
- Grant access to buyer's team

**TUE (5h):**
- Technical audit support
- Code repository access
- Architecture walkthrough

**WED (5h):**
- Financial audit support
- Explain cost structure
- Revenue projections

**THU (3h):**
- Answer questions
- Provide clarifications
- Address concerns

**FRI (2h):**
- Fix any issues identified
- Security patches if needed
- Update documentation

**GOAL:** Due diligence completed successfully

---

### Week 26 (Jul 28 - Aug 3): Closing
**Focus:** Sign contracts, get paid!

**MON (4h):**
- Review final contracts (with lawyer)
- Asset purchase agreement
- IP transfer docs
- Transition services agreement

**TUE (4h):**
- Sign contracts
- Celebrate! 🎉
- Announce to users (transition plan)

**WED (4h):**
- Receive payment (upfront portion)
- Verify transfer
- Begin transition

**THU (4h):**
- Knowledge transfer session 1
- Walk through codebase
- Explain architecture

**FRI (4h):**
- Plan transition period (Month 1-3)
- Set up communication channels
- Review deliverables

**GOAL:** Deal closed, transition started

---

## Success Metrics (Weekly Tracking)

### Leading Indicators
Track every Monday morning:
- [ ] Total registrations (target growth: +30/week in Feb-Mar)
- [ ] Verification rate (target: >70%)
- [ ] Profile completion rate (target: >60%)
- [ ] Utility consent rate (target: >70%)
- [ ] Communities forming (target: 1-2/week in Apr-May)

### Milestones
- [ ] Feb 28: 200 registrations
- [ ] Mar 31: 500 registrations
- [ ] Apr 30: 10 communities forming
- [ ] May 31: 5 DSO submissions
- [ ] Jun 30: Pitch delivered
- [ ] Jul 31: Term sheet signed
- [ ] Aug 31: Deal closed

---

## Weekly Review Template

Every Friday, spend 30 min reviewing:

**What went well this week?**
- [Specific wins]

**What didn't go as planned?**
- [Challenges, blockers]

**Key metrics:**
- Total registrations: [X]
- This week's new: [X]
- Communities forming: [X]
- Conversion rate: [X]%

**Next week priorities:**
- [Priority 1]
- [Priority 2]
- [Priority 3]

**Blockers / Help needed:**
- [Issues requiring attention]

**Adjustments to plan:**
- [Any pivots or strategy changes]

---

## Risk Triggers (Monitor Weekly)

**🚨 RED FLAGS:**
- Week 8: <200 registrations → PIVOT to direct B2B sales
- Week 12: <300 registrations → Reduce feature scope, increase marketing
- Week 16: 0 DSO submissions → Simplify formation process
- Week 21: No response from Regionalwerke → Contact alternative buyers
- Week 24: Negotiation stalled → Activate plan B (Eniwa or independent)

**✅ GREEN LIGHTS:**
- Week 8: >300 registrations → Increase marketing budget
- Week 12: >500 registrations → Accelerate formation features
- Week 16: >10 DSO submissions → Prepare for scale
- Week 21: Strong interest from Regionalwerke → Negotiate hard
- Week 24: Multiple buyer interest → Auction dynamic

---

## Daily Habits

**Every Morning (15 min):**
- Check registrations overnight
- Review support emails
- Check metrics dashboard
- Prioritize day's work

**Every Evening (10 min):**
- Log what you shipped
- Update weekly progress
- Plan tomorrow's tasks

**Every Monday (30 min):**
- Review last week
- Plan this week's priorities
- Update roadmap if needed

**Every Friday (30 min):**
- Weekly review (use template above)
- Celebrate wins
- Reset for next week

---

## Emergency Contacts

**Technical Issues:**
- Railway support (if hosting there)
- PostgreSQL issues: [DBA contact or forum]

**Legal Issues:**
- Energy lawyer: [Contact after hired]
- General legal: [Your lawyer]

**Strategic Questions:**
- Advisor 1: [If you have one]
- Advisor 2: [If you have one]

**Mental Health:**
- This is a sprint, not a marathon
- Take breaks
- Don't burn out
- Ask for help when needed

---

## Final Thoughts

**This plan is ambitious but achievable.**

Key success factors:
1. **Focus:** Say no to everything not on this plan
2. **Speed:** Ship fast, iterate, don't perfect
3. **Metrics:** Track weekly, adjust quickly
4. **Support:** Get help (lawyer, advisors, VA if needed)
5. **Resilience:** Setbacks will happen, keep pushing

**The prize: CHF 300-500K exit in 6 months**

That's worth the sprint.

**You can do this. Start Monday. Execute ruthlessly.**

---

*Last updated: Feb 2, 2026*
*Print this. Put it on your wall. Review every Monday.*
