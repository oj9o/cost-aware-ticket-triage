# Decisions behind the policy

## Optimize the decision, not just the label

A rare critical ticket can cost far more than many easy tickets save. The model supplies probabilities; the router evaluates every desk with the instructor's expected-cost function. Customer multipliers apply to mistake and SLA penalties, while labor and expert fees remain fixed.

## Treat expert answers as evidence

The expert is less reliable for some customer segments and for critical tickets. A transition matrix encodes the published neighboring-severity errors. Before purchase, the policy averages the best achievable desk cost over possible answers and adds the fee. After purchase, Bayes' rule combines the answer with model probabilities instead of treating it as certain truth. The remaining-call budget is checked explicitly.

## Select useful training labels

Pool selection combines entropy, customer cost scale, and expert reliability. A portion of the budget covers each segment; the remainder follows the score. Returned values are zero-based row positions. Free weak labels are deliberately unused to avoid reinforcing unvalidated confident errors. Separate segment models are also unused because the global fit shares limited data across groups.

## Guard against a known operational shift

The published outage scenario identifies regional network failures even when outage flags are missing. The revised policy multiplies regional critical probability by three, renormalizes, and evaluates expected desk costs using queues. A final guard escalates automated decisions to a generalist for complex regional tickets affecting at least 100 users. Live expert queries are now permitted for outage tickets when their expected value exceeds the fee. This replaces the earlier unconditional specialist referral, reducing queue penalties at the expense of more critical misses.

## Evidence and limitations

The policy was implemented before scoring the supplied practice and outage days. The first version preceded scoring. This revision was evaluated after the official days had been observed; validation seeds 903/904 compared candidates and seed 905 was checked after selection. Probabilities are not guaranteed calibrated under arbitrary shifts. Expert reliability follows the lab specification rather than an independently estimated noise model. Offline label selection is a heuristic, not an optimal acquisition policy.

Reference verification covered budgets, unique positional indices, repeatable selection, valid actions, exhausted live-expert budgets, missing outage flags, starter improvement on both days, and preservation of instructor source files. All outcomes are from a deterministic synthetic teaching simulator, not a production deployment.
