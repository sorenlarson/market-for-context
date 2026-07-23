#!/usr/bin/env python3
"""Generate the endogenous capability-pledgeability result and figure."""

import argparse
import csv
import json
import platform
import sys
from dataclasses import asdict
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "src"
if str(SOURCE) not in sys.path:
    sys.path.insert(0, str(SOURCE))

from hidden_reuse import (  # noqa: E402
    HiddenReusePrimitives,
    HiddenReuseRegime,
    PledgeabilityPrimitives,
    PrivateSignalPrimitives,
    __version__,
    provider_reuse_gain,
    solve_private_signal_pricing,
    solve_with_pledgeability,
)


REGIME_ORDER = [
    HiddenReuseRegime.SECURE_MODULAR,
    HiddenReuseRegime.PRICED_REUSE,
    HiddenReuseRegime.WITHHOLDING,
    HiddenReuseRegime.OWNERSHIP,
]
REGIME_COLORS = {
    HiddenReuseRegime.SECURE_MODULAR: "#2A9D8F",
    HiddenReuseRegime.PRICED_REUSE: "#457B9D",
    HiddenReuseRegime.WITHHOLDING: "#E9C46A",
    HiddenReuseRegime.OWNERSHIP: "#E76F51",
}
REGIME_LABELS = {
    HiddenReuseRegime.SECURE_MODULAR: "Secure modularity",
    HiddenReuseRegime.PRICED_REUSE: "Priced reuse",
    HiddenReuseRegime.WITHHOLDING: "Strategic withholding",
    HiddenReuseRegime.OWNERSHIP: "Ownership",
}

SVG_TITLE = "Pledgeable future AI capability and context governance"
SVG_DESCRIPTION = (
    "The left panel shows the share of uncertain future capability value that "
    "can be credibly promised using verifiable royalties and collateral. The "
    "right panel shows the resulting hidden-reuse governance regime under weak "
    "enforcement and costly integration."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", type=int, default=61)
    parser.add_argument("--disclosure-grid", type=int, default=201)
    parser.add_argument("--enforcement", type=float, default=0.20)
    parser.add_argument("--integration-cost", type=float, default=0.80)
    parser.add_argument("--expected-value", type=float)
    parser.add_argument("--value-log-sigma", type=float, default=0.80)
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "outputs")
    return parser.parse_args()


