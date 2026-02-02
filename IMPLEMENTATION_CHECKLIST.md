# BadenLEG Implementation Checklist
**Start Date:** Feb 3, 2026
**Target Acquisition:** Aug 2026
**Quick Reference Guide**

---

## Phase 0: Foundation (COMPLETE ✅)

- [x] PostgreSQL database
- [x] Referral system
- [x] GA4 analytics
- [x] Formation wizard backend (coded but not integrated)
- [x] Consent capture
- [x] Admin endpoints
- [x] Security hardening

**Status:** Production-ready infrastructure exists

---

## Phase 1: Demand Engine (Weeks 1-6, Feb 3 - Mar 16)

### Week 1: Launch (Feb 3-9)
- [ ] Deploy live counter (`/api/stats/live`)
- [ ] Update homepage with urgency messaging
- [ ] Launch Facebook ads (CHF 100/day)
- [ ] Email 10 solar installers
- [ ] Set up email automation infrastructure
- [ ] Press release draft

**Target:** 20 registrations, 2 partnerships initiated

---

### Week 2: Automation (Feb 10-16)
- [ ] User dashboard (`/dashboard`) with readiness score
- [ ] Day 0-14 email sequence (4 emails)
- [ ] Profile completion forms
- [ ] A/B testing infrastructure
- [ ] Follow up with installers (confirm 2 partnerships)

**Target:** 50 total registrations (30 new)

---

### Week 3-4: Growth (Feb 17 - Mar 2)
- [ ] Increase ad spend to CHF 150/day
- [ ] Street-level targeting (partial clusters)
- [ ] Referral program promotion
- [ ] WhatsApp group templates
- [ ] Physical flyer distribution
- [ ] Press release submission

**Target:** 100 total registrations

---

### Week 5-6: Pre-Formation (Mar 3-16)
- [ ] Email nurturing campaigns
- [ ] Re-engagement flows
- [ ] Community readiness notifications
- [ ] Identify 5 pilot communities
- [ ] Formation wizard UI planning

**Target:** 200 total registrations, 10 clusters ready

---

## Phase 2: Formation Capability (Weeks 7-14, Mar 17 - May 11)

### Week 7-9: Wizard UI (Mar 17 - Apr 6)
- [ ] `/formation/start` route & template
- [ ] Community creation form
- [ ] Member invitation system
- [ ] `/formation/community/<id>` dashboard
- [ ] Status visualization
- [ ] Integration of `formation_wizard.py` backend

**Target:** Formation wizard MVP functional

---

### Week 10-12: Documents (Apr 7-27)
- [ ] WeasyPrint setup
- [ ] Community agreement template (DE, legal review)
- [ ] Participant contract template
- [ ] DSO notification form
- [ ] PDF download endpoints
- [ ] Generate docs for 5 pilot communities

**Target:** Documents generated for 5 communities

---

### Week 13-14: Pilot Activation (Apr 28 - May 11)
- [ ] Collect signatures (5 pilot communities)
- [ ] Submit DSO notifications
- [ ] Track approval process
- [ ] Document learnings
- [ ] Scale formation to 20 communities

**Target:** 10 DSO submissions, 450 total registrations

---

## Phase 3: Utility Ops Layer (Weeks 15-20, May 12 - Jun 22)

### Week 15-16: Admin Dashboard (May 12-25)
- [ ] Pipeline visualization (5 stages)
- [ ] Recent registrations table
- [ ] Communities management table
- [ ] Search/filter functionality
- [ ] CSV export buttons
- [ ] Pending actions alerts

**Target:** Full ops dashboard operational, 500 registrations (MILESTONE!)

---

### Week 17-18: Handoff Package (May 26 - Jun 8)
- [ ] CSV export (all consented households)
- [ ] ZIP package (CSV + PDFs + README)
- [ ] GIS export (KML/GeoJSON)
- [ ] Audit logging for exports
- [ ] Test export with sample data
- [ ] Informal Regionalwerke contact

**Target:** Utility handoff package ready, 550 registrations

---

### Week 19-20: API & Acquisition Prep (Jun 9-22)
- [ ] REST API endpoints (households, communities)
- [ ] API key authentication
- [ ] OpenAPI documentation
- [ ] Metrics dashboard (all KPIs)
- [ ] Customer testimonials (5-10 video/written)
- [ ] Acquisition deck (15 slides)

**Target:** API documented, acquisition deck complete, 600 registrations

---

## Phase 4: Acquisition (Weeks 21-26, Jun 23 - Aug 4)

### Week 21-22: First Contact (Jun 23 - Jul 6)
- [ ] Finalize proof package
- [ ] Platform demo video (5 min)
- [ ] Intro email to Regionalwerke
- [ ] Schedule presentation meeting
- [ ] Prepare for questions

---

### Week 23-24: Presentation & Negotiation (Jul 7-20)
- [ ] Present acquisition case
- [ ] Provide additional data as requested
- [ ] Negotiate terms (price, earnout, transition)
- [ ] Get term sheet
- [ ] Legal review initiation

