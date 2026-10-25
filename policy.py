"""AI-assisted MAAI7101 Lab 9 policy — Mouza Al Darmaki. Requires the instructor lab."""
from __future__ import annotations

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline

from lab import build_preprocessor, feature_columns, expected_action_cost


_LABELS = ("low", "normal", "high", "critical")
_ACTIONS = ("automate", "l1", "l2")


def build_models(train_df, seed):
    # Preserve the supplied reliability weights, including weak-label weights.
    model = Pipeline([
        ("prep", build_preprocessor(False)),
        ("model", HistGradientBoostingClassifier(
            max_iter=180, max_leaf_nodes=15, learning_rate=0.07,
            l2_regularization=2.0, min_samples_leaf=25,
            random_state=int(seed))),
    ])
    model.fit(train_df[feature_columns()], train_df["severity"].astype(str),
              model__sample_weight=train_df["sample_weight"])
    # Segment-only fits have little data; retain the shared global model.
    return {"global": model, "enterprise": None, "government": None}


def _prior(proba):
    values = proba.get("specialist") or proba
    p = np.array([float(values.get(k) or 0) for k in _LABELS])
    return p / p.sum() if p.sum() > 0 else np.full(4, 0.25)


def _expert_matrix(ticket):
    # Published expert reliability and adjacent-severity errors, P(answer|truth).
    accuracy = {"consumer": .93, "sme": .86, "enterprise": .74,
                "government": .67}[ticket["segment"]]
    matrix = np.zeros((4, 4))
    for i in range(4):
        correct = max(.35, accuracy - (.16 if i == 3 else 0))
        matrix[i, i] = correct
        neighbors = [j for j in (i-1, i+1) if 0 <= j < 4]
        for j in neighbors:
            matrix[i, j] = (1-correct) / len(neighbors)
    return matrix


def _costs(ticket, p, context):
    distribution = dict(zip(_LABELS, p))
    return np.array([expected_action_cost(distribution, ticket, context, a)
                     for a in _ACTIONS])


def choose_labels(pool_df, proba_df, budget, seed):
    # Cost-weighted uncertainty with segment diversity; positions, never IDs.
    rng = np.random.default_rng(int(seed))
    p = proba_df.loc[:, list(_LABELS)].to_numpy(dtype=float)
    entropy = -(p * np.log(np.maximum(p, 1e-12))).sum(axis=1)
    multiplier = pool_df["segment"].map(
        {"consumer": 1., "sme": 2.4, "enterprise": 7., "government": 11.}).to_numpy()
    reliability = pool_df["segment"].map(
        {"consumer": .93, "sme": .86, "enterprise": .74, "government": .67}).to_numpy()
    priority = entropy * np.sqrt(multiplier) * reliability + rng.uniform(0, 1e-9, len(p))
    count = min(max(0, int(budget)), len(pool_df))
    picked = []
    for segment in ("consumer", "sme", "enterprise", "government"):
        positions = np.flatnonzero(pool_df["segment"].to_numpy() == segment)
        ranked = positions[np.argsort(-priority[positions])]
        picked.extend(ranked[:count // 8].tolist())
    taken = set(picked)
    for i in np.argsort(-priority):
        if len(picked) >= count:
            break
        if int(i) not in taken:
            picked.append(int(i)); taken.add(int(i))
    # Avoid reinforcing confident errors through unvalidated pseudo-labels.
    return {"oracle_indices": picked, "weak_indices": []}


def wants_oracle(ticket, proba, context):
    if int(context.get("oracle_remaining", 0)) <= 0:
        return False
    p = _decision_prior(ticket, proba, context)
    joint = p[:, None] * _expert_matrix(ticket)
    after = 0.0
    for j in range(4):
        probability = joint[:, j].sum()
        if probability > 0:
            after += probability * _costs(ticket, joint[:, j]/probability, context).min()
    fee = float(context.get("economics", {}).get("oracle_cost", 32.0))
    return bool(_costs(ticket, p, context).min() > after + fee)


def route(ticket, proba, context):
    p = _decision_prior(ticket, proba, context)
    answer = context.get("oracle_label")
    if answer in _LABELS:
        posterior = p * _expert_matrix(ticket)[:, _LABELS.index(answer)]
        if posterior.sum() > 0:
            p = posterior / posterior.sum()
    return _ACTIONS[int(_costs(ticket, p, context).argmin())]


def _outage_ticket(ticket, context):
    return (bool(context.get("outage_mode"))
            and ticket.get("emirate") in ("sharjah", "northern")
            and ticket.get("symptom") in ("network_down", "slow_data"))


def _decision_prior(ticket, proba, context):
    p = _prior(proba)
    if _outage_ticket(ticket, context):
        # Conservative prior-shift adjustment, not an automatic specialist referral.
        # Fixed before evaluation; does not inspect hidden labels.
        p[3] *= 3.0
        p /= p.sum()
    return p


def apply_business_rules(ticket, action, context):
    # An outage flag can be missing. Prevent risky mass automation while allowing
    # the cost-aware route to reserve scarce specialists for likely criticals.
    if (_outage_ticket(ticket, context) and action == "automate"
            and float(ticket.get("affected_users", 0)) >= 100
            and float(ticket.get("complexity", 0)) > 0.55):
        return "l1"
    return action
