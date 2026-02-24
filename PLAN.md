# OpenLEG Implementation Plan

## Goal
Execute open-strategy.md using OpenClaw (LEA) as primary autonomous driver. TDD everything. Deploy incrementally.

---

## LLM Model Strategy for OpenClaw

**Current:** groq/qwen3-32b (primary), groq/llama-3.3-70b (fallback)

**Recommendation:** Keep qwen3-32b for tool calling/operations. Add a second model config for long-form generation tasks:

| Task Type | Model | Why |
|-----------|-------|-----|
| Tool calling, DB ops, research | groq/qwen3-32b | Best structured output on Groq free tier |
| Long text generation (outreach emails, docs) | groq/llama-3.3-70b | Better German prose, larger context |
| Code generation | Delegated to Claude Code / Codex | Not OpenClaw's job |

No model change needed. Current config is optimal for Groq free tier.

---

## What YOU (Human) Must Do

These cannot be automated:

1. **Stripe account**: Create Stripe account, get API keys (test + live), add to `.env` on VPS
2. **DeepSign account**: Register at deepsign.ch, get API credentials, add to `.env`
3. **Redis**: No action needed, we add it to docker-compose
4. **WeasyPrint**: No action needed, we add it to Dockerfile
5. **First sales calls**: LEA prepares outreach drafts, YOU make the calls
6. **Legal review**: LEA generates Gemeinschaftsvereinbarung template, YOU get lawyer sign-off
7. **Domain DNS**: `insights.openleg.ch` A record to 83.228.223.66 (if not already set)

---

## Phases (TDD, incremental deploy)

### Phase A: Housekeeping + Commit Untracked (Day 1)
1. Commit `utility_portal.py` + `templates/utility/` (already working, just untracked)
2. Add `requirements-dev.txt` with pytest deps
3. Run existing tests, ensure green baseline

### Phase B: PDF Document Generator (Day 1-2)
**Why first:** Formation wizard is 80% done but can't produce documents. This unblocks first pilot.

**Tests first:**
- `tests/test_document_generator.py`: test Gemeinschaftsvereinbarung PDF output, test Teilnehmervertrag fields, test DSO-Anmeldung format

**Implement:**
- Add `weasyprint` to requirements.txt
- Create `document_generator.py`: 3 templates (Gemeinschaftsvereinbarung, Teilnehmervertrag, DSO-Anmeldung)
- HTML templates in `templates/documents/` rendered to PDF via WeasyPrint
- Wire into formation_wizard.py

**OpenClaw upgrade:**
- New MCP tool: `generate_leg_document` (type, community_id) -> returns PDF URL
- New MCP tool: `list_documents` (community_id) -> lists generated docs

### Phase C: Billing Engine (Day 2-3)
**Why:** 15-min interval allocation is the core product differentiator.

**Tests first:**
- `tests/test_billing_engine.py`: test proportional allocation, test same-level 40% discount, test cross-level 20% discount, test edge cases (zero consumption, negative values)

**Implement:**
- Create `billing_engine.py`: takes 15-min smart meter readings, allocates solar production, calculates network discount, outputs per-participant bills
- DB tables: `billing_periods`, `allocations`, `invoices`

**OpenClaw upgrade:**
- New MCP tool: `run_billing_period` (community_id, period_start, period_end)
- New MCP tool: `get_billing_summary` (community_id, month)

### Phase D: Stripe Integration (Day 3-4)
**Why:** Can't charge customers without it.

**Tests first:**
- `tests/test_stripe_integration.py`: test checkout session creation, test webhook signature verification, test subscription lifecycle (create, update, cancel)

**Implement:**
- Add `stripe` to requirements.txt
- Create `stripe_integration.py`: checkout session, webhook handler, customer portal
- Routes: `/utility/billing`, `/webhook/stripe`
- DB: add `stripe_customer_id`, `stripe_subscription_id` to utility_clients table

**Human action:** Add STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET to .env

### Phase E: Multi-Format Smart Meter Parser (Day 4-5)
**Tests first:**
- `tests/test_meter_formats.py`: test EKZ CSV, test ewz CSV, test CKW SDAT-XML, test BKW format, test auto-detection

