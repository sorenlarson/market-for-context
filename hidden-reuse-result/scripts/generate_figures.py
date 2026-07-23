#!/usr/bin/env python3
"""Generate phase maps for the two-period hidden-reuse game."""

import argparse
import csv
import json
import platform
import sys
from dataclasses import asdict, replace
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_SOURCE = REPO_ROOT / "src"
if str(MODEL_SOURCE) not in sys.path:
    sys.path.insert(0, str(MODEL_SOURCE))

from hidden_reuse import (  # noqa: E402
    HiddenReusePrimitives,
    HiddenReuseRegime,
    __version__,
    deterrence_threshold,
    provider_reuse_gain,
    solve_hidden_reuse,
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

SVG_TITLE = "Governance regimes under hidden AI context reuse"
SVG_DESCRIPTION = (
    "Three phase maps show secure modularity, priced reuse, strategic "
    "withholding, and ownership as enforcement capacity, integration cost, "
    "and the ability to pay for learning rights vary."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", type=int, default=61)
    parser.add_argument("--disclosure-grid", type=int, default=201)
    parser.add_argument(
        "--payment-caps", type=float, nargs="+", default=[0.0, 0.15, 0.50]
    )
    parser.add_argument("--enforcement-max", type=float, default=0.8)
    parser.add_argument("--integration-cost-max", type=float, default=1.1)
    parser.add_argument("--provider-outside-gain", type=float, default=0.45)
    parser.add_argument("--monitoring-cost", type=float, default=0.25)
    parser.add_argument("--owner-reuse-loss", type=float, default=0.75)
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "outputs")
    return parser.parse_args()


def add_svg_accessibility(path: Path) -> None:
    """Add an accessible title and description to Matplotlib's SVG output."""

    source = path.read_text(encoding="utf-8")
    svg_start = source.index("<svg")
    tag_end = source.index(">", svg_start)
    opening = source[svg_start:tag_end]
    opening = opening.replace(
        "<svg",
        '<svg role="img" aria-labelledby="phase-map-title phase-map-description"',
        1,
    )
    metadata = (
        f'\n <title id="phase-map-title">{SVG_TITLE}</title>'
        f'\n <desc id="phase-map-description">{SVG_DESCRIPTION}</desc>'
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
    enforcement_values: np.ndarray,
    integration_costs: np.ndarray,
    payment_cap: float,
    disclosure_grid_size: int,
    baseline: HiddenReusePrimitives,
):
    codes = {regime: index for index, regime in enumerate(REGIME_ORDER)}
    shape = (integration_costs.size, enforcement_values.size)
    regime_codes = np.empty(shape, dtype=int)
    disclosure = np.empty(shape)
    monitoring = np.empty(shape)
    reuse = np.empty(shape)
    owner_payoff = np.empty(shape)
    provider_payoff = np.empty(shape)
    transfer = np.empty(shape)
    agreement = np.empty(shape, dtype=bool)
    provider_gain = np.empty(shape)
    required_monitoring = np.empty(shape)
    payment_cap_binding = np.empty(shape, dtype=bool)
    continuation_route = np.empty(shape, dtype=object)

    baseline = replace(baseline, context_payment_cap=payment_cap)
    for row, integration_cost in enumerate(integration_costs):
        for col, enforcement in enumerate(enforcement_values):
            outcome = solve_hidden_reuse(
                replace(
                    baseline,
                    integration_cost=float(integration_cost),
                    enforcement_capacity=float(enforcement),
                ),
                disclosure_grid_size=disclosure_grid_size,
            )
            regime_codes[row, col] = codes[outcome.regime]
            disclosure[row, col] = outcome.disclosure
            monitoring[row, col] = outcome.monitoring
            reuse[row, col] = outcome.reuse
            owner_payoff[row, col] = outcome.owner_payoff
            provider_payoff[row, col] = outcome.provider_payoff
            transfer[row, col] = outcome.transfer_to_provider
            agreement[row, col] = outcome.agreement
            provider_gain[row, col] = outcome.provider_reuse_gain_before_enforcement
            required_monitoring[row, col] = outcome.required_monitoring_to_deter
            payment_cap_binding[row, col] = outcome.payment_cap_binding
            continuation_route[row, col] = (
                outcome.continuation.route.value if outcome.continuation else "none"
            )

    return {
        "regime_codes": regime_codes,
        "disclosure": disclosure,
        "monitoring": monitoring,
        "reuse": reuse,
        "owner_payoff": owner_payoff,
        "provider_payoff": provider_payoff,
        "transfer": transfer,
        "agreement": agreement,
        "provider_gain": provider_gain,
        "required_monitoring": required_monitoring,
        "payment_cap_binding": payment_cap_binding,
        "continuation_route": continuation_route,
    }


def save_phase_figure(
    output_base: Path,
    enforcement_values: np.ndarray,
    integration_costs: np.ndarray,
    payment_caps: list[float],
    results: list[dict],
    baseline: HiddenReusePrimitives,
) -> None:
    cmap = ListedColormap([REGIME_COLORS[regime] for regime in REGIME_ORDER])
    fig, axes = plt.subplots(
        1,
        len(payment_caps),
        figsize=(4.8 * len(payment_caps), 5.2),
        sharex=True,
        sharey=True,
        constrained_layout=True,
    )
    axes = np.atleast_1d(axes)
    full_disclosure_threshold = np.array(
        [
            deterrence_threshold(
                1.0, replace(baseline, integration_cost=float(integration_cost))
            )
            for integration_cost in integration_costs
        ]
    )

    for ax, payment_cap, result in zip(axes, payment_caps, results):
        ax.imshow(
            result["regime_codes"],
            origin="lower",
            aspect="auto",
            interpolation="nearest",
            extent=(
                enforcement_values.min(),
                enforcement_values.max(),
                integration_costs.min(),
                integration_costs.max(),
            ),
            cmap=cmap,
            vmin=-0.5,
            vmax=len(REGIME_ORDER) - 0.5,
        )
        ax.plot(
            full_disclosure_threshold,
            integration_costs,
            color="black",
            linestyle=":",
            linewidth=1.3,
        )
        ax.set_title(f"Context payment cap T̄ = {payment_cap:.2f}")
        ax.set_xlabel("Maximum enforceable sanction, E")
    axes[0].set_ylabel("Integration cost, F")
    fig.suptitle(
        "Hidden reuse: enforcement or pricing is required to preserve modularity"
    )
    fig.legend(
        handles=[
            Patch(color=REGIME_COLORS[regime], label=REGIME_LABELS[regime])
            for regime in REGIME_ORDER
        ]
        + [
            Line2D(
                [0],
                [0],
                color="black",
                linestyle=":",
                linewidth=1.3,
                label="Full-disclosure deterrence threshold",
            )
        ],
        loc="outside lower center",
        ncol=min(5, len(REGIME_ORDER) + 1),
        frameon=False,
    )
    png_path = output_base.with_suffix(".png")
    svg_path = output_base.with_suffix(".svg")
    fig.savefig(png_path, dpi=240)
    fig.savefig(svg_path)
    plt.close(fig)
    add_svg_accessibility(svg_path)


def write_grid(
    path: Path,
    enforcement_values: np.ndarray,
    integration_costs: np.ndarray,
    payment_caps: list[float],
    results: list[dict],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "context_payment_cap",
                "enforcement_capacity",
                "integration_cost",
                "regime",
                "agreement",
                "disclosure",
                "monitoring",
                "reuse",
                "provider_reuse_gain_before_enforcement",
                "required_monitoring_to_deter",
                "owner_payoff",
                "provider_payoff",
                "transfer_to_provider",
                "payment_cap_binding",
                "period_two_route",
            ]
        )
        for payment_cap, result in zip(payment_caps, results):
            for row, integration_cost in enumerate(integration_costs):
                for col, enforcement in enumerate(enforcement_values):
                    code = int(result["regime_codes"][row, col])
                    writer.writerow(
                        [
                            f"{payment_cap:.8f}",
                            f"{enforcement:.8f}",
                            f"{integration_cost:.8f}",
                            REGIME_ORDER[code].value,
                            str(bool(result["agreement"][row, col])).lower(),
                            f"{result['disclosure'][row, col]:.8f}",
                            f"{result['monitoring'][row, col]:.8f}",
                            f"{result['reuse'][row, col]:.8f}",
                            f"{result['provider_gain'][row, col]:.8f}",
                            f"{result['required_monitoring'][row, col]:.8f}",
                            f"{result['owner_payoff'][row, col]:.8f}",
                            f"{result['provider_payoff'][row, col]:.8f}",
                            f"{result['transfer'][row, col]:.8f}",
                            str(bool(result["payment_cap_binding"][row, col])).lower(),
                            result["continuation_route"][row, col],
                        ]
                    )


