#!/usr/bin/env python3
"""Solve the two-type private-signal capability-pricing benchmark."""

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
    PrivateSignalPrimitives,
    solve_private_signal_pricing,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--low-value", type=float, default=0.15)
    parser.add_argument("--high-value", type=float, default=0.45)
    parser.add_argument("--high-probability", type=float, default=0.30)
    parser.add_argument("--verifiable-share", type=float, default=0.10)
    parser.add_argument("--collateral", type=float, default=0.02)
    parser.add_argument("--owner-access-cost", type=float, default=0.00)
    parser.add_argument("--value-log-sigma", type=float, default=0.80)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    primitives = PrivateSignalPrimitives(
        low_expected_value=args.low_value,
        high_expected_value=args.high_value,
        high_type_probability=args.high_probability,
        verifiable_share=args.verifiable_share,
        collateral=args.collateral,
        owner_access_cost=args.owner_access_cost,
        value_log_sigma=args.value_log_sigma,
    )
    result = solve_private_signal_pricing(primitives)
    payload = {
        "inputs": asdict(primitives),
        "outcome": {
            **asdict(result),
            "policy": result.policy.value,
        },
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
