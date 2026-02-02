# BadenLEG Weekly Execution Plan
**Period:** Feb 3 - Aug 31, 2026 (26 weeks)
**Goal:** 500+ households, 20+ communities, acquisition-ready

---

## Week 1 (Feb 3-9): Foundation Launch

### Monday (8h)
- [ ] Deploy live counter endpoint (`/api/stats/live`)
- [ ] Update homepage with urgency elements
- [ ] Set up Facebook Business Manager account
- [ ] Create initial ad campaign (CHF 100/day, 5 days)
- [ ] Write press release draft

**Deliverables:** Homepage updated, ads running, press release ready

### Tuesday (8h)
- [ ] Email automation infrastructure (database tables)
- [ ] Day 0 welcome email template
- [ ] Day 3 smart meter email template
- [ ] Schedule system (cron job setup)
- [ ] Test email flow with 5 test accounts

**Deliverables:** Email automation functional

### Wednesday (8h)
- [ ] Research 10 solar installers in Baden
- [ ] Draft partnership email template
- [ ] Send personalized outreach (10 emails)
- [ ] Create installer flyer PDF (QR code + value prop)
- [ ] Set up tracking for partnership referrals

**Deliverables:** 10 installer outreach emails sent

### Thursday (8h)
- [ ] Referral system UI enhancements
- [ ] Copy-to-clipboard functionality
- [ ] Email invitation form
- [ ] Referral stats display
- [ ] Social sharing buttons (WhatsApp, Email)

**Deliverables:** Referral UI complete

### Friday (4h) - Deployment & Metrics
- [ ] Deploy all week's work to production
- [ ] QA testing (registration → email → dashboard flow)
- [ ] Set up GA4 custom events
- [ ] Create week 1 metrics dashboard
- [ ] Document any bugs/issues

**Deliverables:** Production deployment, metrics baseline

### Weekend (4h) - Content & Growth
- [ ] Submit press release to Badener Tagblatt
- [ ] Create social media posts (Facebook, Instagram)
- [ ] Monitor ad performance, adjust targeting
- [ ] Respond to any inquiries/emails
- [ ] Plan week 2 priorities

**Week 1 Targets:**
- 20 registrations
- 2 installer partnerships initiated
- Email automation live
- Referral system functional
- Press coverage pitch sent

---

## Week 2 (Feb 10-16): Profile Collection

### Monday (8h)
- [ ] Implement dashboard readiness score calculation
- [ ] Create dashboard template (`/dashboard`)
- [ ] Progress bar visualization
- [ ] Steps checklist UI
- [ ] Link from email to dashboard

**Deliverables:** User dashboard live

### Tuesday (8h)
- [ ] Day 7 consumption data email template
- [ ] Day 14 readiness email template
- [ ] Dashboard "complete your profile" CTAs
- [ ] Form for energy profile updates
- [ ] Save profile updates to database

**Deliverables:** Progressive profiling complete

### Wednesday (8h)
- [ ] Follow up with installer contacts (phone calls)
- [ ] Negotiate partnership terms (referral fee, flyer distribution)
- [ ] Finalize flyer design
- [ ] Print 500 flyers (local print shop)
- [ ] Deliver flyers to confirmed partners

**Deliverables:** 2 confirmed partnerships, flyers distributed

### Thursday (8h)
- [ ] A/B test different homepage headlines
- [ ] Implement headline rotation
- [ ] Track conversions by variant
- [ ] Create "community forming" notification system
- [ ] Email users when nearby neighbors register

**Deliverables:** A/B testing infrastructure, neighbor notifications

### Friday (4h)
- [ ] Production deployment
- [ ] Test progressive profiling flow end-to-end
- [ ] Review week 1 metrics (registrations, email opens, referrals)
- [ ] Adjust marketing based on data
- [ ] Plan week 3