---

### Week 25-26: Due Diligence & Closing (Jul 21 - Aug 4)
- [ ] Code access for technical review
- [ ] Financial data sharing
- [ ] Security assessment cooperation
- [ ] Review purchase agreement
- [ ] Sign agreements
- [ ] **ACQUISITION CLOSED** 🎉

**Target:** CHF 300-500K exit

---

## Critical Files to Create/Modify

### New Files Needed

**Backend:**
- `email_automation.py` - Automated email sequences
- `document_generator.py` - PDF generation
- `api.py` - REST API endpoints

**Templates:**
- `templates/dashboard.html` - User dashboard
- `templates/formation/start.html` - Formation wizard start
- `templates/formation/community.html` - Community status view
- `templates/admin/operations.html` - Internal ops dashboard
- `templates/emails/day_0_welcome.html` - Welcome email
- `templates/emails/day_3_smartmeter.html` - Smart meter question
- `templates/emails/day_7_consumption.html` - Consumption data
- `templates/emails/day_14_readiness.html` - Readiness check
- `templates/documents/community_agreement.html` - PDF template
- `templates/documents/participant_contract.html` - PDF template
- `templates/documents/dso_notification.html` - PDF template

---

### Files to Modify

**Backend:**
- `app.py` - Add new routes (formation, dashboard, admin)
- `database.py` - Add helper methods (counts, filters)

**Frontend:**
- `templates/index.html` - Add live counter, urgency elements
- `templates/base.html` - Add Facebook Pixel

**Database:**
- Add migrations for: `scheduled_emails`, `community_documents`

---

## Database Schema Extensions

```sql
-- Scheduled emails
CREATE TABLE scheduled_emails (
    id SERIAL PRIMARY KEY,
    building_id VARCHAR(64) REFERENCES buildings,
    email VARCHAR(255) NOT NULL,
    template_key VARCHAR(64) NOT NULL,
    send_at TIMESTAMP NOT NULL,
    sent_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending'
);

-- Community documents
CREATE TABLE community_documents (
    community_id VARCHAR(64) PRIMARY KEY REFERENCES communities,
    documents JSONB,
    generated_at TIMESTAMP
);

-- API keys
CREATE TABLE api_keys (
    key_id VARCHAR(64) PRIMARY KEY,
    key_hash VARCHAR(128) NOT NULL,
    name VARCHAR(255),
    permissions JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP
);

-- Webhooks
CREATE TABLE webhooks (
    webhook_id VARCHAR(64) PRIMARY KEY,
    url TEXT NOT NULL,
    events JSONB,
    secret VARCHAR(128),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN DEFAULT TRUE
);
```

---

## Marketing Checklist

### Facebook Ads
- [ ] Create Business Manager account
- [ ] Install Facebook Pixel
- [ ] Create 3 ad variants (solar owners, cost-conscious, environmentalists)
- [ ] Set up conversion tracking
- [ ] Launch with CHF 100/day budget
- [ ] Monitor daily, optimize weekly

### Partnerships
- [ ] List 10 target solar installers
- [ ] Draft partnership email
- [ ] Send personalized outreach
- [ ] Create co-branded flyer PDF
- [ ] Print 1000 flyers (CHF 500)
- [ ] Deliver to confirmed partners

### PR
- [ ] Write press release
- [ ] Create media kit (press release, photos, infographic)
- [ ] Submit to Badener Tagblatt
- [ ] Follow up with journalist call
- [ ] Offer interview/demo
- [ ] Track media mentions

### Content
- [ ] FAQ page
- [ ] Case studies (after pilot communities)
- [ ] Savings calculator (interactive)
- [ ] Email newsletter template
- [ ] Social media calendar (3 posts/week)

---

## Technical Dependencies

### Python Packages to Install
```bash
pip install weasyprint  # PDF generation
pip install jinja2  # Already installed, but verify version
pip install psycopg2-binary  # Already installed
pip install Flask-Limiter  # Already installed
```

### Services to Configure
- [x] SendGrid (already configured)
- [x] Google Analytics 4 (already integrated)
- [ ] Facebook Business Manager
- [ ] Cron job service (Railway Cron or external)

### Environment Variables to Set
```bash
FB_PIXEL_ID=your_facebook_pixel_id
API_SECRET_KEY=generate_random_32_char_string
CRON_SECRET=for_authenticating_cron_jobs
```

---

## Metrics to Track Weekly

### Growth Metrics (Every Monday)
- [ ] Total registrations
- [ ] New registrations (last 7 days)
- [ ] Email verification rate
- [ ] Profile completion rate
- [ ] Referral rate

### Engagement Metrics
- [ ] Email open rate (target: 40%+)
- [ ] Dashboard visit rate
- [ ] Formation starts
- [ ] Communities formed
- [ ] DSO submissions

### Marketing Metrics
- [ ] Facebook CPM (target: < CHF 15)
- [ ] Facebook CPC (target: < CHF 1.50)
- [ ] Cost per registration (target: < CHF 40)
- [ ] Organic traffic growth
- [ ] Partner referrals

