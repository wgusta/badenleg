# Strategy Assessment

- Date: 2026-03-26
- Scope: Current OpenLEG strategy and implementation
- Method: First-principles review of repo docs, product surface, architecture, and test signal
- Status: Snapshot for later review

## Executive Summary

- Strongest asset: public Swiss energy data + API + municipality-level distribution
- Weakest trait: no single governing thesis across product, docs, and roadmap
- Current shape: `SEO publisher + resident network app + municipal/utility SaaS + internal AI ops + speculative Physical AI thesis`
- Recommendation: narrow to a single sequence and demote Physical AI to R&D until live LEG proof exists

## Findings

### 1. Strategy Fragmentation

- Severity: High
- Finding:
  - The repo does not present one stable product thesis.
  - Different surfaces describe materially different businesses.
- Evidence:
  - `README.md` positions OpenLEG as a LEG platform:
    - `README.md:5-14`
  - `research.md` records multiple pivots and marks parts of the prior strategy as stale:
    - `research.md:173-188`
  - Homepage sells free resident/municipality infrastructure:
    - `templates/index.html:121-135`
    - `templates/index.html:144-179`
  - Roadmap sells Physical AI and AI-governed infrastructure:
    - `templates/roadmap.html:19-27`
    - `templates/roadmap.html:44-61`
    - `templates/roadmap.html:100-121`
- First-principles implication:
  - One product needs one primary customer, one core pain, one success metric.
  - Right now the repo optimizes for several at once.

### 2. Real Moat Is Data/API, Not Workflow Breadth

- Severity: High
- Finding:
  - The most defensible part of the product is the public data ingestion and API exposure.
  - That appears more differentiated than the full workflow/UI stack.
- Evidence:
  - Public data ingestion:
    - `public_data.py:1-4`
    - `public_data.py:47-75`
    - `public_data.py:115-158`
    - `public_data.py:179-202`
  - Public API surface:
    - `api_public.py:61-172`
    - `api_public.py:178-268`
    - `api_public.py:274-420`
  - Public API docs exist:
    - `api_public.py:512-515`
    - `templates/api_docs.html:18-205`
- First-principles implication:
  - Proprietary value is coming from aggregation, normalization, and packaging of public Swiss energy data.
  - That is a clearer wedge than trying to fully own the whole LEG operating stack at once.

### 3. Execution Spread Exceeds Likely Capacity

- Severity: High
- Finding:
  - One Flask app currently owns most concerns: marketing site, citizen onboarding, admin, internal automation, formation, billing, cron, and metrics.
- Evidence:
  - Public site routes:
    - `app.py:664-779`
  - Admin/internal routes:
    - `app.py:930-1244`
  - Citizen signup and dashboards:
    - `app.py:1262-1799`
  - Formation lifecycle:
    - `app.py:1803-1932`
  - Cron/billing/ops:
    - `app.py:1936-2145`
- Supporting signal:
  - File size concentration:
    - `app.py` ~2152 LOC
    - `database.py` ~3710 LOC
- First-principles implication:
  - This is workable short-term, but every new bet increases coupling, regression surface, and decision overhead.
  - The strategic problem is not “nothing works”; it is that too many things are being worked at once.

### 4. Physical AI Is Currently Narrative + Heuristics, Not Core Product

- Severity: High
- Finding:
  - The current “Physical AI” layer is mostly optionality framing on top of LEG economics, not a distinct operational product.
- Evidence:
  - Pivot log:
    - `research.md:179-186`
  - Roadmap framing:
    - `templates/roadmap.html:19-27`
    - `templates/roadmap.html:44-61`
    - `templates/roadmap.html:77-109`
  - Surplus/compute logic is heuristic:
    - `public_data.py:409-460`
  - Financial model adds speculative compute/heat revenue assumptions:
    - `api_public.py:349-420`
  - Calculator surfaces “compute optionality” in UI:
    - `templates/leg_kalkulator.html:87-107`
    - `templates/leg_kalkulator.html:287-307`
  - Core LEG savings model remains simple/static:
    - `formation_wizard.py:922-983`
- First-principles implication:
  - This should be treated as R&D option value, not primary product positioning.
  - The market will trust this only after real LEG adoption and real surplus data exist.

### 5. Utility SaaS Story Is Only Partially Real