**Week 2 Targets:**
- 50 total registrations (30 new)
- 30%+ profile completion rate
- 2 confirmed partnerships
- 15% referral rate

---

## Week 3-4 (Feb 17 - Mar 2): Growth Acceleration

### Key Initiatives (16 days, 64h total)

**Marketing Blitz (20h):**
- [ ] Increase Facebook ad spend to CHF 150/day
- [ ] Create 5 ad variants (different images, copy)
- [ ] Instagram ads launch
- [ ] Local Facebook group posts (organic)
- [ ] Reddit r/Switzerland post (if allowed)
- [ ] Partner email to installer customer lists

**Street-Level Targeting (12h):**
- [ ] Identify streets with 2-3 partial clusters
- [ ] Create neighborhood-specific ads ("Your neighbors on Musterstrasse...")
- [ ] Physical flyer drops (target streets)
- [ ] Door-to-door outreach (pilot 20 houses)

**Referral Campaign (12h):**
- [ ] Launch "CHF 50 for you + CHF 50 for friend" promo
- [ ] Email existing users about referral program
- [ ] Create shareable social media graphics
- [ ] Leaderboard on homepage
- [ ] Weekly referral winner announcement

**WhatsApp Groups (8h):**
- [ ] Create group template
- [ ] Invite users in formed clusters
- [ ] Community manager role (respond to questions)
- [ ] Share formation tips, next steps

**Email Nurturing (12h):**
- [ ] Segment users by readiness score
- [ ] Targeted emails to 80%+ readiness ("You're almost ready!")
- [ ] Re-engagement for inactive users
- [ ] Success stories from early adopters

**Week 3-4 Targets:**
- 100 total registrations (cumulative)
- 5 clusters with 4+ confirmed members
- 40%+ profile completion
- 20% referral rate
- 2 media mentions (articles or interviews)

---

## Week 5-6 (Mar 3-16): Pre-Formation Prep

### Formation Wizard Development (32h)
- [ ] `/formation/start` route & template
- [ ] Community creation form
- [ ] Member selection UI
- [ ] Invitation email system
- [ ] `/formation/accept/<token>` endpoint
- [ ] Community dashboard template
- [ ] Status visualization (progress steps)
- [ ] Readiness score integration

### Pilot Community Selection (8h)
- [ ] Identify 5 "ready" clusters (4+ members, high engagement)
- [ ] Personal outreach to admins
- [ ] Explain pilot benefits (free formation, priority support)
- [ ] Confirm participation
- [ ] Schedule formation kickoff meetings

### Document Templates Draft (12h)
- [ ] Community agreement German text (legal review)
- [ ] Participant contract template
- [ ] DSO notification form (Regionalwerke format research)
- [ ] PDF generation setup (WeasyPrint install)
- [ ] Test PDF output

### Marketing Continued (12h)
- [ ] Facebook ads optimization (pause low performers)
- [ ] Increase budget on best performing ads
- [ ] Create video testimonial (if possible)
- [ ] Partnership expansion (2 more installers)
- [ ] Local newspaper follow-up

**Week 5-6 Targets:**
- 200 total registrations
- 10 clusters ready to form
- 5 pilot communities confirmed
- Formation wizard MVP deployed
- Document templates drafted

---

## Week 7-9 (Mar 17 - Apr 6): Formation Wizard Polish

### Full Wizard Implementation (60h)
- [ ] Multi-step formation flow
- [ ] Member invitation system (email + token)
- [ ] Community dashboard (status, members, documents)
- [ ] Next steps recommendation engine
- [ ] Admin controls (invite/remove members)
- [ ] Distribution model selection
- [ ] Formation start button (checks minimum members)

### Document Generation (40h)
- [ ] WeasyPrint integration
- [ ] HTML templates for all 3 document types
- [ ] Signature field placement
- [ ] Download endpoints (secured)
- [ ] Bulk generation for multiple communities
- [ ] Email delivery of documents

