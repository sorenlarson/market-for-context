#!/usr/bin/env python3
"""Solve one heterogeneous ownership-versus-access scenario."""

import argparse
import json
import sys
from dataclasses import asdict, replace
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "src"
if str(SOURCE) not in sys.path:
    sys.path.insert(0, str(SOURCE))

from hidden_reuse import solve_ownership_access, vertical_customer_network  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--learning-topology",
        choices=("complementary", "within_type"),
        default="complementary",
    )
    parser.add_argument("--external-learning-efficiency", type=float, default=0.65)
    parser.add_argument("--neutrality-penalty", type=float, default=0.10)
    parser.add_argument(
        "--fringe-customer-value",
        type=float,
        default=0.0,
        help=(
            "relationship value with unmodeled outside customers put at risk "
            "per owned asset; makes even a full rollup bear conflict cost"
        ),
    )
    parser.add_argument("--show-candidates", action="store_true")
    return parser.parse_args()


def candidate_dict(candidate) -> dict:
    result = asdict(candidate)
    result["regime"] = candidate.regime.value
    return result


def main() -> None:
    args = parse_args()
    primitives = vertical_customer_network(
        learning_topology=args.learning_topology,
        external_learning_efficiency=args.external_learning_efficiency,
        neutrality_penalty=args.neutrality_penalty,
    )
    if args.fringe_customer_value:
        primitives = replace(
            primitives,
            fringe_customer_value_per_owned_asset=args.fringe_customer_value,
        )
    outcome = solve_ownership_access(primitives)
    result = {
        "inputs": {
            "learning_topology": args.learning_topology,
            "external_learning_efficiency": args.external_learning_efficiency,
            "neutrality_penalty": args.neutrality_penalty,
            "fringe_customer_value_per_owned_asset": args.fringe_customer_value,
        },
        "regime": outcome.regime.value,
        "owned_names": outcome.owned_names,
        "ownership_size": outcome.ownership_size,
        "platform_learning_value": outcome.platform_learning_value,
        "incremental_value": outcome.incremental_value,
        "total_private_value": outcome.total_private_value,
        "selection_margin": outcome.selection_margin,
        "maximum_deviation_gain": outcome.maximum_deviation_gain,
        "value_decomposition": candidate_dict(outcome.chosen),
    }
    if args.show_candidates:
        result["candidates"] = [
            candidate_dict(candidate)
            for candidate in sorted(
                outcome.candidates,
                key=lambda candidate: candidate.incremental_value,
                reverse=True,
            )
        ]
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
