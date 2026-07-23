#!/usr/bin/env python3
"""Generate deterministic and Monte Carlo phase diagrams for the first result."""

import argparse
import csv
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib.patches import Patch

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from context_game.model import Primitives, Regime, solve  # noqa: E402
from context_game.simulation import Heterogeneity, simulate_grid  # noqa: E402


REGIME_COLORS = {
    Regime.MODULAR.value: "#2A9D8F",
    Regime.WITHHOLDING.value: "#E9C46A",
    Regime.OWNERSHIP.value: "#E76F51",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draws", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--grid", type=int, default=61)
    parser.add_argument("--protection", type=float, default=0.2)
    parser.add_argument("--marginal-value", type=float, default=0.55)
    parser.add_argument("--curvature", type=float, default=0.45)
    parser.add_argument("--context-rent", type=float, default=1.0)
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "outputs")
    return parser.parse_args()


def deterministic_map(
    leakages: np.ndarray,
    integration_costs: np.ndarray,
    protection: float,
    marginal_value_at_full: float,
    curvature: float,
    context_rent: float,
) -> np.ndarray:
    codes = {
        Regime.MODULAR: 0,
        Regime.WITHHOLDING: 1,
        Regime.OWNERSHIP: 2,
    }
    result = np.empty((integration_costs.size, leakages.size), dtype=int)
    for row, integration_cost in enumerate(integration_costs):
        for col, leakage in enumerate(leakages):
            outcome = solve(
                Primitives(
                    marginal_value_at_full=marginal_value_at_full,
                    curvature=curvature,
                    context_rent=context_rent,
                    leakage=float(leakage),
                    protection=protection,
                    integration_cost=float(integration_cost),
                )
            )
            result[row, col] = codes[outcome.regime]
    return result


def save_deterministic_figure(
    path: Path,
    leakages: np.ndarray,
    costs: np.ndarray,
    protection: float,
    marginal_value_at_full: float,
    curvature: float,
    context_rent: float,
) -> None:
    regime_map = deterministic_map(
        leakages,
        costs,
        protection,
        marginal_value_at_full,
        curvature,
        context_rent,
    )
    cmap = ListedColormap(
        [
            REGIME_COLORS[Regime.MODULAR.value],
            REGIME_COLORS[Regime.WITHHOLDING.value],
            REGIME_COLORS[Regime.OWNERSHIP.value],
        ]
    )
    fig, ax = plt.subplots(figsize=(8.4, 5.6), constrained_layout=True)
    ax.imshow(
        regime_map,
        origin="lower",
        aspect="auto",
        interpolation="nearest",
        extent=(leakages.min(), leakages.max(), costs.min(), costs.max()),
        cmap=cmap,
        vmin=-0.5,
        vmax=2.5,
    )

    thresholds = np.array(
        [
            solve(
                Primitives(
                    marginal_value_at_full=marginal_value_at_full,
                    curvature=curvature,
                    context_rent=context_rent,
                    leakage=float(leakage),
                    protection=protection,
                    integration_cost=0.0,
                )
            ).integration_threshold
            for leakage in leakages
        ]
    )
    ax.plot(leakages, thresholds, color="black", linewidth=1.8, label="ownership boundary")
    disclosure_cutoff = marginal_value_at_full / max(
        1e-12, context_rent * (1.0 - protection)
    )
    if 0 <= disclosure_cutoff <= 1:
        ax.axvline(
            disclosure_cutoff,
            color="black",
            linewidth=1.2,
            linestyle="--",
            label="full-sharing boundary",
        )
    ax.set(
        xlabel="Information leakage, ω",
        ylabel="Integration cost, F",
        title=f"Analytical regimes at contractual protection κ={protection:.2f}",
    )
    ax.legend(
        handles=[
            Patch(color=REGIME_COLORS[Regime.MODULAR.value], label="Modular sharing"),
            Patch(
                color=REGIME_COLORS[Regime.WITHHOLDING.value],
                label="Strategic withholding",
            ),
            Patch(color=REGIME_COLORS[Regime.OWNERSHIP.value], label="Ownership"),
        ],
        loc="upper right",
        frameon=True,
    )
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_probability_figure(path: Path, result) -> None:
    panels = [
        ("Modular sharing", result.modular_probability, Regime.MODULAR.value),
        (
            "Strategic withholding",
            result.withholding_probability,
            Regime.WITHHOLDING.value,
        ),
        ("Ownership", result.ownership_probability, Regime.OWNERSHIP.value),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(14.4, 4.8), sharex=True, sharey=True)
    for ax, (title, values, regime) in zip(axes, panels):
        color = REGIME_COLORS[regime]
        cmap = LinearSegmentedColormap.from_list(
            f"{regime}-probability", ["#F6F6F6", color]
        )
        image = ax.imshow(
            values,
            origin="lower",
            aspect="auto",
            interpolation="nearest",
            extent=(
                result.leakages.min(),
                result.leakages.max(),
                result.integration_costs.min(),
                result.integration_costs.max(),
            ),
            cmap=cmap,
            vmin=0,
            vmax=1,
        )
        ax.set_title(title)
        ax.set_xlabel("Information leakage, ω")
        fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04, label="Probability")
    axes[0].set_ylabel("Integration cost, F")
    fig.suptitle("Regime probabilities across heterogeneous initial conditions")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_grid(path: Path, result) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "leakage",
                "integration_cost",
                "p_modular",
                "p_withholding",
                "p_ownership",
                "mean_context_use",
            ]
        )
        for row, cost in enumerate(result.integration_costs):
            for col, leakage in enumerate(result.leakages):
                writer.writerow(
                    [
                        f"{leakage:.8f}",
                        f"{cost:.8f}",
                        f"{result.modular_probability[row, col]:.8f}",
                        f"{result.withholding_probability[row, col]:.8f}",
                        f"{result.ownership_probability[row, col]:.8f}",
                        f"{result.mean_disclosure[row, col]:.8f}",
                    ]
                )


def main() -> None:
    args = parse_args()
    if args.grid < 3:
        raise SystemExit("--grid must be at least 3")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    leakages = np.linspace(0.0, 1.0, args.grid)
    costs = np.linspace(0.0, 0.9, args.grid)
    result = simulate_grid(
        leakages,
        costs,
        protection=args.protection,
        marginal_value_at_full=args.marginal_value,
        curvature=args.curvature,
        context_rent=args.context_rent,
        draws=args.draws,
        seed=args.seed,
        heterogeneity=Heterogeneity(),
    )

    save_deterministic_figure(
        args.output_dir / "deterministic-regime-map.png",
        leakages,
        costs,
        args.protection,
        args.marginal_value,
        args.curvature,
        args.context_rent,
    )
    save_probability_figure(
        args.output_dir / "monte-carlo-regime-probabilities.png", result
    )
    write_grid(args.output_dir / "regime-grid.csv", result)
    summary = {
        "draws": args.draws,
        "seed": args.seed,
        "grid_points_per_axis": args.grid,
        "protection": args.protection,
        "baseline": {
            "marginal_value_at_full": args.marginal_value,
            "curvature": args.curvature,
            "context_rent": args.context_rent,
        },
        "heterogeneity": {
            "value_sigma": 0.20,
            "context_sigma": 0.30,
            "integration_sigma": 0.25,
        },
    }
    (args.output_dir / "run-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