### Pilot Community Formation (20h)
- [ ] 5 communities create via wizard
- [ ] Generate all documents
- [ ] Collect signatures (electronic or email confirmation)
- [ ] Submit DSO notifications
- [ ] Track approval process
- [ ] Document any issues/learnings

**Week 7-9 Targets:**
- 300 total registrations
- Formation wizard fully functional
- 5 pilot communities with complete documents
- 5 DSO submissions completed
- 0 major bugs in formation flow

---

## Week 10-12 (Apr 7-27): Document Refinement

### Legal Review (16h)
- [ ] Consult with Swiss energy law expert
- [ ] Review community agreement compliance
- [ ] Update templates based on feedback
- [ ] Add required legal disclosures
- [ ] Finalize terms and conditions

### DSO Coordination (12h)
- [ ] Contact Regionalwerke Baden DSO department
- [ ] Discuss submission format preferences
- [ ] Share sample documents for feedback
- [ ] Adjust forms to match their requirements
- [ ] Establish submission process

### Batch Document Generation (12h)
- [ ] Admin tool for bulk document generation
- [ ] Generate docs for all ready communities
- [ ] Email all members with signature instructions
- [ ] Track signature collection status
- [ ] Reminder emails for pending signatures

### Formation Support (20h)
- [ ] User support (emails, questions)
- [ ] Troubleshoot formation issues
- [ ] Guide communities through process
- [ ] Create FAQ document
- [ ] Video tutorials (optional)

### Marketing (20h)
- [ ] Case study from pilot communities
- [ ] Before/after testimonials
- [ ] Success metrics (X communities formed, Y households)
- [ ] Press release: "First BadenLEG communities formed"
- [ ] Social media campaign

**Week 10-12 Targets:**
- 400 total registrations
- 15 communities in formation
- 10 DSO submissions
- Legal compliance verified
- DSO relationship established

---

## Week 13-14 (Apr 28 - May 11): Scale Formation

### Formation Acceleration (24h)
- [ ] Email campaign to ready clusters
- [ ] "Last chance to form in April" urgency
- [ ] Streamline wizard (remove friction)
- [ ] Automated formation suggestions
- [ ] Group formation events (online meetings)

### Document Pipeline (16h)
- [ ] Monitor signature collection
- [ ] Follow up on delayed signatures
- [ ] Submit all complete DSO notifications
- [ ] Track DSO approval timelines
- [ ] Database of submission statuses

### Support Scaling (12h)
- [ ] FAQ page for common questions
- [ ] Email templates for support responses
- [ ] Self-service resources
- [ ] Community forums or Discord (optional)

### Marketing (12h)
- [ ] Highlight formation success stories
- [ ] "X communities already formed"
- [ ] FOMO messaging
- [ ] Limited time formation incentives

**Week 13-14 Targets:**
- 450 total registrations
- 20 communities formed
- 15 DSO submissions
- 5 DSO approvals received
- Formation process streamlined

---

## Week 15-16 (May 12-25): Admin Dashboard

### Operations Dashboard (40h)
- [ ] Pipeline visualization (5 stages)
- [ ] Recent registrations table
- [ ] Communities in formation table
- [ ] Pending actions alerts
- [ ] Search/filter functionality
- [ ] CSV export buttons
- [ ] Building detail view
- [ ] Community management view

### Reporting (12h)
- [ ] Weekly metrics report (automated)
- [ ] Community status report
- [ ] DSO submission tracking
- [ ] Consent compliance audit
- [ ] Growth projections

### Internal Tools (12h)
- [ ] Bulk email tool
- [ ] User data export
- [ ] Community status updates
- [ ] Manual intervention capabilities

**Week 15-16 Targets:**
- 500 total registrations (MILESTONE!)
- 25 communities formed
- 20 DSO submissions
- Full admin dashboard operational
- Weekly metrics automated

---

