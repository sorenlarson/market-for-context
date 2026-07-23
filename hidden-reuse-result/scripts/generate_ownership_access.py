#!/usr/bin/env python3
"""Generate evidence for the platform-versus-rollup network result."""

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
from matplotlib.patches import Circle, Patch

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "src"
if str(SOURCE) not in sys.path:
    sys.path.insert(0, str(SOURCE))

from hidden_reuse import (  # noqa: E402
    HomogeneousOwnershipAccessPrimitives,
    OwnershipAccessRegime,
    __version__,
    homogeneous_network,
    hybrid_suppression_threshold,
    platform_rollup_indifference_efficiency,
    solve_ownership_access,
    vertical_customer_network,
)


REGIME_ORDER = (
    OwnershipAccessRegime.PLATFORM,
    OwnershipAccessRegime.SINGLE_ASSET,
    OwnershipAccessRegime.SPECIALIZED_ROLLUP,
    OwnershipAccessRegime.CROSS_TYPE_ROLLUP,
    OwnershipAccessRegime.FULL_ROLLUP,
)
REGIME_CODE = {regime: index for index, regime in enumerate(REGIME_ORDER)}
REGIME_COLORS = {
    OwnershipAccessRegime.PLATFORM: "#DCE7ED",
    OwnershipAccessRegime.SINGLE_ASSET: "#F2DDA4",
    OwnershipAccessRegime.SPECIALIZED_ROLLUP: "#76A98C",
    OwnershipAccessRegime.CROSS_TYPE_ROLLUP: "#D89B45",
    OwnershipAccessRegime.FULL_ROLLUP: "#C9584C",
}
REGIME_LABELS = {
    OwnershipAccessRegime.PLATFORM: "Neutral platform",
    OwnershipAccessRegime.SINGLE_ASSET: "One acquired asset",
    OwnershipAccessRegime.SPECIALIZED_ROLLUP: "Specialized partial rollup",
    OwnershipAccessRegime.CROSS_TYPE_ROLLUP: "Cross-type partial rollup",
    OwnershipAccessRegime.FULL_ROLLUP: "Full-network rollup",
}

MAP_TITLE = (
    "Customer access can substitute for ownership—and customer conflict polarizes it"
)
MAP_DESCRIPTION = (
    "Two phase maps compare a homogeneous six-asset network with a heterogeneous "
    "network of clinics, laboratories, and payers. The horizontal axis is the "
    "fraction of learning available through arm's-length customer access. The "
    "vertical axis is the share of cross-boundary customer value placed at risk "
    "by partial ownership. At high customer conflict, each map separates into a "
    "neutral platform and a full rollup. At low conflict, partial rollups appear."
)
TOPOLOGY_TITLE = "Equal aggregate learning can imply different firm boundaries"
TOPOLOGY_DESCRIPTION = (
    "Two directed learning networks have the same total edge weight. When learning "
    "is diffuse across complementary clinic, laboratory, and payer links, the "
    "intermediary remains a platform. When the same learning weight is concentrated "
    "within types, the selected firm owns the two clinics."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", type=int, default=61)
    parser.add_argument("--draws", type=int, default=600)
    parser.add_argument("--seed", type=int, default=20260721)
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "outputs")
    return parser.parse_args()


def add_svg_accessibility(
    path: Path, title: str, description: str, prefix: str
) -> None:
    source = path.read_text(encoding="utf-8")
    svg_start = source.index("<svg")
    tag_end = source.index(">", svg_start)
    opening = source[svg_start:tag_end].replace(
        "<svg",
        f'<svg role="img" aria-labelledby="{prefix}-title {prefix}-description"',
        1,
    )
    metadata = (
        f'\n <title id="{prefix}-title">{title}</title>'
        f'\n <desc id="{prefix}-description">{description}</desc>'
    )
    source = (
        source[:svg_start]
        + opening
        + source[tag_end : tag_end + 1]
        + metadata
        + source[tag_end + 1 :]
    )
    path.write_text(source, encoding="utf-8")


def _heterogeneous_endpoint_threshold(network) -> float:
    full = solve_ownership_access(replace(network, external_learning_efficiency=0.0))
    full_candidate = next(
        candidate
        for candidate in full.candidates
        if candidate.size == len(network.nodes)
    )
    total_learning = sum(sum(row) for row in network.learning)
    return full_candidate.incremental_value / total_learning


