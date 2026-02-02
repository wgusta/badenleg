# Week 4 Action Plan (Feb 24 - Mar 1, 2026)

## Objectives
- Reach 200 registrations and prepare formation wizard MVP handoff.
- Harden referral & email automation based on prior weeks' data.
- Set up initial pilot community selection criteria.

## Prioritized Tasks
1) A/B Testing & Conversion (10h)
   - Implement headline rotation (3 variants) with server-side bucketing; track conversions by variant.
   - Add CTA placement test (top vs mid vs bottom button) and measure CTR.
2) Email Nurture Iteration (6h)
   - Add Day 7 consumption + Day 14 formation nudges; dynamic snippets using nearest-cluster count.
   - Re-engagement email for non-verified signups after 72h.
3) Referral & Leaderboard Polish (6h)
   - Add homepage leaderboard section (top 5 anonymized streets) pulling `/api/referral/leaderboard`.
   - Weekly referral winner banner + email; reset counter weekly while keeping lifetime tally in DB.
4) Pilot Community Prep (6h)
   - Define "ready" cluster rule (≥4 verified, same transformer/zip); create admin query to list candidates.
   - Outreach template for pilot invite; schedule 5 calls for Week 5.
5) Metrics & QA (2h)
   - Review funnel: visit→reg, reg→verify, verify→profile completion; flag weak step and patch.

## Success Criteria (by Mar 1)
- 200+ total registrations
- ≥30% profile completion
- ≥15% referral rate sustained
- 5 pilot candidates identified with contact emails confirmed

## Risks & Mitigations
- Variant underperforms → kill after 500 sessions; revert to control.
- Low email engagement → subject-line tests + resend to non-openers.
- Data quality for pilots → manual email/phone verification for candidate clusters.

## Owners & Timeboxes
- Experiment framework: 6h (Mon)
- Email content + logic: 4h (Tue)
- Leaderboard UI: 4h (Wed)
- Pilot selection query + outreach: 4h (Thu)
- QA/metrics: 2h (Fri)

## Dependencies
- GA4 events per variant; ensure `variant_id` sent.
- `/api/referral/leaderboard` live.
- DB has address/zip fields for clustering.

## Notes
- Keep experiments simple; avoid heavy FE libraries.
- All copy in German; keep claims conservative.
