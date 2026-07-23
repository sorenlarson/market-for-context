#!/usr/bin/env python3
"""Generate the firm-size separation result, data, and figures."""

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
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "src"
if str(SOURCE) not in sys.path:
    sys.path.insert(0, str(SOURCE))

from hidden_reuse import (  # noqa: E402
    FirmSizePrimitives,
    HiddenReusePrimitives,
    PledgeabilityPrimitives,
    __version__,
    derive_owner_internalization_advantage,
    solve_firm_size,
)


SVG_TITLE = "The integration decision and equilibrium firm size separate"
SVG_DESCRIPTION = (
    "The left panel shows whether homogeneous context-generating assets remain "
    "modular or form integrated firms as the per-asset ownership advantage and "
    "cross-asset learning vary. The right panel shows the target number of "
    "assets per integrated firm as learning and ongoing coordination cost vary, "
    "holding a declining-marginal-cost integration learning curve fixed."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", type=int, default=81)
    parser.add_argument("--max-firm-size", type=int, default=60)
    parser.add_argument("--advantage-min", type=float, default=0.30)
    parser.add_argument("--advantage-max", type=float, default=0.90)
    parser.add_argument("--learning-max", type=float, default=1.00)
    parser.add_argument("--organization-cost-min", type=float, default=0.003)
    parser.add_argument("--organization-cost-max", type=float, default=0.040)
    parser.add_argument("--shared-fixed-cost", type=float, default=1.50)
    parser.add_argument("--learning-saturation", type=float, default=4.00)
    parser.add_argument("--integration-cost", type=float, default=0.50)
    parser.add_argument("--integration-elasticity", type=float, default=0.65)
    parser.add_argument("--organization-elasticity", type=float, default=1.40)
    parser.add_argument("--baseline-learning", type=float, default=0.35)
    parser.add_argument("--baseline-organization-cost", type=float, default=0.015)
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "outputs")
    return parser.parse_args()