def solve_grid(efficiencies: np.ndarray, penalties: np.ndarray, builder) -> dict:
    shape = (penalties.size, efficiencies.size)
    regime_code = np.empty(shape, dtype=int)
    ownership_size = np.empty(shape, dtype=int)
    incremental_value = np.empty(shape)
    selection_margin = np.empty(shape)
    owned_names = np.empty(shape, dtype=object)
    for row, penalty in enumerate(penalties):
        for column, efficiency in enumerate(efficiencies):
            outcome = solve_ownership_access(builder(float(efficiency), float(penalty)))
            regime_code[row, column] = REGIME_CODE[outcome.regime]
            ownership_size[row, column] = outcome.ownership_size
            incremental_value[row, column] = outcome.incremental_value
            selection_margin[row, column] = outcome.selection_margin
            owned_names[row, column] = "|".join(outcome.owned_names)
    return {
        "regime_code": regime_code,
        "ownership_size": ownership_size,
        "incremental_value": incremental_value,
        "selection_margin": selection_margin,
        "owned_names": owned_names,
    }


def save_regime_map(
    output_base: Path,
    efficiencies: np.ndarray,
    penalties: np.ndarray,
    homogeneous: dict,
    heterogeneous: dict,
    homogeneous_threshold: float,
    heterogeneous_threshold: float,
) -> None:
    colors = [REGIME_COLORS[regime] for regime in REGIME_ORDER]
    cmap = ListedColormap(colors)
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.5), constrained_layout=True)
    panels = [
        (
            axes[0],
            homogeneous,
            homogeneous_threshold,
            "A. Six otherwise similar assets",
        ),
        (
            axes[1],
            heterogeneous,
            heterogeneous_threshold,
            "B. Clinics, labs, and payers",
        ),
    ]
    for ax, result, threshold, title in panels:
        ax.imshow(
            result["regime_code"],
            origin="lower",
            aspect="auto",
            interpolation="nearest",
            extent=(0, 1, 0, 1),
            cmap=cmap,
            vmin=-0.5,
            vmax=len(REGIME_ORDER) - 0.5,
        )
        ax.axvline(
            threshold,
            color="#1B1B1B",
            linewidth=1.5,
            linestyle="--",
        )
        ax.set(
            xlim=(0, 1),
            ylim=(0, 1),
            xlabel="Learning available without ownership, q",
            title=title,
        )
        ax.grid(False)
    axes[0].set_ylabel("Cross-boundary customer value at risk, χ")
    axes[0].text(0.12, 0.84, "FULL\nROLLUP", ha="center", va="center", fontsize=10)
    axes[0].text(0.84, 0.84, "NEUTRAL\nPLATFORM", ha="center", va="center", fontsize=10)
    axes[1].text(0.12, 0.84, "FULL\nROLLUP", ha="center", va="center", fontsize=10)
    axes[1].text(0.84, 0.84, "NEUTRAL\nPLATFORM", ha="center", va="center", fontsize=10)
    legend_handles = [
        Patch(color=REGIME_COLORS[regime], label=REGIME_LABELS[regime])
        for regime in REGIME_ORDER
    ]
    legend_handles.append(
        Line2D(
            [0],
            [0],
            color="#1B1B1B",
            linestyle="--",
            label="Platform/full-rollup indifference",
        )
    )
    fig.legend(
        handles=legend_handles,
        loc="outside lower center",
        ncol=3,
        frameon=False,
    )
    fig.suptitle(MAP_TITLE, fontsize=14, fontweight="semibold")
    for suffix in ("png", "svg"):
        path = output_base.with_suffix(f".{suffix}")
        fig.savefig(path, dpi=190, bbox_inches="tight")
        if suffix == "svg":
            add_svg_accessibility(
                path,
                MAP_TITLE,
                MAP_DESCRIPTION,
                "ownership-access-map",
            )
    plt.close(fig)