**Implement:**
- Extend `meter_data.py` with format auto-detection
- Add parsers: ewz, CKW, BKW, IWB, AEW
- Normalize all to common 15-min interval DataFrame

### Phase F: Sales Pipeline MCP Tools (Day 5-6)
**Why:** LEA needs these to autonomously manage VNB outreach.

**Tests first:**
- `tests/test_sales_pipeline.py`: test pipeline CRUD, test scoring, test outreach draft generation

**Implement:**
- DB tables: `vnb_pipeline` (vnb_name, status, score, notes, next_action, assigned_to)
- New MCP tools:
  - `get_vnb_pipeline` (status_filter) -> list pipeline entries
  - `update_vnb_status` (vnb_id, status, notes)
  - `score_vnb` (vnb_id) -> auto-score based on population, solar, competition gap
  - `draft_outreach` (vnb_id) -> generate personalized outreach email
  - `get_pipeline_dashboard` -> funnel metrics

**OpenClaw AGENTS.md update:**
- Add "Sales Pipeline Management" standing objective
- LEA checks pipeline daily, suggests next actions

### Phase G: Admin Pipeline Dashboard (Day 6)
**Implement:**
- Route: `/admin/pipeline`
- Template: `templates/admin/pipeline.html`
- Visual funnel: lead -> contacted -> demo -> trial -> paid -> churned
- Driven by vnb_pipeline table

### Phase H: DeepSign E-Signatures (Day 7)
**Tests first:**
- `tests/test_deepsign.py`: test document upload, test signature request, test webhook callback

**Implement:**
- Create `deepsign_integration.py`: upload PDF, request AES signature, handle callback
- Wire into formation_wizard.py: after document generation, send for signature

**Human action:** Add DEEPSIGN_API_KEY, DEEPSIGN_WEBHOOK_SECRET to .env

### Phase I: Redis + Hardening (Day 8)
**Implement:**
- Add redis service to docker-compose.yml
- Replace in-memory tenant cache with Redis
- Rate limiting backend: Redis instead of in-memory
- Session storage: Redis

### Phase J: Enterprise B2B API (Day 9-10)
**Tests first:**
- `tests/test_b2b_api.py`: expand existing tests for new endpoints

**Implement:**
- New endpoints: formation-pipeline, grid-optimization, community-benchmarks
- Tier enforcement: starter (3 endpoints), professional (all), enterprise (custom)

---

## OpenClaw Skill Upgrades Summary

New MCP tools to add to `server.mjs`:
1. `generate_leg_document` - PDF generation
2. `list_documents` - Document listing
3. `run_billing_period` - Billing calculation
4. `get_billing_summary` - Billing reports
5. `get_vnb_pipeline` - Sales pipeline read
6. `update_vnb_status` - Pipeline status update
7. `score_vnb` - Auto-scoring
8. `draft_outreach` - Email draft generation
9. `get_pipeline_dashboard` - Funnel metrics

Updated AGENTS.md directives:
- Daily pipeline review
- Weekly outreach draft queue
- Monthly billing reconciliation check

Updated SOUL.md:
- Add sales personality traits (consultative, data-driven pitching)
- Add billing domain knowledge

---

## Deploy Strategy

Each phase: write tests -> implement -> pytest green -> commit -> `bash deploy.sh`

After Phase F: LEA starts autonomous VNB research pipeline on production.

---

## Ralph Loop Integration

After each phase deploy:
1. LEA runs morning briefing (existing)
2. LEA reviews pipeline metrics (new, Phase F+)
3. LEA flags blockers, suggests priorities
4. Human reviews, approves outreach
5. Repeat

The Ralph Loop kicks off after Phase A commit, running continuously.

---

## Execution Order & Dependencies

```
A (housekeeping) -> B (PDF) -> C (billing) -> D (Stripe) -> E (meter formats)
                              \-> F (sales pipeline) -> G (dashboard)
                                                    \-> H (DeepSign)
                                                        I (Redis) -> J (B2B API)
```

B,C,D,E are serial (each builds on prior).
F can start parallel after B.
H depends on B (needs PDF generator).
I,J are independent hardening.
