# BadenLEG Metrics Dashboard

## Weekly Tracking Template

### Week of: _______________

## User Metrics
| Metric | Target | Actual | Notes |
|--------|--------|--------|-------|
| Total Registered Users | - | - | |
| New Registrations (this week) | - | - | |
| Verified Users | - | - | |
| Registration Conversion Rate | >20% | - | visitors → registrations |

## Referral Metrics
| Metric | Target | Actual | Notes |
|--------|--------|--------|-------|
| Total Referrals | - | - | |
| Referral Rate | 20-30% | - | users who refer at least 1 person |
| Top Referrer Count | - | - | |

## Acquisition Cost
| Metric | Target | Actual | Notes |
|--------|--------|--------|-------|
| Marketing Spend (CHF) | - | - | |
| Cost per Acquisition | <CHF 15 | - | total spend / new users |
| Organic vs Paid | - | - | |

## Formation Clusters
| Metric | Target | Actual | Notes |
|--------|--------|--------|-------|
| Formation-ready Clusters | 10+ | - | 3+ households, willing to form |
| Communities in DSO Process | 3-5 | - | |
| Communities Formed | - | - | |

## Traffic Sources
| Source | Visits | Registrations | Conversion |
|--------|--------|---------------|------------|
| Direct | - | - | - |
| Referral Links | - | - | - |
| Social Media | - | - | - |
| Installer Partners | - | - | - |
| Flyers/QR Codes | - | - | - |

## Month 1 Targets (50-75 users)
- [ ] PostgreSQL + SMTP operational
- [ ] 50-75 registered users
- [ ] Email confirmation rate >60%
- [ ] <CHF 20 cost per acquisition
- [ ] 2 installer partnerships confirmed

## Month 3 Targets (300-350 users)
- [ ] 250-350 registered users
- [ ] 10+ formation-ready clusters identified
- [ ] 2-3 communities in formation process
- [ ] Regionalwerke meeting scheduled
- [ ] <CHF 12 cost per acquisition

## Month 6 Targets (400-500 users)
- [ ] 400-500 registered users
- [ ] 15-20 communities in formation
- [ ] 5+ communities reached DSO approval
- [ ] Regionalwerke relationship established
- [ ] Revenue: CHF 5-15K from formations

## 80% Probability Scorecard (Target: 12/15 by Month 6)

### Market Validation (5 points)
- [ ] 300+ registered addresses by Month 3
- [ ] 400-500 registered addresses by Month 6
- [ ] 10+ formation-ready clusters
- [ ] 3-5 communities in DSO approval process
- [ ] <CHF 15 cost per acquisition

### Relationship Building (4 points)
- [ ] First meeting with Regionalwerke by Month 4
- [ ] Pilot or partnership discussion initiated
- [ ] Positive stakeholder relationships (2+ contacts)
- [ ] Access to their resources

### Platform Readiness (3 points)
- [ ] PostgreSQL + SMTP operational
- [ ] Stage 2 Formation Wizard MVP built
- [ ] Technical documentation complete

### Strategic Positioning (3 points)
- [ ] Formation success stories (2-3 documented)
- [ ] Media coverage (1+ article)
- [ ] Independent revenue (CHF 5-15K)

**Current Score: ___/15**

## Notes
_Weekly observations, blockers, wins, and learnings_

---

## API Endpoints for Metrics

```bash
# Get public stats
curl https://badenleg.ch/api/stats/public

# Get referral leaderboard
curl https://badenleg.ch/api/referral/leaderboard

# Admin: Full stats (requires ADMIN_TOKEN)
curl -H "X-Admin-Token: YOUR_TOKEN" https://badenleg.ch/admin/dashboard
```