- Severity: Medium
- Finding:
  - The B2B utility portal exists, but not all promised capability is fully implemented.
- Evidence:
  - Strategy promise:
    - `open-strategy.md:82-89`
  - Utility portal shipped:
    - `utility_portal.py:53-115`
    - `utility_portal.py:121-179`
    - `utility_portal.py:185-202`
  - `/utility/settings` route exists but template is missing:
    - `utility_portal.py:208-212`
    - no `templates/utility/settings.html`
- First-principles implication:
  - The portal is real enough for a prototype/demo story.
  - It is not yet the clean, complete self-serve product the strategic copy implies.

### 6. Product Quality Signal Is Better Than Strategy Signal

- Severity: Medium
- Finding:
  - The codebase is not in obvious operational collapse.
  - Test coverage is substantial and mostly green.
- Evidence:
  - Local test run summary:
    - `675 passed`
    - `4 skipped`
    - `11 errors`
  - The `11` errors are from Playwright visual smoke setup trying to bind a local port:
    - `tests/test_visual_smoke.py:34-63`
- First-principles implication:
  - Implementation risk is secondary to positioning/focus risk.
  - The problem is prioritization, not lack of engineering effort.

### 7. One Concrete Product Gap

- Severity: Medium
- Finding:
  - There is at least one user-visible route that is not actually renderable.
- Evidence:
  - Missing utility settings template:
    - `utility_portal.py:208-212`
    - no `templates/utility/settings.html`
- First-principles implication:
  - This is a small bug, but symbolic of a broader issue: strategic claims are ahead of shipped completeness in some areas.

## Strengths

- Public Swiss energy data ingestion appears real and useful.
- Public API is broad, documented, and tested.
- Municipality/SEO distribution strategy is coherent as a top-of-funnel engine.
- Formation/billing/outreach layers are meaningful prototypes, not just mockups.
- Test signal is strong enough to support iteration.

## Core Risks

- Focus risk:
  - too many top-line stories competing for attention
- Trust risk:
  - roadmap language may outrun what is operationally true today
- Architecture risk:
  - monolith concentration increases change cost
- Distribution risk:
  - if SEO and public-data traffic do not convert into actual LEG activity, the stack becomes overbuilt lead scaffolding

## Recommendation

### Primary Recommendation

- Choose one operating sequence and enforce it across docs, product copy, roadmap, and implementation:
  - `public data/API + SEO`
  - `resident demand capture`
  - `first active LEGs`
  - `municipality case studies`
  - `paid support / managed deployment`

### What To De-Emphasize

- Demote Physical AI from primary positioning to R&D / future optionality.
- Keep it in roadmap/research, but stop letting it dominate the main product narrative until:
  - live LEGs exist
  - real surplus data exists
  - at least one pilot path is concrete

### What To Treat As The Core Product

- Core product:
  - open municipal energy intelligence
  - LEG discovery / savings / transparency tooling
  - resident demand capture
  - municipality enablement
- Secondary product:
  - utility SaaS / managed services
- Tertiary product:
  - compute / Physical AI experimentation

### Architecture Recommendation

- Refactor by boundary, not by feature:
  - `public-data-api`
  - `public-web`
  - `ops-internal`
- Keep the monolith if needed operationally, but make these boundaries explicit in module ownership and future extraction.

## Immediate Next Moves

- Align top-level docs:
  - update `README.md`
  - replace stale B2B framing with current primary sequence
- Align public messaging:
  - reduce Physical AI prominence on primary conversion pages
- Fix visible product gaps:
  - add or remove `/utility/settings`
- Define one north-star metric:
  - recommended: `active LEG formations` or `municipalities with verified resident demand`
- Decide whether OpenLEG is primarily:
  - a public infrastructure project
  - a lead-gen/data platform
  - a municipality enablement product
  - a utility SaaS business
  - Do not market all four equally

## Merge-Readiness View Of Strategy

- Asset quality: Strong
- Product completeness: Moderate
- Strategic coherence: Weak
- Recommendation status: Re-focus before adding major new surface area

## Short Conclusion

- Net assessment:
  - strong asset
  - credible implementation
  - weak strategic focus
- Highest-leverage move:
  - narrow the story to what is already genuinely strongest and most defensible