### Acquisition Metrics
- [ ] Total verified households
- [ ] Utility consent rate (target: 70%+)
- [ ] Formation throughput (communities/week)
- [ ] DSO approval rate
- [ ] Media mentions

---

## Daily Routine

### Morning (30 min)
- Check overnight registrations
- Review ad performance
- Respond to critical emails
- Check for errors/bugs
- Plan day's priorities

### Work Blocks (6-8 hours)
- Deep work on current week's features
- No distractions, focus time
- Test as you build
- Document as you go

### Afternoon (30 min)
- Deploy to staging
- QA testing
- Review metrics
- Respond to user questions

### Evening (15 min)
- Final production check
- Plan tomorrow
- Update project board

---

## Weekly Routine

### Monday Morning (1h)
- Review last week's metrics
- Set this week's goals (3-5 specific)
- Update planning docs
- Prioritize tasks

### Friday Afternoon (2h)
- Deploy week's work to production
- Full QA testing
- Update documentation
- Metrics review vs. targets
- Plan next week

### Sunday Evening (1h)
- Mental reset
- Review acquisition timeline
- Adjust strategy if needed
- Prep for Monday

---

## Red Flags to Watch

### User Growth Stalls (< 15 new/week)
**Response:**
- Double marketing budget
- Launch partnership blitz
- Door-to-door campaign
- Event marketing

### Formation Rate Low (< 2 communities/week)
**Response:**
- Simplify wizard (remove friction)
- Phone support for formations
- Group formation webinars
- Financial incentives

### DSO Delays (> 45 days)
**Response:**
- Escalate with Regionalwerke
- Legal consultation
- Media pressure
- Alternative contacts

### Technical Failures (> 5% error rate)
**Response:**
- Roll back deployment
- Fix critical bugs immediately
- Add monitoring/alerts
- Implement fallback processes

---

## Success Criteria (Ready for Acquisition)

### Must-Have (Deal Blockers)
- [ ] 500+ verified households (Baden)
- [ ] 20+ communities formed
- [ ] 10+ DSO submissions
- [ ] 70%+ utility consent rate
- [ ] Utility handoff package (tested)
- [ ] Internal ops dashboard (functional)
- [ ] No major security vulnerabilities
- [ ] Acquisition deck (complete)

### Nice-to-Have (Strengthen Position)
- [ ] 1000+ registered households
- [ ] 50+ communities formed
- [ ] 5+ media mentions
- [ ] Alternative buyer interest
- [ ] Revenue (CHF 10K+ from fees)

---

## Quick Win: This Week (Feb 3-9)

**Monday (TODAY):**
1. Deploy live counter to homepage (2h)
2. Create Facebook Business Manager account (1h)
3. Draft solar installer outreach email (1h)
4. Set up email automation database tables (2h)
5. Update homepage with urgency text (1h)
6. Launch first Facebook ad (CHF 100/day, 5 days) (1h)

**By Friday:**
- 20 registrations
- Ads running
- Email automation functional
- 10 installer emails sent
- Press release drafted

**JUST START. Imperfect action > perfect planning.**

---

## When Things Go Wrong

### Bug in Production
1. Check error logs immediately
2. Assess impact (how many users affected?)
3. Rollback if critical (< 5 min decision)
4. Fix in staging
5. Test thoroughly
6. Re-deploy
7. Monitor closely

### Marketing Not Working
1. Review data (which channel underperforming?)
2. Pause underperformers immediately
3. A/B test new variants
4. Shift budget to winners
5. Try alternative channels

### Acquisition Talks Stall
1. Don't panic (negotiations take time)
2. Continue operations (show momentum)
3. Gather more proof points
4. Engage alternative buyers
5. Be willing to walk away

---

## Resources & Support

### Technical Questions
- Flask docs: flask.palletsprojects.com
- PostgreSQL docs: postgresql.org/docs
- WeasyPrint docs: weasyprint.org

### Legal/Regulatory
- Stromversorgungsgesetz (StromVG): fedlex.admin.ch
- Energy law expert: (consult if needed)
- Privacy/GDPR: (already compliant)

### Marketing
- Facebook Ads Help: facebook.com/business/help
- Google Analytics: analytics.google.com
- Copywriting resources: copyhackers.com

### Community
- Founder peers: (local startup community)
- Swiss energy forums: (research if needed)

---

## Final Reminders

1. **Ship fast, iterate faster.** Don't wait for perfection.
2. **Focus on acquisition value.** Every feature decision: does this prove the case?
3. **Talk to users.** 5 conversations = more insight than 100 analytics reports.
4. **Measure everything.** If you can't measure it, you can't improve it.
5. **Take care of yourself.** 6 months is a marathon, not a sprint.
6. **Trust the plan.** You've done the thinking. Now execute.

**You've got this. Start Monday. Execute relentlessly. Exit by August.**

---

*Created: Feb 2, 2026*
*Review: Every Monday*
*Update: As needed*

**Next Action:** Deploy live counter + launch first Facebook ad (Monday Feb 3)
