#!/usr/bin/env python3
"""Solve one hidden-value capability-pricing scenario and print JSON."""

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
    HiddenReusePrimitives,
    PledgeabilityPrimitives,
    solve_with_pledgeability,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-value", type=float)
    parser.add_argument("--verifiable-share", type=float, default=0.10)
    parser.add_argument("--collateral", type=float, default=0.02)
    parser.add_argument("--value-log-sigma", type=float, default=0.80)
    parser.add_argument("--bilateral-owner-capture", type=float, default=0.50)
    parser.add_argument("--enforcement", type=float, default=0.20)
    parser.add_argument("--integration-cost", type=float, default=0.80)
    parser.add_argument("--disclosure-grid", type=int, default=401)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    hidden = HiddenReusePrimitives(
        enforcement_capacity=args.enforcement,
        integration_cost=args.integration_cost,
    )
    pricing = PledgeabilityPrimitives(
        expected_net_capability_value=args.expected_value,
        verifiable_share=args.verifiable_share,
        collateral=args.collateral,
        value_log_sigma=args.value_log_sigma,
        bilateral_owner_capture=args.bilateral_owner_capture,
    )
    result = solve_with_pledgeability(
        hidden,
        pricing,
        disclosure_grid_size=args.disclosure_grid,
    )
    payload = {
        "inputs": {
            "hidden_reuse": asdict(hidden),
            "pledgeability": asdict(pricing),
        },
        "pricing": asdict(result.pricing),
        "governance": {
            **asdict(result.governance),
            "regime": result.governance.regime.value,
            "continuation": (
                {
                    **asdict(result.governance.continuation),
                    "route": result.governance.continuation.route.value,
                }
                if result.governance.continuation
                else None
            ),
        },
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