def main() -> None:
    args = parse_args()
    if args.grid < 3:
        raise SystemExit("--grid must be at least 3")
    if args.disclosure_grid < 2:
        raise SystemExit("--disclosure-grid must be at least 2")
    if args.enforcement_max <= 0 or args.integration_cost_max <= 0:
        raise SystemExit("axis maxima must be positive")
    if any(payment_cap < 0 for payment_cap in args.payment_caps):
        raise SystemExit("payment caps cannot be negative")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    enforcement_values = np.linspace(0.0, args.enforcement_max, args.grid)
    integration_costs = np.linspace(0.0, args.integration_cost_max, args.grid)
    payment_caps = list(args.payment_caps)
    baseline = HiddenReusePrimitives(
        provider_outside_gain=args.provider_outside_gain,
        monitoring_cost=args.monitoring_cost,
        owner_reuse_loss=args.owner_reuse_loss,
    )
    results = [
        solve_grid(
            enforcement_values,
            integration_costs,
            payment_cap,
            args.disclosure_grid,
            baseline,
        )
        for payment_cap in payment_caps
    ]

    save_phase_figure(
        args.output_dir / "hidden-reuse-regime-map",
        enforcement_values,
        integration_costs,
        payment_caps,
        results,
        baseline,
    )
    write_grid(
        args.output_dir / "hidden-reuse-regime-grid.csv",
        enforcement_values,
        integration_costs,
        payment_caps,
        results,
    )
    summary = {
        "model_version": __version__,
        "result_status": "calibrated theoretical computation; not empirical evidence",
        "grid_points_per_axis": args.grid,
        "disclosure_grid_size": args.disclosure_grid,
        "enforcement_range": [0.0, args.enforcement_max],
        "integration_cost_range": [0.0, args.integration_cost_max],
        "context_payment_caps": payment_caps,
        "full_disclosure_provider_reuse_gain_at_default_integration_cost": (
            provider_reuse_gain(1.0, baseline)
        ),
        "full_disclosure_deterrence_threshold_at_default_integration_cost": (
            deterrence_threshold(1.0, baseline)
        ),
        "baseline": asdict(baseline),
        "regime_cell_counts": {
            f"{payment_cap:.2f}": {
                REGIME_LABELS[regime]: int(np.sum(result["regime_codes"] == index))
                for index, regime in enumerate(REGIME_ORDER)
            }
            for payment_cap, result in zip(payment_caps, results)
        },
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
        },
    }
    (args.output_dir / "hidden-reuse-run-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