def _draw_arrow(ax, start, end, weight, maximum, color="#6A7278") -> None:
    direction = np.asarray(end) - np.asarray(start)
    length = float(np.linalg.norm(direction))
    if length == 0:
        return
    unit = direction / length
    shifted_start = np.asarray(start) + unit * 0.13
    shifted_end = np.asarray(end) - unit * 0.16
    ax.annotate(
        "",
        xy=shifted_end,
        xytext=shifted_start,
        arrowprops={
            "arrowstyle": "-|>",
            "color": color,
            "alpha": 0.22 + 0.63 * weight / maximum,
            "linewidth": 0.5 + 3.0 * weight / maximum,
            "shrinkA": 0,
            "shrinkB": 0,
            "connectionstyle": "arc3,rad=0.08",
        },
        zorder=1,
    )


def save_topology_figure(output_base: Path) -> dict:
    q = 0.85
    chi = 0.10
    complementary = vertical_customer_network(
        learning_topology="complementary",
        external_learning_efficiency=q,
        neutrality_penalty=chi,
    )
    within_type = vertical_customer_network(
        learning_topology="within_type",
        external_learning_efficiency=q,
        neutrality_penalty=chi,
    )
    scenarios = [
        ("A. Complementary across types", complementary),
        ("B. Concentrated within types", within_type),
    ]
    positions = {
        "clinic_east": (0.0, 1.0),
        "lab_east": (1.0, 1.0),
        "payer_east": (2.0, 1.0),
        "clinic_west": (0.0, 0.0),
        "lab_west": (1.0, 0.0),
        "payer_west": (2.0, 0.0),
    }
    node_colors = {"clinic": "#4C78A8", "lab": "#59A14F", "payer": "#B279A2"}
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.8), constrained_layout=True)
    outcomes = {}
    for ax, (title, network) in zip(axes, scenarios):
        outcome = solve_ownership_access(network)
        outcomes[title] = outcome
        maximum = max(max(row) for row in network.learning)
        cutoff = 0.20 * maximum
        for source, source_node in enumerate(network.nodes):
            for target, target_node in enumerate(network.nodes):
                weight = network.learning[source][target]
                if weight >= cutoff:
                    _draw_arrow(
                        ax,
                        positions[source_node.name],
                        positions[target_node.name],
                        weight,
                        maximum,
                    )
        for node in network.nodes:
            x, y = positions[node.name]
            owned = node.name in outcome.owned_names
            circle = Circle(
                (x, y),
                radius=0.12,
                facecolor=node_colors[node.kind] if owned else "white",
                edgecolor=node_colors[node.kind],
                linewidth=3.0 if owned else 1.7,
                zorder=3,
            )
            ax.add_patch(circle)
            ax.text(x, y - 0.22, node.name.replace("_", " "), ha="center", fontsize=8)
        ax.set(
            xlim=(-0.35, 2.35),
            ylim=(-0.38, 1.32),
            aspect="equal",
            title=title,
        )
        ax.axis("off")
        ax.text(
            1.0,
            -0.36,
            "Selected owner: "
            + (", ".join(outcome.owned_names) or "none (neutral platform)"),
            ha="center",
            fontsize=9,
            fontweight="semibold",
        )
    legend = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="none",
            markerfacecolor=color,
            markeredgecolor=color,
            markersize=9,
            label=kind.title(),
        )
        for kind, color in node_colors.items()
    ]
    legend.append(
        Line2D(
            [0],
            [0],
            marker="o",
            color="none",
            markerfacecolor="#555555",
            markeredgecolor="#555555",
            markeredgewidth=2.5,
            markersize=9,
            label="Filled node = owned",
        )
    )
    fig.legend(handles=legend, loc="outside lower center", ncol=4, frameon=False)
    fig.suptitle(TOPOLOGY_TITLE, fontsize=14, fontweight="semibold")
    for suffix in ("png", "svg"):
        path = output_base.with_suffix(f".{suffix}")
        fig.savefig(path, dpi=190, bbox_inches="tight")
        if suffix == "svg":
            add_svg_accessibility(
                path,
                TOPOLOGY_TITLE,
                TOPOLOGY_DESCRIPTION,
                "ownership-topology",
            )
    plt.close(fig)
    return {
        "external_learning_efficiency": q,
        "neutrality_penalty": chi,
        "aggregate_learning_weight": sum(sum(row) for row in complementary.learning),
        "complementary": {
            "regime": outcomes["A. Complementary across types"].regime.value,
            "owned_names": outcomes["A. Complementary across types"].owned_names,
            "incremental_value": outcomes[
                "A. Complementary across types"
            ].incremental_value,
        },
        "within_type": {
            "regime": outcomes["B. Concentrated within types"].regime.value,
            "owned_names": outcomes["B. Concentrated within types"].owned_names,
            "incremental_value": outcomes[
                "B. Concentrated within types"
            ].incremental_value,
        },
    }