def add_svg_accessibility(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    svg_start = source.index("<svg")
    tag_end = source.index(">", svg_start)
    opening = source[svg_start:tag_end].replace(
        "<svg",
        '<svg role="img" aria-labelledby="pledge-map-title pledge-map-description"',
        1,
    )
    metadata = (
        f'\n <title id="pledge-map-title">{SVG_TITLE}</title>'
        f'\n <desc id="pledge-map-description">{SVG_DESCRIPTION}</desc>'
    )
    source = (
        source[:svg_start]
        + opening
        + source[tag_end : tag_end + 1]
        + metadata
        + source[tag_end + 1 :]
    )
    path.write_text(source, encoding="utf-8")


def solve_grid(
    verifiable_shares: np.ndarray,
    collateral_shares: np.ndarray,
    hidden: HiddenReusePrimitives,
    expected_value: float,
    value_log_sigma: float,
    disclosure_grid_size: int,
) -> dict:
    codes = {regime: index for index, regime in enumerate(REGIME_ORDER)}
    shape = (collateral_shares.size, verifiable_shares.size)
    pledgeable_share = np.empty(shape)
    maximum_payment = np.empty(shape)
    regime_codes = np.empty(shape, dtype=int)
    disclosure = np.empty(shape)
    reuse = np.empty(shape)
    transfer = np.empty(shape)

    for row, collateral_share in enumerate(collateral_shares):
        collateral = float(collateral_share * expected_value)
        for col, verifiable_share in enumerate(verifiable_shares):
            result = solve_with_pledgeability(
                hidden,
                PledgeabilityPrimitives(
                    expected_net_capability_value=expected_value,
                    verifiable_share=float(verifiable_share),
                    collateral=collateral,
                    value_log_sigma=value_log_sigma,
                ),
                disclosure_grid_size=disclosure_grid_size,
            )
            pledgeable_share[row, col] = result.pricing.pledgeable_share
            maximum_payment[row, col] = result.pricing.maximum_pledgeable_payment
            regime_codes[row, col] = codes[result.governance.regime]
            disclosure[row, col] = result.governance.disclosure
            reuse[row, col] = result.governance.reuse
            transfer[row, col] = result.governance.transfer_to_provider

    return {
        "pledgeable_share": pledgeable_share,
        "maximum_payment": maximum_payment,
        "regime_codes": regime_codes,
        "disclosure": disclosure,
        "reuse": reuse,
        "transfer": transfer,
    }


def save_figure(
    output_base: Path,
    verifiable_shares: np.ndarray,
    collateral_shares: np.ndarray,
    result: dict,
    hidden: HiddenReusePrimitives,
    expected_value: float,
) -> None:
    regime_cmap = ListedColormap([REGIME_COLORS[regime] for regime in REGIME_ORDER])
    fig, axes = plt.subplots(
        1, 2, figsize=(11.2, 5.2), sharex=True, sharey=True, constrained_layout=True
    )
    extent = (
        verifiable_shares.min(),
        verifiable_shares.max(),
        collateral_shares.min(),
        collateral_shares.max(),
    )

    pledge_image = axes[0].imshow(
        result["pledgeable_share"],
        origin="lower",
        aspect="auto",
        interpolation="nearest",
        extent=extent,
        cmap="cividis",
        vmin=0,
        vmax=1,
    )
    axes[0].plot(
        verifiable_shares,
        1.0 - verifiable_shares,
        color="white",
        linewidth=1.7,
        linestyle="--",
        label="Entire expected value is pledgeable",
    )
    axes[0].set_title("Maximum enforceable claim")
    axes[0].legend(loc="upper right", frameon=True)
    fig.colorbar(
        pledge_image,
        ax=axes[0],
        fraction=0.046,
        pad=0.04,
        label="Share of expected capability value",
    )

    axes[1].imshow(
        result["regime_codes"],
        origin="lower",
        aspect="auto",
        interpolation="nearest",
        extent=extent,
        cmap=regime_cmap,
        vmin=-0.5,
        vmax=len(REGIME_ORDER) - 0.5,
    )
    axes[1].set_title("Governance after pricing constraint")
    axes[1].legend(
        handles=[
            Patch(color=REGIME_COLORS[regime], label=REGIME_LABELS[regime])
            for regime in REGIME_ORDER
            if np.any(result["regime_codes"] == REGIME_ORDER.index(regime))
        ],
        loc="upper right",
        frameon=True,
    )

    for ax in axes:
        ax.set_xlabel("Verifiable share of future value, φ")
    axes[0].set_ylabel("Collateral as a share of expected value, W / E[V]")
    fig.suptitle(
        "Future capability can be priced only to the extent it is pledgeable\n"
        f"E[V]={expected_value:.3f}, enforcement={hidden.enforcement_capacity:.2f}, "
        f"integration cost={hidden.integration_cost:.2f}"
    )

    png_path = output_base.with_suffix(".png")
    svg_path = output_base.with_suffix(".svg")
    fig.savefig(png_path, dpi=240)
    fig.savefig(svg_path)
    plt.close(fig)
    add_svg_accessibility(svg_path)


def write_grid(
    path: Path,
    verifiable_shares: np.ndarray,
    collateral_shares: np.ndarray,
    expected_value: float,
    result: dict,
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "verifiable_share",
                "collateral_share_of_expected_value",
                "collateral",
                "expected_net_capability_value",
                "maximum_pledgeable_payment",
                "pledgeable_share",
                "unpledgeable_expected_value",
                "regime",
                "disclosure",
                "reuse",
                "transfer_to_provider",
            ]
        )
        for row, collateral_share in enumerate(collateral_shares):
            for col, verifiable_share in enumerate(verifiable_shares):
                payment = result["maximum_payment"][row, col]
                regime = REGIME_ORDER[int(result["regime_codes"][row, col])]
                writer.writerow(
                    [
                        f"{verifiable_share:.8f}",
                        f"{collateral_share:.8f}",
                        f"{collateral_share * expected_value:.8f}",
                        f"{expected_value:.8f}",
                        f"{payment:.8f}",
                        f"{result['pledgeable_share'][row, col]:.8f}",
                        f"{expected_value - payment:.8f}",
                        regime.value,
                        f"{result['disclosure'][row, col]:.8f}",
                        f"{result['reuse'][row, col]:.8f}",
                        f"{result['transfer'][row, col]:.8f}",
                    ]
                )


