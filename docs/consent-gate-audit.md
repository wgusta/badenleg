# Consent gate audit (#518)

Every query whose output another resident can see, its gate, and the
mutation proof that the gate is load-bearing. The gate itself is correct as
documented and unchanged by this audit: an inner join on
`consents.share_with_neighbors = TRUE`, so a building without a consent row
is excluded (fail closed), and a count uses conditions identical to its list.

The consent semantic is judged by `tests/consent_visibility.py`
(`filters_by_consent`), not by substring matching; the query-shape contract
lives in `tests/test_consent_visibility.py`.

## Inventory

| # | Query (module) | Resident-visible output | Consumers | Gate |
|---|---|---|---|---|
| 1 | `store.building.get_all_buildings` (both `city_id` branches) | Map of neighbour buildings (`building_id`, lat/lon, type) | `neighbor_view.py` resident view | inner join + predicate, both branches |
| 2 | `store.building.get_all_building_profiles` (both branches) | Neighbour addresses, consumption, PV potential | `neighbor_view.py`, `clustering_run.py` billing | inner join + predicate, both branches |
| 3 | `store.building.get_neighbor_count_near` (both branches) | Count of visible neighbours | resident dashboard readiness | inner join + predicate, both branches; count conditions identical to the list in #1 |
| 4 | `store.formation.fetch_nearby_consenting_neighbours` | Candidate neighbours for a formation nudge | `formation_wizard` | inner join + predicate |
| 5 | `store.formation.fetch_community_with_members` | Member addresses and emails inside one community | community status view | inner join on `cns.share_with_neighbors = TRUE`; a member without a consent row drops out of the aggregate (fail closed) |
| 6 | `store.formation.fetch_user_communities` (`member_count` subquery) | Community size shown to a member | `fetch_user_communities` consumers | subquery inner-joins consents with the same predicate as the list in #5 |
| 7 | `store.referral.get_referral_leaderboard` (both branches) | Street names with referral counts | referral leaderboard | inner join + predicate, both branches |

## Unconsumed surfaces

- `street_stats` (table, `store/schema.py`) has no readers or writers in the
  codebase. It is not a query, so nothing to gate; it is a deletion candidate
  for a schema-cleanup ticket rather than a finding to harden.
- No resident-visible query was found without a consumer; nothing was deleted
  in this audit.

## Not in scope (checked, not gated)

- `get_building`, `get_building_for_dashboard`, `get_building_by_email`,
  `get_referral_stats`, `get_referral_code`: self-views (a member reading
  their own record) or internal seams, never another resident's output.
- `get_operator_building_profiles`: operator-only by contract, its docstring
  forbids resident-visible use; gated surfaces must not be widened to it.
- Metering and billing reads carry their own consent gates, pinned by
  `tests/test_neighbor_view_privacy.py` (#509) and the metering tickets; this
  audit is the neighbour-consent surface only.

## Mutation proof (gate broken, suite red, gate restored, suite green)

Each mutation replaced the query's `share_with_neighbors = TRUE` predicate
with `TRUE` inside the one function, ran the pinning tests, recorded the red
output, then reverted the file and re-ran green.

| # | Query | Pinning tests | Red output | Green after revert |
|---|---|---|---|---|
| 1 | `get_all_buildings` | `tests/test_database_helpers.py` | `test_neighbor_queries_exclude_revoked_and_missing_consent`, `test_neighbor_queries_keep_consented_buildings_and_city_scope` FAILED (2 failed, 6 passed) | `test_database_helpers.py` 8 passed |
| 2 | `get_all_building_profiles` | `tests/test_neighbor_view_privacy.py` | `test_building_profiles_read_excludes_revoked_and_missing_consent`, `test_the_city_scoped_read_is_gated_too` FAILED (2 failed, 36 passed) | `test_neighbor_view_privacy.py` 38 passed |
| 3 | `get_neighbor_count_near` | `tests/test_database_helpers.py` | same two tests FAILED (2 failed, 35 passed incl. neighbour-view file) | 8 passed |
| 4 | `fetch_nearby_consenting_neighbours` | `tests/test_formation_nudge.py` | `test_neighbour_search_filters_by_consent_in_the_query` FAILED (1 failed, 33 passed) | 34 passed |
| 5 | `fetch_community_with_members` | `tests/test_store_formation.py` | `test_fetch_community_with_members_reads_the_aggregate` FAILED (assertion shows `AND TRUE` in the captured SQL, 1 failed, 68 passed) | 69 passed |
| 6 | `fetch_user_communities` | `tests/test_store_formation.py` | `test_fetch_user_communities_reads_the_membership_rows` FAILED (1 failed, 42 passed) | 43 passed |
| 7 | `get_referral_leaderboard` | `tests/test_store_referral.py` | `test_leaderboard_excludes_revoked_and_missing_consent`, `test_leaderboard_keeps_city_scope_and_limit` FAILED (2 failed, 4 passed) | 6 passed |

Every row's red output came from the suite that pins that query; no query
needed a new test to become catchable, so none was added here.
