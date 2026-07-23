#!/usr/bin/env python3
"""Solve and print one hidden-reuse scenario."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src"
if str(SOURCE) not in sys.path:
    sys.path.insert(0, str(SOURCE))

from hidden_reuse import HiddenReusePrimitives, solve_hidden_reuse  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Solve one two-period hidden-reuse contract."
    )
    parser.add_argument("--enforcement", type=float, default=0.45)
    parser.add_argument("--integration-cost", type=float, default=0.70)
    parser.add_argument("--payment-cap", type=float, default=0.00)
    parser.add_argument("--provider-outside-gain", type=float, default=0.45)
    parser.add_argument("--monitoring-cost", type=float, default=0.25)
    parser.add_argument("--owner-reuse-loss", type=float, default=0.75)
    parser.add_argument("--disclosure-grid", type=int, default=401)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    primitives = HiddenReusePrimitives(
        enforcement_capacity=args.enforcement,
        integration_cost=args.integration_cost,
        context_payment_cap=args.payment_cap,
        provider_outside_gain=args.provider_outside_gain,
        monitoring_cost=args.monitoring_cost,
        owner_reuse_loss=args.owner_reuse_loss,
    )
    outcome = solve_hidden_reuse(primitives, disclosure_grid_size=args.disclosure_grid)
    payload = {
        "result_status": "calibrated theoretical computation; not empirical evidence",
        "inputs": {
            "enforcement_capacity": args.enforcement,
            "integration_cost": args.integration_cost,
            "context_payment_cap": args.payment_cap,
            "provider_outside_gain": args.provider_outside_gain,
            "monitoring_cost": args.monitoring_cost,
            "owner_reuse_loss": args.owner_reuse_loss,
            "disclosure_grid_size": args.disclosure_grid,
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
            "payment_cap_binding": outcome.payment_cap_binding,
            "period_two_route": (
                outcome.continuation.route.value if outcome.continuation else "none"
            ),
        },
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