def write_grid(
    path: Path,
    efficiencies: np.ndarray,
    penalties: np.ndarray,
    results: dict,
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "network",
                "external_learning_efficiency",
                "neutrality_penalty",
                "regime",
                "ownership_size",
                "owned_names",
                "incremental_value",
                "selection_margin",
            ]
        )
        for network_name, result in results.items():
            for row, penalty in enumerate(penalties):
                for column, efficiency in enumerate(efficiencies):
                    regime = REGIME_ORDER[result["regime_code"][row, column]]
                    writer.writerow(
                        [
                            network_name,
                            f"{efficiency:.8f}",
                            f"{penalty:.8f}",
                            regime.value,
                            int(result["ownership_size"][row, column]),
                            result["owned_names"][row, column],
                            f"{result['incremental_value'][row, column]:.8f}",
                            f"{result['selection_margin'][row, column]:.8f}",
                        ]
                    )


def _perturb_vertical_network(base, rng: np.random.Generator):
    size = len(base.nodes)
    learning_shock = rng.lognormal(-0.5 * 0.25**2, 0.25, size=(size, size))
    customer_shock = rng.lognormal(-0.5 * 0.20**2, 0.20, size=(size, size))
    learning = tuple(
        tuple(
            0.0
            if source == target
            else base.learning[source][target] * learning_shock[source, target]
            for target in range(size)
        )
        for source in range(size)
    )
    customer = tuple(
        tuple(
            0.0
            if source == target
            else base.customer_dependence[source][target]
            * customer_shock[source, target]
            for target in range(size)
        )
        for source in range(size)
    )
    nodes = tuple(
        replace(
            node,
            internalization_advantage=(
                node.internalization_advantage + float(rng.normal(0.0, 0.02))
            ),
        )
        for node in base.nodes
    )
    return replace(
        base,
        nodes=nodes,
        learning=learning,
        customer_dependence=customer,
        organization_cost_scale=(
            base.organization_cost_scale * float(rng.lognormal(-0.5 * 0.12**2, 0.12))
        ),
    )


def write_robustness(path: Path, draws: int, seed: int) -> dict:
    scenarios = {
        "low_access_high_conflict": (0.40, 0.80),
        "intermediate_access_low_conflict": (0.60, 0.10),
        "high_access_high_conflict": (0.80, 0.80),
    }
    rng = np.random.default_rng(seed)
    base = vertical_customer_network()
    counts = {name: {regime.value: 0 for regime in REGIME_ORDER} for name in scenarios}
    size_totals = {name: 0 for name in scenarios}
    for _ in range(draws):
        perturbed = _perturb_vertical_network(base, rng)
        for name, (efficiency, penalty) in scenarios.items():
            outcome = solve_ownership_access(
                replace(
                    perturbed,
                    external_learning_efficiency=efficiency,
                    neutrality_penalty=penalty,
                )
            )
            counts[name][outcome.regime.value] += 1
            size_totals[name] += outcome.ownership_size
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "scenario",
                "external_learning_efficiency",
                "neutrality_penalty",
                "regime",
                "probability",
                "mean_ownership_size",
                "draws",
                "seed",
            ]
        )
        for name, (efficiency, penalty) in scenarios.items():
            mean_size = size_totals[name] / draws
            for regime in REGIME_ORDER:
                writer.writerow(
                    [
                        name,
                        f"{efficiency:.8f}",
                        f"{penalty:.8f}",
                        regime.value,
                        f"{counts[name][regime.value] / draws:.8f}",
                        f"{mean_size:.8f}",
                        draws,
                        seed,
                    ]
                )
    return {
        name: {
            "external_learning_efficiency": scenarios[name][0],
            "neutrality_penalty": scenarios[name][1],
            "mean_ownership_size": size_totals[name] / draws,
            "regime_probabilities": {
                regime: count / draws for regime, count in regime_counts.items()
            },
        }
        for name, regime_counts in counts.items()
    }