def add_svg_accessibility(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    svg_start = source.index("<svg")
    tag_end = source.index(">", svg_start)
    opening = source[svg_start:tag_end].replace(
        "<svg",
        '<svg role="img" aria-labelledby="firm-size-title firm-size-description"',
        1,
    )
    metadata = (
        f'\n <title id="firm-size-title">{SVG_TITLE}</title>'
        f'\n <desc id="firm-size-description">{SVG_DESCRIPTION}</desc>'
    )
    source = (
        source[:svg_start]
        + opening
        + source[tag_end : tag_end + 1]
        + metadata
        + source[tag_end + 1 :]
    )
    path.write_text(source, encoding="utf-8")


def _baseline(args: argparse.Namespace) -> FirmSizePrimitives:
    return FirmSizePrimitives(
        internalization_advantage=0.65,
        shared_fixed_cost=args.shared_fixed_cost,
        cross_node_learning=args.baseline_learning,
        learning_saturation=args.learning_saturation,
        integration_cost_scale=args.integration_cost,
        integration_cost_elasticity=args.integration_elasticity,
        organization_cost_scale=args.baseline_organization_cost,
        organization_cost_elasticity=args.organization_elasticity,
        max_firm_size=args.max_firm_size,
    )


def solve_maps(
    advantages: np.ndarray,
    learning_values: np.ndarray,
    organization_costs: np.ndarray,
    baseline: FirmSizePrimitives,
) -> dict:
    entry_size = np.empty((learning_values.size, advantages.size), dtype=int)
    entry_target = np.empty_like(entry_size)
    entry_threshold = np.empty_like(entry_size, dtype=float)
    entry_per_node = np.empty_like(entry_size, dtype=float)
    entry_regime = np.empty(entry_size.shape, dtype=object)

    threshold_by_learning = np.empty(learning_values.size)
    target_by_learning = np.empty(learning_values.size, dtype=int)
    for row, learning in enumerate(learning_values):
        conditional = solve_firm_size(
            replace(
                baseline,
                internalization_advantage=0.0,
                cross_node_learning=float(learning),
            )
        )
        threshold_by_learning[row] = conditional.integration_threshold
        target_by_learning[row] = conditional.conditional_target_size
        for col, advantage in enumerate(advantages):
            outcome = solve_firm_size(
                replace(
                    baseline,
                    internalization_advantage=float(advantage),
                    cross_node_learning=float(learning),
                )
            )
            entry_size[row, col] = outcome.equilibrium_firm_size
            entry_target[row, col] = outcome.conditional_target_size
            entry_threshold[row, col] = outcome.integration_threshold
            entry_per_node[row, col] = outcome.per_node_surplus_at_target
            entry_regime[row, col] = outcome.regime.value

    scale_size = np.empty((learning_values.size, organization_costs.size), dtype=int)
    scale_continuous = np.empty_like(scale_size, dtype=float)
    scale_threshold = np.empty_like(scale_size, dtype=float)
    for row, learning in enumerate(learning_values):
        for col, organization_cost in enumerate(organization_costs):
            outcome = solve_firm_size(
                replace(
                    baseline,
                    internalization_advantage=0.0,
                    cross_node_learning=float(learning),
                    organization_cost_scale=float(organization_cost),
                )
            )
            scale_size[row, col] = outcome.conditional_target_size
            scale_continuous[row, col] = outcome.continuous_target_size
            scale_threshold[row, col] = outcome.integration_threshold

    return {
        "entry_size": entry_size,
        "entry_target": entry_target,
        "entry_threshold": entry_threshold,
        "entry_per_node": entry_per_node,
        "entry_regime": entry_regime,
        "threshold_by_learning": threshold_by_learning,
        "target_by_learning": target_by_learning,
        "scale_size": scale_size,
        "scale_continuous": scale_continuous,
        "scale_threshold": scale_threshold,
    }


def bridge_examples() -> dict:
    weak_hidden = HiddenReusePrimitives(enforcement_capacity=0.20)
    strong_hidden = HiddenReusePrimitives(enforcement_capacity=0.80)
    weak_unpriced = derive_owner_internalization_advantage(weak_hidden)
    weak_priced = derive_owner_internalization_advantage(
        weak_hidden,
        PledgeabilityPrimitives(verifiable_share=0.60, collateral=0.00),
    )
    strong = derive_owner_internalization_advantage(strong_hidden)
    return {
        "weak_enforcement_unpriced": weak_unpriced,
        "weak_enforcement_priced": weak_priced,
        "strong_enforcement": strong,
    }


def save_figure(
    output_base: Path,
    advantages: np.ndarray,
    learning_values: np.ndarray,
    organization_costs: np.ndarray,
    result: dict,
    baseline: FirmSizePrimitives,
    bridges: dict,
) -> None:
    cmap = plt.get_cmap("viridis").copy()
    cmap.set_bad("#F0F0F0")
    observed_max = max(
        int(np.max(result["entry_size"])), int(np.max(result["scale_size"]))
    )
    color_max = max(2, observed_max)
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.5), constrained_layout=True)

    entry_masked = np.ma.masked_where(result["entry_size"] == 0, result["entry_size"])
    axes[0].imshow(
        entry_masked,
        origin="lower",
        aspect="auto",
        interpolation="nearest",
        extent=(
            advantages.min(),
            advantages.max(),
            learning_values.min(),
            learning_values.max(),
        ),
        cmap=cmap,
        vmin=1,
        vmax=color_max,
    )
    axes[0].plot(
        result["threshold_by_learning"],
        learning_values,
        color="black",
        linewidth=1.8,
        label="Integration threshold",
    )
    weak = bridges["weak_enforcement_unpriced"].internalization_advantage
    strong = bridges["strong_enforcement"].internalization_advantage
    axes[0].scatter(
        [strong, weak],
        [baseline.cross_node_learning, baseline.cross_node_learning],
        marker="o",
        s=45,
        facecolors=["white", "black"],
        edgecolors="black",
        linewidths=1.2,
        zorder=5,
    )
    axes[0].annotate(
        "strong enforcement",
        (strong, baseline.cross_node_learning),
        xytext=(-4, -18),
        textcoords="offset points",
        ha="center",
        fontsize=8,
    )
    axes[0].annotate(
        "weak enforcement",
        (weak, baseline.cross_node_learning),
        xytext=(-4, 11),
        textcoords="offset points",
        ha="center",
        fontsize=8,
    )
    axes[0].set(
        title="1. Hidden reuse decides whether firms form",
        xlabel="Per-asset internalization advantage, A",
        ylabel="Transferable cross-asset learning, L",
    )
    axes[0].legend(
        handles=[
            Patch(facecolor="#F0F0F0", edgecolor="#C0C0C0", label="Modular"),
            Line2D([0], [0], color="black", linewidth=1.8, label="Entry boundary"),
        ],
        loc="upper right",
        frameon=True,
    )

    right = axes[1].imshow(
        result["scale_size"],
        origin="lower",
        aspect="auto",
        interpolation="nearest",
        extent=(
            organization_costs.min(),
            organization_costs.max(),
            learning_values.min(),
            learning_values.max(),
        ),
        cmap=cmap,
        vmin=1,
        vmax=color_max,
    )
    baseline_outcome = solve_firm_size(baseline)
    axes[1].scatter(
        [baseline.organization_cost_scale],
        [baseline.cross_node_learning],
        color="black",
        s=45,
        zorder=5,
    )
    axes[1].annotate(
        f"baseline: {baseline_outcome.conditional_target_size} assets",
        (baseline.organization_cost_scale, baseline.cross_node_learning),
        xytext=(8, 8),
        textcoords="offset points",
        fontsize=8,
    )
    axes[1].set(
        title="2. Integration economies and coordination set size",
        xlabel="Ongoing coordination-cost scale, c",
        ylabel="Transferable cross-asset learning, L",
    )
    colorbar = fig.colorbar(
        right,
        ax=axes,
        fraction=0.035,
        pad=0.025,
        label="Assets per integrated firm",
    )
    ticks = sorted(
        set(
            np.linspace(1, color_max, min(7, color_max), dtype=int).tolist()
            + [baseline_outcome.conditional_target_size]
        )
    )
    colorbar.set_ticks(ticks)
    fig.suptitle(
        "Firm boundaries and firm size are different margins\n"
        f"K={baseline.shared_fixed_cost:.2f}, κ={baseline.learning_saturation:.1f}, "
        f"d={baseline.integration_cost_scale:.2f}, "
        f"ρ={baseline.integration_cost_elasticity:.2f}, "
        f"η={baseline.organization_cost_elasticity:.1f}"
    )

    png_path = output_base.with_suffix(".png")
    svg_path = output_base.with_suffix(".svg")
    fig.savefig(png_path, dpi=240)
    fig.savefig(svg_path)
    plt.close(fig)
    add_svg_accessibility(svg_path)


