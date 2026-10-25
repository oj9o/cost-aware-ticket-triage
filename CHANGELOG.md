# Revision 2 — 25 October 2026

## What changed

- Replaced unconditional regional-outage specialist referral with expected-cost allocation and a fixed 3x regional critical-probability adjustment.
- Added a generalist guard for complex regional network tickets affecting at least 100 users.
- Enabled value-of-information expert purchases during the outage.
- Kept the weighted global HistGradientBoostingClassifier, active label selection, instructor API and prices unchanged.

## Before and after on the official outage day

Total simulated savings: AED 3,163,154 → AED 3,677,493 (+AED 514,339).
Savings per 1,000 tickets: AED 1,054,384.67 → AED 1,225,831.
SLA violations: 540 → 164. Critical misses: 4 → 9. Regional network critical misses: 0 → 5.
Practice-day results are unchanged. The new policy improves cost but sacrifices some critical-case coverage.

## Models compared

Selected: one global HistGradientBoostingClassifier for consumer, SME, enterprise and government.

Alternative: global HistGradientBoostingClassifier plus two separately fitted CatBoostClassifier experts, one for enterprise and one for government. Each expert retained all training examples with 3x weight on its segment; segment predictions blended global and expert probabilities equally. This is customer-segment routing, not arbitrary chronological batches.

The alternative saved AED 3,668,743 on the official outage day, below the selected policy's AED 3,677,493. On validation seeds 903/904 it also saved less: AED 3,522,643 / 3,076,399 versus AED 3,528,057 / 3,086,257. More models did not improve the measured objective in this comparison. The alternative is retained in the private lab archive, not used by policy.py.

## Independent check and limitations

After selection, new seed 905: previous policy saved AED 2,884,403; revised policy AED 3,381,216. Critical misses rose 3 → 13; SLA violations fell 525 → 175. Official evaluation days were already observed, so their improved score is not an untouched test estimate. All figures come from the teaching simulator. No hidden labels enter policy decisions; no claim of optimality or real deployment is made.