## Week 17-18 (May 26 - Jun 8): Utility Handoff Package

### Export Package Development (32h)
- [ ] CSV format design (field mapping)
- [ ] Consent verification logic
- [ ] ZIP package generator
- [ ] README file template
- [ ] Community PDFs bundled
- [ ] GIS export (KML/GeoJSON)
- [ ] Audit logging for exports

### Utility Coordination (12h)
- [ ] Identify Regionalwerke contact (decision-maker)
- [ ] Informal meeting request
- [ ] Share sample export package
- [ ] Get feedback on format
- [ ] Adjust based on needs

### API Development (20h)
- [ ] REST API endpoints (households, communities)
- [ ] API key authentication
- [ ] Rate limiting
- [ ] OpenAPI documentation
- [ ] Webhook registration endpoint

**Week 17-18 Targets:**
- 550 total registrations
- 30 communities formed
- Utility handoff package ready
- API documentation complete
- Regionalwerke contact established

---

## Week 19-20 (Jun 9-22): Acquisition Preparation

### Proof Package Assembly (24h)
- [ ] Metrics dashboard (all KPIs)
- [ ] Customer testimonials (video + written)
- [ ] Media coverage compilation
- [ ] Cost avoidance analysis
- [ ] Platform demo video (record + edit)
- [ ] Technical documentation
- [ ] Security audit report

### Acquisition Deck (16h)
- [ ] Slide deck (15 slides)
- [ ] Business case slides
- [ ] Product demo slides
- [ ] Integration plan slides
- [ ] Financial projections
- [ ] Team/transition plan
- [ ] Practice presentation

### Due Diligence Prep (12h)
- [ ] Code cleanup/documentation
- [ ] Database schema documentation
- [ ] Security review
- [ ] Legal review (all contracts)
- [ ] Financial records organized

### Outreach (12h)
- [ ] Intro email to Regionalwerke
- [ ] Follow-up calls
- [ ] Schedule presentation meeting
- [ ] Prepare for questions

**Week 19-20 Targets:**
- 600 total registrations
- 35 communities formed
- Acquisition deck complete
- First meeting scheduled
- Due diligence ready

---

## Week 21-26 (Jun 23 - Aug 4): Negotiation & Closing

### Presentation & Negotiation (30h across 6 weeks)
- [ ] Present acquisition case
- [ ] Answer questions
- [ ] Provide additional data as requested
- [ ] Negotiate terms (price, earnout, transition)
- [ ] Get term sheet

### Due Diligence Support (30h)
- [ ] Provide code access
- [ ] Answer technical questions
- [ ] Security assessment cooperation
- [ ] Financial data sharing
- [ ] Customer data room setup

### Legal Process (20h)
- [ ] Review purchase agreement
- [ ] Negotiate contract terms
- [ ] IP transfer documentation
- [ ] Transition services agreement
- [ ] Sign agreements

### Continued Operations (40h)
- [ ] Continue supporting formations
- [ ] Maintain platform operations
- [ ] User support
- [ ] Keep growth momentum
- [ ] Document everything

**Week 21-26 Targets:**
- 700+ total registrations
- 40+ communities formed
- Term sheet signed
- Due diligence complete
- Acquisition closed (CHF 300-500K)

---

## Weekly Rhythm (Every Week)

### Monday Morning (1h)
- Review previous week metrics
- Set weekly goals (3-5 specific outcomes)
- Prioritize tasks
- Update project board

### Daily Standups (15min each)
- What did I accomplish yesterday?
- What will I accomplish today?
- What blockers exist?
- Adjust plan as needed

### Friday Afternoon (2h)
- Deploy week's work
- QA testing
- Update documentation
- Review metrics vs. targets
- Plan next week

### Sunday Evening (1h)
- Prep for Monday
- Review acquisition timeline
- Adjust strategy if needed
- Mental reset

---

## Metrics Tracking (Weekly Review)

