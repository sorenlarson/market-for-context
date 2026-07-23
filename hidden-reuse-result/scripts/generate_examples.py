#!/usr/bin/env python3
"""Generate the worked examples quoted in the documentation."""

import json
import sys
from dataclasses import asdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "src"
if str(SOURCE) not in sys.path:
    sys.path.insert(0, str(SOURCE))

from hidden_reuse import HiddenReusePrimitives, solve_hidden_reuse  # noqa: E402


SCENARIOS = [
    (
        "withholding",
        "Weak enforcement, no market for learning rights, expensive integration",
        HiddenReusePrimitives(
            enforcement_capacity=0.20,
            integration_cost=0.80,
            context_payment_cap=0.00,
        ),
    ),
    (
        "priced_reuse",
        "Weak enforcement, but the provider can pay for learning rights",
        HiddenReusePrimitives(
            enforcement_capacity=0.20,
            integration_cost=0.80,
            context_payment_cap=0.15,
        ),
    ),
    (
        "secure_modularity",
        "Enforcement is strong enough to make non-reuse incentive compatible",
        HiddenReusePrimitives(
            enforcement_capacity=0.40,
            integration_cost=0.40,
            context_payment_cap=0.00,
        ),
    ),
]


def serialize_example(name, description, primitives):
    outcome = solve_hidden_reuse(primitives, disclosure_grid_size=401)
    return {
        "name": name,
        "description": description,
        "changed_primitives": {
            "enforcement_capacity": primitives.enforcement_capacity,
            "integration_cost": primitives.integration_cost,
            "context_payment_cap": primitives.context_payment_cap,
        },
        "outcome": {
            "regime": outcome.regime.value,
            "agreement": outcome.agreement,
            "disclosure": outcome.disclosure,
            "monitoring": outcome.monitoring,
            "reuse": outcome.reuse,
            "transfer_to_provider": outcome.transfer_to_provider,
            "owner_payoff": outcome.owner_payoff,
            "provider_payoff": outcome.provider_payoff,
            "provider_reuse_gain_before_enforcement": (
                outcome.provider_reuse_gain_before_enforcement
            ),
            "required_monitoring_to_deter": outcome.required_monitoring_to_deter,
            "period_two_route": (
                outcome.continuation.route.value if outcome.continuation else "none"
            ),
        },
    }


def markdown_table(examples):
    lines = [
        "# Generated worked examples",
        "",
        "These values are generated from the model at a 401-point disclosure grid.",
        "",
        "| Scenario | Regime | Disclosure | Monitoring | Reuse | Transfer to provider |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for example in examples:
        outcome = example["outcome"]
        lines.append(
            "| {name} | {regime} | {disclosure:.3f} | {monitoring:.3f} | "
            "{reuse:.3f} | {transfer:.3f} |".format(
                name=example["name"],
                regime=outcome["regime"],
                disclosure=outcome["disclosure"],
                monitoring=outcome["monitoring"],
                reuse=outcome["reuse"],
                transfer=outcome["transfer_to_provider"],
            )
        )
    lines.extend(
        [
            "",
            "A negative transfer means the provider pays the context owner.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    output_dir = REPO_ROOT / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    examples = [
        serialize_example(name, description, primitives)
        for name, description, primitives in SCENARIOS
    ]
    payload = {
        "result_status": "calibrated theoretical computation; not empirical evidence",
        "baseline": asdict(HiddenReusePrimitives()),
        "examples": examples,
    }
    (output_dir / "worked-examples.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "worked-examples.md").write_text(
        markdown_table(examples), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
