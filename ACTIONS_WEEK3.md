# Week 3 Action Plan (Feb 17 - Feb 23, 2026)

## Objectives
- Accelerate registrations beyond 100 with targeted campaigns.
- Launch referral promo + leaderboards to lift viral coefficient.
- Begin street-level targeting experiments for Baden clusters.

## Prioritized Tasks
1) Marketing Blitz (12h)
   - Increase FB/IG budget to CHF 150/day; run 5 ad creatives (energy savings, neighbor angle, compliance urgency, installer co-brand, leaderboard).
   - Add UTM tagging + GA4 events for campaign/source; verify in real time.
   - Launch Instagram story ads with swipe-up to landing.
2) Referral Campaign (8h)
   - Implement "CHF 50 + CHF 50" incentive banner on dashboard/home.
   - Add weekly top-referrer shout-out email; extend `/api/referral/leaderboard` UI snippet on homepage.
   - Create social share images (square + story) in Canva.
3) Street Targeting (6h)
   - Identify 10 streets with 2–3 partial clusters; craft localized ad copy and flyer PDFs.
   - Pilot flyer drop or door-to-door for 20 houses; track conversions via QR with `?src=street-{name}`.
4) WhatsApp Groups (4h)
   - Create template welcome message + rules; seed 2 groups from highest-interest clusters.
   - Assign light moderation schedule (15 min/day).
5) Metrics & QA (2h)
   - Review Week 2 KPIs: new regs, verification rate, referral rate, CPC/CPA; decide keep/kill creatives.
   - Deploy incremental fixes Friday; smoke-test registration → email → dashboard flow.

## Success Criteria (by Feb 23)
- 100+ total registrations
- ≥20% referral rate
- CAC (paid) ≤ CHF 25
- At least 2 streets show uplift from localized copy

## Risks & Mitigations
- Ad disapprovals → keep 2 spare creatives ready; tone down energy savings claims.
- Low referral uptake → move incentive to hero + post-registration modal; send reminder email.
- Tracking gaps → manual GA4 debug view each morning; fall back to server-side logging in `app.py` if GA fails.

## Owners & Timeboxes
- Marketing ops: 12h (Mon/Tue)
- Referral UI/banners: 4h (Wed)
- Canva assets + share images: 4h (Wed)
- Street targeting research: 3h (Thu)
- Flyers/QR + pilot drop: 3h (Sat)
- QA/metrics: 2h (Fri)

## Dependencies
- Live counter and public stats endpoint (done).
- `db.get_referral_leaderboard` available; need homepage widget.
- GA4 ID configured in env.

## Notes
- Keep German-only copy; stay within compliance claims (<CHF 800/yr savings, cite as estimate).
- Use `?ref=` and `?src=` params consistently for attribution.
