#!/usr/bin/env python3
"""Generate deterministic and Monte Carlo maps for endogenous contracting."""

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
MODEL_SOURCE = REPO_ROOT / "src" / "endogenous_context_game"
if str(MODEL_SOURCE) not in sys.path:
    sys.path.insert(0, str(MODEL_SOURCE))

from model import ContractPrimitives, Regime, solve_contract  # noqa: E402
from simulation import (  # noqa: E402
    ContractHeterogeneity,
    simulate_contract_grid,
)


REGIME_COLORS = {
    Regime.MODULAR: "#2A9D8F",
    Regime.WITHHOLDING: "#E9C46A",
    Regime.OWNERSHIP: "#E76F51",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draws", type=int, default=5_000)
    parser.add_argument("--seed", type=int, default=19)
    parser.add_argument("--grid", type=int, default=61)
    parser.add_argument("--protectability", type=float, default=0.8)
    parser.add_argument("--protection-cost", type=float, default=1.2)
    parser.add_argument("--learning-share", type=float, default=0.25)
    parser.add_argument("--owner-bargaining-weight", type=float, default=0.5)
    parser.add_argument(
        "--output-dir", type=Path, default=REPO_ROOT / "endogenous_outputs"
    )
    return parser.parse_args()


def deterministic_map(
    leakages: np.ndarray,
    integration_costs: np.ndarray,
    *,
    protection_cost: float,
    protectability: float,
    learning_share: float,
) -> np.ndarray:
    codes = {
        Regime.MODULAR: 0,
        Regime.WITHHOLDING: 1,
        Regime.OWNERSHIP: 2,
    }
    result = np.empty((integration_costs.size, leakages.size), dtype=int)
    for row, integration_cost in enumerate(integration_costs):
        for col, leakage in enumerate(leakages):
            outcome = solve_contract(
                ContractPrimitives(
                    provider_learning_value=learning_share,
                    leakage=float(leakage),
                    protectability=protectability,
                    protection_cost=protection_cost,
                    integration_cost=float(integration_cost),
                )
            )
            result[row, col] = codes[outcome.regime]
    return result


def ownership_boundary(
    leakages: np.ndarray,
    *,
    protection_cost: float,
    protectability: float,
    learning_share: float,
) -> np.ndarray:
    return np.array(
        [
            solve_contract(
                ContractPrimitives(
                    provider_learning_value=learning_share,
                    leakage=float(leakage),
                    protectability=protectability,
                    protection_cost=protection_cost,
                    integration_cost=0.0,
                )
            ).integration_threshold
            for leakage in leakages
        ]
    )


def save_contract_cost_comparison(
    path: Path,
    leakages: np.ndarray,
    integration_costs: np.ndarray,
    *,
    protectability: float,
    learning_share: float,
) -> None:
    protection_costs = [0.10, 0.40, 1.20]
    cmap = ListedColormap(
        [
            REGIME_COLORS[Regime.MODULAR],
            REGIME_COLORS[Regime.WITHHOLDING],
            REGIME_COLORS[Regime.OWNERSHIP],
        ]
    )
    fig, axes = plt.subplots(
        1, 3, figsize=(14.4, 4.8), sharex=True, sharey=True, constrained_layout=True
    )
    for ax, cost in zip(axes, protection_costs):
        values = deterministic_map(
            leakages,
            integration_costs,
            protection_cost=cost,
            protectability=protectability,
            learning_share=learning_share,
        )
        ax.imshow(
            values,
            origin="lower",
            aspect="auto",
            interpolation="nearest",
            extent=(
                leakages.min(),
                leakages.max(),
                integration_costs.min(),
                integration_costs.max(),
            ),
            cmap=cmap,
            vmin=-0.5,
            vmax=2.5,
        )
        boundary = ownership_boundary(
            leakages,
            protection_cost=cost,
            protectability=protectability,
            learning_share=learning_share,
        )
        ax.plot(leakages, boundary, color="black", linewidth=1.6)
        saturation = cost / max(1e-12, (1.0 - learning_share) * protectability)
        if 0 < saturation < 1:
            ax.axvline(saturation, color="black", linestyle=":", linewidth=1.1)
        ax.set_title(f"Protection cost p = {cost:.2f}")
        ax.set_xlabel("Technological leakage, ω")
    axes[0].set_ylabel("Integration cost, F")
    fig.suptitle(
        "Endogenous protection shifts the sharing–withholding–ownership boundary"
    )
    fig.legend(
        handles=[
            Patch(color=REGIME_COLORS[Regime.MODULAR], label="Modular sharing"),
            Patch(
                color=REGIME_COLORS[Regime.WITHHOLDING],
                label="Strategic withholding",
            ),
            Patch(color=REGIME_COLORS[Regime.OWNERSHIP], label="Ownership"),
        ],
        loc="outside lower center",
        ncol=3,
        frameon=False,
    )
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_probability_figure(path: Path, result) -> None:
    panels = [
        ("Modular sharing", result.modular_probability, Regime.MODULAR),
        (
            "Strategic withholding",
            result.withholding_probability,
            Regime.WITHHOLDING,
        ),
        ("Ownership", result.ownership_probability, Regime.OWNERSHIP),
    ]
    fig, axes = plt.subplots(
        1, 3, figsize=(14.4, 4.8), sharex=True, sharey=True, constrained_layout=True
    )
    for ax, (title, values, regime) in zip(axes, panels):
        cmap = LinearSegmentedColormap.from_list(
            f"{regime.value}-probability", ["#F6F6F6", REGIME_COLORS[regime]]
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
        ax.set_xlabel("Technological leakage, ω")
        fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04, label="Probability")
    axes[0].set_ylabel("Integration cost, F")
    fig.suptitle("Equilibrium probabilities with endogenous protection and bargaining")
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
                "p_no_trade",
                "p_agreement",
                "mean_disclosure",
                "mean_context_use",
                "mean_protection",
                "mean_owner_payoff",
                "mean_provider_payoff",
                "mean_transfer_to_provider",
            ]
        )
        for row, integration_cost in enumerate(result.integration_costs):
            for col, leakage in enumerate(result.leakages):
                writer.writerow(
                    [
                        f"{leakage:.8f}",
                        f"{integration_cost:.8f}",
                        f"{result.modular_probability[row, col]:.8f}",
                        f"{result.withholding_probability[row, col]:.8f}",
                        f"{result.ownership_probability[row, col]:.8f}",
                        f"{result.no_trade_probability[row, col]:.8f}",
                        f"{result.agreement_probability[row, col]:.8f}",
                        f"{result.mean_disclosure[row, col]:.8f}",
                        f"{result.mean_context_use[row, col]:.8f}",
                        f"{result.mean_protection[row, col]:.8f}",
                        f"{result.mean_owner_payoff[row, col]:.8f}",
                        f"{result.mean_provider_payoff[row, col]:.8f}",
                        f"{result.mean_transfer_to_provider[row, col]:.8f}",
                    ]
                )


