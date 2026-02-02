# Week 5 Action Plan (Mar 3 - Mar 9, 2026)

## Objectives
- Ship formation wizard MVP (UI over existing backend) and start 5 pilot communities.
- Draft legal document templates and wire PDF generation skeleton.
- Maintain growth momentum to 300 registrations.

## Prioritized Tasks
1) Formation Wizard UI (14h)
   - Build `/formation/start` page with multi-step flow (address confirm → members list → invites → summary).
   - Connect to backend endpoints in `formation_wizard.py`; handle tokens & status polling.
   - Add minimal validation + loading/error states; German copy only.
2) Invitations & Tokens (4h)
   - Email invite template with magic link token; endpoint for `/formation/accept/<token>`.
   - Capture acceptance + role (admin/member); display counts in community dashboard.
3) Document Pipeline Draft (6h)
   - Set up WeasyPrint (or fallback xhtml2pdf) scaffold; create HTML base template and stub data mapping.
   - Draft German text blocks for community agreement + participant contract (placeholder legal review).
4) Pilot Community Activation (4h)
   - Choose 5 clusters from Week 4 list; manual outreach to schedule kickoff calls.
   - White-glove support via phone/WhatsApp; log feedback/issues.
5) Metrics & QA (2h)
   - Regression test reg → verify → wizard start; ensure errors logged.
   - Track pilot funnel separately (spreadsheet if faster).

## Success Criteria (by Mar 9)
- Wizard UI deployed and usable end-to-end for pilots
- 5 pilot communities created, invites sent
- Draft PDFs generated (even if rough) for at least 2 pilots
- 300+ total registrations

## Risks & Mitigations
- PDF tooling issues → fallback to simple HTML-to-PDF via `pdfkit` + wkhtmltopdf container.
- Pilot drop-off → personal follow-up within 24h; offer to fill data for them.
- Backend gaps → patch `formation_wizard.py` quickly; log any missing fields.

## Owners & Timeboxes
- Wizard UI: 14h (Tue-Thu)
- Invites + email template: 4h (Thu)
- PDF scaffold: 6h (Fri)
- Pilot outreach/support: 4h (Wed/Fri)
- QA/metrics: 2h (Fri)

## Dependencies
- Working email sender (SendGrid key in env).
- Stable `formation_wizard.py` endpoints.
- Address & member data quality from DB.

## Notes
- Optimize for pilots, not polish; hardcode copy where faster.
- Keep logs verbose for pilot flow to debug quickly.