def write_entry_grid(
    path: Path,
    advantages: np.ndarray,
    learning_values: np.ndarray,
    result: dict,
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "internalization_advantage",
                "cross_node_learning",
                "integration_threshold",
                "conditional_target_size",
                "equilibrium_firm_size",
                "per_node_surplus_at_target",
                "regime",
            ]
        )
        for row, learning in enumerate(learning_values):
            for col, advantage in enumerate(advantages):
                writer.writerow(
                    [
                        f"{advantage:.8f}",
                        f"{learning:.8f}",
                        f"{result['entry_threshold'][row, col]:.8f}",
                        int(result["entry_target"][row, col]),
                        int(result["entry_size"][row, col]),
                        f"{result['entry_per_node'][row, col]:.8f}",
                        result["entry_regime"][row, col],
                    ]
                )


def write_scale_grid(
    path: Path,
    organization_costs: np.ndarray,
    learning_values: np.ndarray,
    result: dict,
    baseline: FirmSizePrimitives,
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "integration_cost_scale",
                "integration_cost_elasticity",
                "organization_cost_scale",
                "cross_node_learning",
                "integration_threshold",
                "conditional_target_size",
                "continuous_target_size",
            ]
        )
        for row, learning in enumerate(learning_values):
            for col, organization_cost in enumerate(organization_costs):
                writer.writerow(
                    [
                        f"{baseline.integration_cost_scale:.8f}",
                        f"{baseline.integration_cost_elasticity:.8f}",
                        f"{organization_cost:.8f}",
                        f"{learning:.8f}",
                        f"{result['scale_threshold'][row, col]:.8f}",
                        int(result["scale_size"][row, col]),
                        f"{result['scale_continuous'][row, col]:.8f}",
                    ]
                )


