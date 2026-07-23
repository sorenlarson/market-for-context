#!/usr/bin/env python3
"""Solve one homogeneous firm-size scenario and print JSON."""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src"
if str(SOURCE) not in sys.path:
    sys.path.insert(0, str(SOURCE))

from hidden_reuse import (  # noqa: E402
    FirmSizePrimitives,
    HiddenReusePrimitives,
    PledgeabilityPrimitives,
    derive_owner_internalization_advantage,
    solve_firm_size,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--internalization-advantage", type=float, default=0.65)
    parser.add_argument("--shared-fixed-cost", type=float, default=1.50)
    parser.add_argument("--cross-node-learning", type=float, default=0.35)
    parser.add_argument("--learning-saturation", type=float, default=4.00)
    parser.add_argument("--integration-cost", type=float, default=0.50)
    parser.add_argument("--integration-elasticity", type=float, default=0.65)
    parser.add_argument("--organization-cost", type=float, default=0.015)
    parser.add_argument("--organization-elasticity", type=float, default=1.40)
    parser.add_argument("--advantage-dilution", type=float, default=0.00)
    parser.add_argument("--max-firm-size", type=int, default=60)
    parser.add_argument("--derive-advantage-from-hidden-reuse", action="store_true")
    parser.add_argument("--enforcement", type=float, default=0.20)
    parser.add_argument("--verifiable-share", type=float)
    parser.add_argument("--collateral", type=float, default=0.00)
    parser.add_argument("--disclosure-grid", type=int, default=401)
    parser.add_argument("--include-profile", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    bridge = None
    advantage = args.internalization_advantage
    if args.derive_advantage_from_hidden_reuse:
        pricing = (
            PledgeabilityPrimitives(
                verifiable_share=args.verifiable_share,
                collateral=args.collateral,
            )
            if args.verifiable_share is not None
            else None
        )
        bridge = derive_owner_internalization_advantage(
            HiddenReusePrimitives(enforcement_capacity=args.enforcement),
            pricing,
            disclosure_grid_size=args.disclosure_grid,
        )
        advantage = bridge.internalization_advantage

    primitives = FirmSizePrimitives(
        internalization_advantage=advantage,
        shared_fixed_cost=args.shared_fixed_cost,
        cross_node_learning=args.cross_node_learning,
        learning_saturation=args.learning_saturation,
        integration_cost_scale=args.integration_cost,
        integration_cost_elasticity=args.integration_elasticity,
        organization_cost_scale=args.organization_cost,
        organization_cost_elasticity=args.organization_elasticity,
        advantage_dilution_elasticity=args.advantage_dilution,
        max_firm_size=args.max_firm_size,
    )
    outcome = solve_firm_size(primitives)
    payload = {
        "inputs": asdict(primitives),
        "bridge": (
            {
                **asdict(bridge),
                "modular_regime": bridge.modular_regime.value,
            }
            if bridge is not None
            else None
        ),
        "outcome": {
            "regime": outcome.regime.value,
            "integrates": outcome.integrates,
            "equilibrium_firm_size": outcome.equilibrium_firm_size,
            "conditional_target_size": outcome.conditional_target_size,
            "co_maximizing_sizes": outcome.co_maximizing_sizes,
            # None when dilution is positive: the continuous benchmark is a
            # zeta = 0 construct.
            "continuous_target_size": (
                outcome.continuous_target_size
                if outcome.continuous_target_size == outcome.continuous_target_size
                else None
            ),
            "integration_threshold": outcome.integration_threshold,
            "internalization_advantage": outcome.internalization_advantage,
            "per_node_surplus_at_target": outcome.per_node_surplus_at_target,
            "total_surplus_at_target": outcome.total_surplus_at_target,
            "industry_boundary_binding": outcome.industry_boundary_binding,
        },
    }
    if args.include_profile:
        payload["profile"] = [asdict(point) for point in outcome.profile]
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