def main() -> None:
    args = parse_args()
    if args.grid < 3:
        raise SystemExit("--grid must be at least 3")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    leakages = np.linspace(0.0, 1.0, args.grid)
    integration_costs = np.linspace(0.0, 0.9, args.grid)
    result = simulate_contract_grid(
        leakages,
        integration_costs,
        protectability=args.protectability,
        protection_cost=args.protection_cost,
        provider_learning_share=args.learning_share,
        owner_bargaining_weight=args.owner_bargaining_weight,
        draws=args.draws,
        seed=args.seed,
        heterogeneity=ContractHeterogeneity(),
    )

    save_contract_cost_comparison(
        args.output_dir / "protection-cost-regime-comparison.png",
        leakages,
        integration_costs,
        protectability=args.protectability,
        learning_share=args.learning_share,
    )
    save_probability_figure(
        args.output_dir / "contract-regime-probabilities.png", result
    )
    write_grid(args.output_dir / "contract-regime-grid.csv", result)
    summary = {
        "draws": args.draws,
        "seed": args.seed,
        "grid_points_per_axis": args.grid,
        "protectability": args.protectability,
        "protection_cost": args.protection_cost,
        "provider_learning_share": args.learning_share,
        "owner_bargaining_weight": args.owner_bargaining_weight,
        "baseline": {
            "marginal_value_at_full": 0.55,
            "curvature": 0.45,
            "context_rent": 1.0,
        },
        "heterogeneity": {
            "value_sigma": 0.20,
            "context_sigma": 0.30,
            "integration_sigma": 0.25,
            "protection_cost_sigma": 0.20,
        },
    }
    (args.output_dir / "contract-run-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
