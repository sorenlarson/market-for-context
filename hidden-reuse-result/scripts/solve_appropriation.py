#!/usr/bin/env python3
"""Solve one homogeneous access-versus-appropriation scenario."""

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
    CaptureShareFrictions,
    HomogeneousValueAppropriationPrimitives,
    derive_capture_shares,
    homogeneous_value_network,
    platform_rollup_capture_threshold,
    solve_value_appropriation,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--external-learning", type=float, default=0.55)
    parser.add_argument("--platform-capture", type=float, default=0.25)
    parser.add_argument("--owner-capture", type=float, default=0.45)
    parser.add_argument("--customer-conflict", type=float, default=0.60)
    parser.add_argument(
        "--derive-capture-shares",
        action="store_true",
        help=(
            "replace --platform-capture and --owner-capture with shares "
            "derived from pledgeability frictions"
        ),
    )
    parser.add_argument("--service-verifiable-share", type=float, default=0.15)
    parser.add_argument("--service-commitment-share", type=float, default=0.10)
    parser.add_argument("--acquisition-verifiable-share", type=float, default=0.40)
    parser.add_argument("--acquisition-commitment-share", type=float, default=0.15)
    parser.add_argument("--seller-bargaining-weight", type=float, default=1.0)
    parser.add_argument("--downstream-passthrough-share", type=float, default=0.0)
    args = parser.parse_args()
    derived_shares = None
    platform_capture = args.platform_capture
    owner_capture = args.owner_capture
    if args.derive_capture_shares:
        derived_shares = derive_capture_shares(
            CaptureShareFrictions(
                service_verifiable_share=args.service_verifiable_share,
                service_commitment_share=args.service_commitment_share,
                acquisition_verifiable_share=args.acquisition_verifiable_share,
                acquisition_commitment_share=args.acquisition_commitment_share,
                seller_bargaining_weight=args.seller_bargaining_weight,
                downstream_passthrough_share=args.downstream_passthrough_share,
            )
        )
        platform_capture = derived_shares.platform_capture_share
        owner_capture = derived_shares.owner_capture_share
    primitives = HomogeneousValueAppropriationPrimitives(
        external_learning_efficiency=args.external_learning,
        platform_capture_share=platform_capture,
        owner_capture_share=owner_capture,
        neutrality_penalty=args.customer_conflict,
    )
    outcome = solve_value_appropriation(homogeneous_value_network(primitives))
    payload = {
        "inputs": asdict(primitives),
        "derived_capture_shares": (
            asdict(derived_shares) if derived_shares is not None else None
        ),
        "pure_mode_platform_capture_threshold": (
            platform_rollup_capture_threshold(primitives)
        ),
        "solution": {
            "regime": outcome.regime.value,
            "ownership_size": outcome.ownership_size,
            "owned_names": outcome.owned_names,
            "baseline_platform_value": outcome.baseline_platform_value,
            "incremental_private_value": outcome.incremental_private_value,
            "total_private_value": outcome.total_private_value,
            "capture_upgrade": outcome.chosen.capture_upgrade,
            "productive_learning_upgrade": (outcome.chosen.productive_learning_upgrade),
            "external_access_slope": outcome.chosen.external_access_slope,
            "selection_margin": outcome.selection_margin,
            "maximum_deviation_gain": outcome.maximum_deviation_gain,
        },
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