def write_examples(
    output_dir: Path,
    baseline: FirmSizePrimitives,
    bridges: dict,
) -> None:
    examples = []
    for name, bridge in bridges.items():
        primitives = replace(
            baseline,
            internalization_advantage=bridge.internalization_advantage,
        )
        outcome = solve_firm_size(primitives)
        examples.append(
            {
                "name": name,
                "bilateral_bridge": {
                    **asdict(bridge),
                    "modular_regime": bridge.modular_regime.value,
                },
                "firm_size_inputs": asdict(primitives),
                "firm_size_outcome": {
                    "regime": outcome.regime.value,
                    "integrates": outcome.integrates,
                    "equilibrium_firm_size": outcome.equilibrium_firm_size,
                    "conditional_target_size": outcome.conditional_target_size,
                    "continuous_target_size": outcome.continuous_target_size,
                    "integration_threshold": outcome.integration_threshold,
                    "per_node_surplus_at_target": (outcome.per_node_surplus_at_target),
                },
            }
        )
    payload = {
        "model_version": __version__,
        "result_status": "calibrated theoretical computation; not empirical evidence",
        "examples": examples,
    }
    (output_dir / "firm-size-examples.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    args = parse_args()
    if args.grid < 3:
        raise SystemExit("--grid must be at least 3")
    if args.max_firm_size < 2:
        raise SystemExit("--max-firm-size must be at least 2")
    if args.advantage_max <= args.advantage_min:
        raise SystemExit("advantage maximum must exceed its minimum")
    if args.learning_max <= 0:
        raise SystemExit("--learning-max must be positive")
    if args.organization_cost_min < 0:
        raise SystemExit("organization cost minimum cannot be negative")
    if args.organization_cost_max <= args.organization_cost_min:
        raise SystemExit("organization cost maximum must exceed its minimum")
    if args.integration_cost < 0:
        raise SystemExit("integration cost cannot be negative")
    if not 0 < args.integration_elasticity <= 1:
        raise SystemExit("integration elasticity must be in (0, 1]")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    baseline = _baseline(args)
    baseline.validate()
    advantages = np.linspace(args.advantage_min, args.advantage_max, args.grid)
    learning_values = np.linspace(0.0, args.learning_max, args.grid)
    organization_costs = np.linspace(
        args.organization_cost_min, args.organization_cost_max, args.grid
    )
    result = solve_maps(
        advantages,
        learning_values,
        organization_costs,
        baseline,
    )
    bridges = bridge_examples()

    save_figure(
        args.output_dir / "firm-size-separation-map",
        advantages,
        learning_values,
        organization_costs,
        result,
        baseline,
        bridges,
    )
    write_entry_grid(
        args.output_dir / "firm-size-entry-grid.csv",
        advantages,
        learning_values,
        result,
    )
    write_scale_grid(
        args.output_dir / "firm-size-scale-grid.csv",
        organization_costs,
        learning_values,
        result,
        baseline,
    )
    write_examples(args.output_dir, baseline, bridges)

    baseline_outcome = solve_firm_size(baseline)
    summary = {
        "model_version": __version__,
        "result_status": "calibrated theoretical computation; not empirical evidence",
        "proposed_result": (
            "The per-node hidden-reuse advantage determines integration entry but "
            "not conditional firm size; fixed costs, transferable learning, "
            "declining marginal integration cost, and increasing ongoing "
            "coordination costs determine size."
        ),
        "per_node_surplus_formula": (
            "g(n) = A - K/n + L(n-1)/(kappa+n-1) - d*n^(rho-1) - c*n^eta"
        ),
        "grid_points_per_axis": args.grid,
        "advantage_range": [args.advantage_min, args.advantage_max],
        "learning_range": [0.0, args.learning_max],
        "organization_cost_range": [
            args.organization_cost_min,
            args.organization_cost_max,
        ],
        "baseline": asdict(baseline),
        "baseline_outcome": {
            "regime": baseline_outcome.regime.value,
            "equilibrium_firm_size": baseline_outcome.equilibrium_firm_size,
            "conditional_target_size": baseline_outcome.conditional_target_size,
            "continuous_target_size": baseline_outcome.continuous_target_size,
            "integration_threshold": baseline_outcome.integration_threshold,
            "per_node_surplus_at_target": (baseline_outcome.per_node_surplus_at_target),
        },
        "bilateral_bridge_advantages": {
            name: bridge.internalization_advantage for name, bridge in bridges.items()
        },
        "observed_conditional_size_range": [
            int(np.min(result["scale_size"])),
            int(np.max(result["scale_size"])),
        ],
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
        },
    }
    (args.output_dir / "firm-size-run-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