def candidate_json(candidate) -> dict:
    result = asdict(candidate)
    result["regime"] = candidate.regime.value
    return result


def worked_examples() -> dict:
    scenarios = {
        "platform": vertical_customer_network(
            external_learning_efficiency=0.80, neutrality_penalty=0.80
        ),
        "partial_complementary_rollup": vertical_customer_network(
            external_learning_efficiency=0.60, neutrality_penalty=0.10
        ),
        "full_rollup": vertical_customer_network(
            external_learning_efficiency=0.40, neutrality_penalty=0.80
        ),
    }
    result = {}
    for name, primitives in scenarios.items():
        outcome = solve_ownership_access(primitives)
        result[name] = {
            "external_learning_efficiency": primitives.external_learning_efficiency,
            "neutrality_penalty": primitives.neutrality_penalty,
            "regime": outcome.regime.value,
            "owned_names": outcome.owned_names,
            "ownership_size": outcome.ownership_size,
            "incremental_value": outcome.incremental_value,
            "selection_margin": outcome.selection_margin,
            "maximum_deviation_gain": outcome.maximum_deviation_gain,
            "value_decomposition": candidate_json(outcome.chosen),
        }
    return result


def main() -> None:
    args = parse_args()
    if args.grid < 3:
        raise SystemExit("--grid must be at least 3")
    if args.draws < 1:
        raise SystemExit("--draws must be positive")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    efficiencies = np.linspace(0.0, 1.0, args.grid)
    penalties = np.linspace(0.0, 1.0, args.grid)

    homogeneous_base = HomogeneousOwnershipAccessPrimitives()
    homogeneous = solve_grid(
        efficiencies,
        penalties,
        lambda efficiency, penalty: homogeneous_network(
            replace(
                homogeneous_base,
                external_learning_efficiency=efficiency,
                neutrality_penalty=penalty,
            )
        ),
    )
    heterogeneous_base = vertical_customer_network()
    heterogeneous = solve_grid(
        efficiencies,
        penalties,
        lambda efficiency, penalty: replace(
            heterogeneous_base,
            external_learning_efficiency=efficiency,
            neutrality_penalty=penalty,
        ),
    )
    homogeneous_threshold = platform_rollup_indifference_efficiency(homogeneous_base)
    assert homogeneous_threshold is not None
    heterogeneous_threshold = _heterogeneous_endpoint_threshold(heterogeneous_base)
    save_regime_map(
        args.output_dir / "ownership-access-regime-map",
        efficiencies,
        penalties,
        homogeneous,
        heterogeneous,
        homogeneous_threshold,
        heterogeneous_threshold,
    )
    topology = save_topology_figure(args.output_dir / "ownership-access-topology")
    write_grid(
        args.output_dir / "ownership-access-grid.csv",
        efficiencies,
        penalties,
        {"homogeneous": homogeneous, "heterogeneous_vertical": heterogeneous},
    )
    robustness = write_robustness(
        args.output_dir / "ownership-access-robustness.csv", args.draws, args.seed
    )
    examples = worked_examples()
    (args.output_dir / "ownership-access-examples.json").write_text(
        json.dumps(
            {"examples": examples, "topology_counterfactual": topology},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    summary = {
        "model_version": __version__,
        "result_status": (
            "Calibrated theoretical computation and synthetic robustness exercise; "
            "not empirical evidence about current AI markets."
        ),
        "solver": "exact enumeration of all 2^6 ownership subsets",
        "grid_points_per_axis": args.grid,
        "robustness_draws": args.draws,
        "seed": args.seed,
        "homogeneous_primitives": asdict(homogeneous_base),
        "homogeneous_platform_rollup_indifference_efficiency": (homogeneous_threshold),
        "homogeneous_hybrid_suppression_at_q_0_55": hybrid_suppression_threshold(
            replace(homogeneous_base, external_learning_efficiency=0.55)
        ),
        "homogeneous_hybrid_suppression_at_q_0_60": hybrid_suppression_threshold(
            replace(homogeneous_base, external_learning_efficiency=0.60)
        ),
        "heterogeneous_platform_rollup_indifference_efficiency": (
            heterogeneous_threshold
        ),
        "robustness": robustness,
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
        },
    }
    (args.output_dir / "ownership-access-run-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