### Growth Metrics
- [ ] Total registrations
- [ ] Weekly new registrations
- [ ] Email verification rate
- [ ] Profile completion rate
- [ ] Referral rate

### Engagement Metrics
- [ ] Email open rates
- [ ] Dashboard visit rate
- [ ] Time to formation (days)
- [ ] Communities formed
- [ ] DSO submissions

### Conversion Metrics
- [ ] Visitor → registration conversion
- [ ] Registration → verified conversion
- [ ] Verified → community member conversion
- [ ] Community → DSO submission conversion

### Acquisition Metrics
- [ ] Total verified households
- [ ] Utility consent rate
- [ ] Formation throughput (communities/week)
- [ ] DSO approval rate
- [ ] Media mentions

---

## Resource Allocation

### Time Budget (26 weeks × 20h = 520h total)

**Phase 1 - Demand (Week 1-6):** 120h
- Marketing/content: 40h
- Email automation: 30h
- Dashboard/UX: 30h
- Partnerships: 20h

**Phase 2 - Formation (Week 7-14):** 160h
- Wizard UI: 80h
- Documents: 50h
- Pilot support: 30h

**Phase 3 - Ops (Week 15-20):** 120h
- Admin dashboard: 50h
- Export package: 40h
- API: 30h

**Phase 4 - Acquisition (Week 21-26):** 120h
- Presentation: 40h
- Due diligence: 40h
- Operations: 40h

---

## Success Milestones

### February End (Week 4)
- ✅ 100 registrations
- ✅ Email automation live
- ✅ 2 partnerships
- ✅ Referral system functional

### March End (Week 8)
- ✅ 300 registrations
- ✅ Formation wizard deployed
- ✅ 5 pilot communities

### April End (Week 12)
- ✅ 450 registrations
- ✅ 15 communities formed
- ✅ 10 DSO submissions

### May End (Week 16)
- ✅ 550 registrations
- ✅ 25 communities formed
- ✅ Admin dashboard operational

### June End (Week 20)
- ✅ 650 registrations
- ✅ 35 communities formed
- ✅ Acquisition deck presented

### August End (Week 26)
- ✅ 700+ registrations
- ✅ 40+ communities formed
- ✅ Acquisition closed

---

## Contingency Plans

### If Growth Stalls (< 20 new registrations/week)
1. Double marketing budget (CHF 200/day)
2. Door-to-door campaign (hire part-time help)
3. Partnership expansion (10 more installers)
4. Event marketing (local sustainability fairs)
5. PR blitz (press releases to all local media)

### If Formation Rate Low (< 2 communities/week)
1. Simplify wizard (remove optional steps)
2. Phone support for formation
3. Group formation webinars
4. Formation incentives (CHF 50 credit)
5. Pre-filled templates (less user input)

### If DSO Delays (> 45 days approval)
1. Escalate with Regionalwerke management
2. Legal consultation (are delays justified?)
3. Media attention (public pressure)
4. Alternative DSO contacts
5. Federal regulator escalation (if needed)

### If Regionalwerke Doesn't Respond
1. Alternative buyers (Eniwa, Axpo, EKZ)
2. Licensing model (sell to multiple utilities)
3. Continue independent growth
4. Investor fundraising
5. Expand to other cantons

---

## Communication Plan

### Weekly Updates (Fridays)
- Email to all registered users
- "This week: X new households joined"
- Formation updates
- Tips and next steps

### Monthly Newsletter
- Success stories
- Community spotlights
- LEG education
- Upcoming events

### Media Relations
- Press release every major milestone
- Respond to journalist inquiries within 24h
- Offer expert commentary on LEG topics
- Build relationships with Badener Tagblatt

### Utility Communication
- Monthly informal check-ins
- Share anonymized metrics
- Solicit feedback
- Build relationship before acquisition pitch

---

*Last updated: Feb 2, 2026*
*Review and update every Monday*
