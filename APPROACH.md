# Decisions behind the policy

## Optimize the decision, not just the label

A rare critical ticket can cost far more than many easy tickets save. The model supplies probabilities; the router evaluates every desk with the instructor's expected-cost function. Customer multipliers apply to mistake and SLA penalties, while labor and expert fees remain fixed.

## Treat expert answers as evidence

The expert is less reliable for some customer segments and for critical tickets. A transition matrix encodes the published neighboring-severity errors. Before purchase, the policy averages the best achievable desk cost over possible answers and adds the fee. After purchase, Bayes' rule combines the answer with model probabilities instead of treating it as certain truth. The remaining-call budget is checked explicitly.

## Select useful training labels

Pool selection combines entropy, customer cost scale, and expert reliability. A portion of the budget covers each segment; the remainder follows the score. Returned values are zero-based row positions. Free weak labels are deliberately unused to avoid reinforcing unvalidated confident errors. Separate segment models are also unused because the global fit shares limited data across groups.

## Guard against a known operational shift

The published outage scenario identifies regional network failures, including missing outage flags. A final business rule sends matching symptoms to specialists. This makes the rule interpretable, but it can overload scarce capacity. The reported queue and SLA deterioration is part of the result, not a hidden caveat.

## Evidence and limitations

The policy was implemented before scoring the supplied practice and outage days. Those days were not used to tune the policy, but they have now been observed; a new optimization should use a distinct validation procedure and a fresh holdout. Probabilities are not guaranteed calibrated under arbitrary shifts. Expert reliability follows the lab specification rather than an independently estimated noise model. Offline label selection is a heuristic, not an optimal acquisition policy.

Reference verification covered budgets, unique positional indices, repeatable selection, valid actions, exhausted live-expert budgets, missing outage flags, starter improvement on both days, and preservation of instructor source files. All outcomes are from a deterministic synthetic teaching simulator, not a production deployment.