def write_examples(
    output_dir: Path,
    hidden: HiddenReusePrimitives,
    expected_value: float,
    value_log_sigma: float,
) -> None:
    scenarios = [
        ("unpledgeable", 0.00, 0.00),
        ("partly_pledgeable", 0.10, 0.02),
        ("priced_reuse_boundary", 0.50, 0.00),
        ("fully_pledgeable", 0.80, 0.20),
    ]
    examples = []
    for name, verifiable_share, collateral in scenarios:
        result = solve_with_pledgeability(
            hidden,
            PledgeabilityPrimitives(
                expected_net_capability_value=expected_value,
                verifiable_share=verifiable_share,
                collateral=collateral,
                value_log_sigma=value_log_sigma,
            ),
            disclosure_grid_size=401,
        )
        examples.append(
            {
                "name": name,
                "verifiable_share": verifiable_share,
                "collateral": collateral,
                "pricing": asdict(result.pricing),
                "governance": {
                    "regime": result.governance.regime.value,
                    "disclosure": result.governance.disclosure,
                    "reuse": result.governance.reuse,
                    "transfer_to_provider": (result.governance.transfer_to_provider),
                },
            }
        )

    private_signal_scenarios = [
        (
            "pool_private_signals",
            PrivateSignalPrimitives(
                low_expected_value=0.15,
                high_expected_value=0.45,
                high_type_probability=0.30,
                verifiable_share=0.10,
                collateral=0.02,
            ),
        ),
        (
            "screen_high_private_signal",
            PrivateSignalPrimitives(
                low_expected_value=0.15,
                high_expected_value=0.45,
                high_type_probability=0.90,
                verifiable_share=0.10,
                collateral=0.02,
            ),
        ),
    ]
    private_signal_examples = []
    for name, primitives in private_signal_scenarios:
        result = solve_private_signal_pricing(primitives)
        private_signal_examples.append(
            {
                "name": name,
                "inputs": asdict(primitives),
                "outcome": {
                    **asdict(result),
                    "policy": result.policy.value,
                },
            }
        )

    payload = {
        "model_version": __version__,
        "result_status": "calibrated theoretical computation; not empirical evidence",
        "formula": "P* = min(E[V], W + phi * E[V])",
        "examples": examples,
        "private_signal_examples": private_signal_examples,
    }
    (output_dir / "pledgeability-examples.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    args = parse_args()
    if args.grid < 3:
        raise SystemExit("--grid must be at least 3")
    if args.disclosure_grid < 2:
        raise SystemExit("--disclosure-grid must be at least 2")
    if args.expected_value is not None and args.expected_value < 0:
        raise SystemExit("--expected-value cannot be negative")
    if args.value_log_sigma < 0:
        raise SystemExit("--value-log-sigma cannot be negative")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    hidden = HiddenReusePrimitives(
        enforcement_capacity=args.enforcement,
        integration_cost=args.integration_cost,
    )
    expected_value = (
        args.expected_value
        if args.expected_value is not None
        else max(0.0, provider_reuse_gain(1.0, hidden))
    )
    if expected_value <= 0:
        raise SystemExit("the expected capability value must be positive")

    verifiable_shares = np.linspace(0.0, 1.0, args.grid)
    collateral_shares = np.linspace(0.0, 1.0, args.grid)
    result = solve_grid(
        verifiable_shares,
        collateral_shares,
        hidden,
        expected_value,
        args.value_log_sigma,
        args.disclosure_grid,
    )

    save_figure(
        args.output_dir / "capability-pledgeability-map",
        verifiable_shares,
        collateral_shares,
        result,
        hidden,
        expected_value,
    )
    write_grid(
        args.output_dir / "capability-pledgeability-grid.csv",
        verifiable_shares,
        collateral_shares,
        expected_value,
        result,
    )
    write_examples(
        args.output_dir,
        hidden,
        expected_value,
        args.value_log_sigma,
    )

    summary = {
        "model_version": __version__,
        "result_status": "calibrated theoretical computation; not empirical evidence",
        "grid_points_per_axis": args.grid,
        "disclosure_grid_size": args.disclosure_grid,
        "formula": "P* = min(E[V], W + phi * E[V])",
        "expected_net_capability_value": expected_value,
        "value_log_sigma": args.value_log_sigma,
        "hidden_reuse_baseline": asdict(hidden),
        "regime_cell_counts": {
            REGIME_LABELS[regime]: int(np.sum(result["regime_codes"] == index))
            for index, regime in enumerate(REGIME_ORDER)
        },
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
        },
    }
    (args.output_dir / "pledgeability-run-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
