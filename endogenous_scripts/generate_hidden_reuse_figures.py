#!/usr/bin/env python3
"""Generate phase maps for the two-period hidden-reuse game."""

import argparse
import csv
import json
import sys
from dataclasses import replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_SOURCE = REPO_ROOT / "src" / "endogenous_context_game"
if str(MODEL_SOURCE) not in sys.path:
    sys.path.insert(0, str(MODEL_SOURCE))

from hidden_reuse import (  # noqa: E402
    HiddenReusePrimitives,
    HiddenReuseRegime,
    provider_reuse_gain,
    solve_hidden_reuse,
)


REGIME_ORDER = [
    HiddenReuseRegime.SECURE_MODULAR,
    HiddenReuseRegime.LEAKY_MODULAR,
    HiddenReuseRegime.WITHHOLDING,
    HiddenReuseRegime.OWNERSHIP,
]
REGIME_COLORS = {
    HiddenReuseRegime.SECURE_MODULAR: "#2A9D8F",
    HiddenReuseRegime.LEAKY_MODULAR: "#457B9D",
    HiddenReuseRegime.WITHHOLDING: "#E9C46A",
    HiddenReuseRegime.OWNERSHIP: "#E76F51",
}
REGIME_LABELS = {
    HiddenReuseRegime.SECURE_MODULAR: "Secure modularity",
    HiddenReuseRegime.LEAKY_MODULAR: "Priced reuse",
    HiddenReuseRegime.WITHHOLDING: "Strategic withholding",
    HiddenReuseRegime.OWNERSHIP: "Ownership",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", type=int, default=61)
    parser.add_argument("--disclosure-grid", type=int, default=101)
    parser.add_argument(
        "--output-dir", type=Path, default=REPO_ROOT / "hidden_reuse_outputs"
    )
    return parser.parse_args()


def solve_grid(
    enforcement_values: np.ndarray,
    integration_costs: np.ndarray,
    payment_cap: float,
    disclosure_grid_size: int,
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
    continuation_route = np.empty(shape, dtype=object)

    baseline = HiddenReusePrimitives(context_payment_cap=payment_cap)
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
        "continuation_route": continuation_route,
    }


def save_phase_figure(
    path: Path,
    enforcement_values: np.ndarray,
    integration_costs: np.ndarray,
    payment_caps: list[float],
    results: list[dict],
) -> None:
    cmap = ListedColormap([REGIME_COLORS[regime] for regime in REGIME_ORDER])
    fig, axes = plt.subplots(
        1,
        len(payment_caps),
        figsize=(14.4, 5.0),
        sharex=True,
        sharey=True,
        constrained_layout=True,
    )
    full_disclosure_gain = provider_reuse_gain(1.0, HiddenReusePrimitives())

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
        ax.axvline(
            full_disclosure_gain,
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
        ],
        loc="outside lower center",
        ncol=4,
        frameon=False,
    )
    fig.savefig(path, dpi=180)
    plt.close(fig)


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
                "disclosure",
                "monitoring",
                "reuse",
                "owner_payoff",
                "provider_payoff",
                "transfer_to_provider",
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
                            f"{result['disclosure'][row, col]:.8f}",
                            f"{result['monitoring'][row, col]:.8f}",
                            f"{result['reuse'][row, col]:.8f}",
                            f"{result['owner_payoff'][row, col]:.8f}",
                            f"{result['provider_payoff'][row, col]:.8f}",
                            f"{result['transfer'][row, col]:.8f}",
                            result["continuation_route"][row, col],
                        ]
                    )


def main() -> None:
    args = parse_args()
    if args.grid < 3:
        raise SystemExit("--grid must be at least 3")
    if args.disclosure_grid < 2:
        raise SystemExit("--disclosure-grid must be at least 2")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    enforcement_values = np.linspace(0.0, 0.8, args.grid)
    integration_costs = np.linspace(0.0, 1.1, args.grid)
    payment_caps = [0.0, 0.15, 0.50]
    results = [
        solve_grid(
            enforcement_values,
            integration_costs,
            payment_cap,
            args.disclosure_grid,
        )
        for payment_cap in payment_caps
    ]

    save_phase_figure(
        args.output_dir / "hidden-reuse-regime-map.png",
        enforcement_values,
        integration_costs,
        payment_caps,
        results,
    )
    write_grid(
        args.output_dir / "hidden-reuse-regime-grid.csv",
        enforcement_values,
        integration_costs,
        payment_caps,
        results,
    )
    summary = {
        "grid_points_per_axis": args.grid,
        "disclosure_grid_size": args.disclosure_grid,
        "enforcement_range": [0.0, 0.8],
        "integration_cost_range": [0.0, 1.1],
        "context_payment_caps": payment_caps,
        "full_disclosure_provider_reuse_gain": provider_reuse_gain(
            1.0, HiddenReusePrimitives()
        ),
        "baseline": {
            "discount_factor": 0.90,
            "owner_reuse_loss": 0.75,
            "incumbent_capability_gain": 0.25,
            "provider_outside_gain": 0.45,
            "monitoring_cost": 0.25,
        },
    }
    (args.output_dir / "hidden-reuse-run-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
