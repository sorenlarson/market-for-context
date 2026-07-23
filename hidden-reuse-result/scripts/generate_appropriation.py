#!/usr/bin/env python3
"""Generate evidence for the access-versus-appropriation result."""

import argparse
import csv
import json
import platform
import sys
from dataclasses import replace
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "src"
if str(SOURCE) not in sys.path:
    sys.path.insert(0, str(SOURCE))

from hidden_reuse import (  # noqa: E402
    HomogeneousValueAppropriationPrimitives,
    OwnershipAccessRegime,
    ParetoTaskPrimitives,
    __version__,
    homogeneous_value_candidate_increment,
    homogeneous_value_network,
    platform_rollup_capture_threshold,
    solve_pareto_pricing,
    solve_value_appropriation,
)


REGIME_ORDER = (
    OwnershipAccessRegime.PLATFORM,
    OwnershipAccessRegime.SPECIALIZED_ROLLUP,
    OwnershipAccessRegime.FULL_ROLLUP,
)
REGIME_CODE = {regime: index for index, regime in enumerate(REGIME_ORDER)}
REGIME_COLORS = {
    OwnershipAccessRegime.PLATFORM: "#DCE7ED",
    OwnershipAccessRegime.SPECIALIZED_ROLLUP: "#76A98C",
    OwnershipAccessRegime.FULL_ROLLUP: "#C9584C",
}
REGIME_LABELS = {
    OwnershipAccessRegime.PLATFORM: "Neutral platform",
    OwnershipAccessRegime.SPECIALIZED_ROLLUP: "Partial platform-owner",
    OwnershipAccessRegime.FULL_ROLLUP: "Full rollup",
}

FIGURE_TITLE = "Access is not appropriation"
FIGURE_DESCRIPTION = (
    "Two phase maps plot the fraction of learning available through customer "
    "access horizontally and the platform's share of AI-created operating "
    "value vertically. When customer conflict is high, low provider capture "
    "supports a full rollup even at complete external learning access, while "
    "high access and high capture support a neutral platform. When customer "
    "conflict is low, partial platform-owner structures survive."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", type=int, default=81)
    parser.add_argument("--draws", type=int, default=600)
    parser.add_argument("--seed", type=int, default=20260722)
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


def equivalent_pareto_tail(capture_share: float) -> Optional[float]:
    """Invert theta=(alpha-1)/(2 alpha-1) for theta in [0, 1/2)."""

    if not 0 < capture_share < 0.5:
        return None
    return (1.0 - capture_share) / (1.0 - 2.0 * capture_share)


def _regime_for_size(size: int, total: int) -> OwnershipAccessRegime:
    if size == 0:
        return OwnershipAccessRegime.PLATFORM
    if size == total:
        return OwnershipAccessRegime.FULL_ROLLUP
    return OwnershipAccessRegime.SPECIALIZED_ROLLUP


def _homogeneous_components(
    owned_size: int, primitives: HomogeneousValueAppropriationPrimitives
) -> dict[str, float]:
    if owned_size == 0:
        return {
            "owned_operating_surplus": 0.0,
            "internal_learning": 0.0,
            "incoming_customer_learning": 0.0,
            "internalization_value": 0.0,
            "capture_upgrade": 0.0,
            "productive_learning_upgrade": 0.0,
            "external_access_slope": 0.0,
            "ownership_cost": 0.0,
            "incremental_private_value": 0.0,
        }
    total = primitives.asset_count
    internal = primitives.directed_pair_learning * owned_size * (owned_size - 1)
    incoming = primitives.directed_pair_learning * owned_size * (total - owned_size)
    operating = primitives.per_asset_operating_surplus * owned_size
    direct = primitives.internalization_advantage * owned_size
    capture = (primitives.owner_capture_share - primitives.platform_capture_share) * (
        operating + primitives.external_learning_efficiency * (internal + incoming)
    )
    learning = (
        primitives.owner_capture_share
        * (1.0 - primitives.external_learning_efficiency)
        * internal
    )
    fixed = primitives.fixed_ownership_cost
    organization = (
        primitives.organization_cost_scale
        * owned_size**primitives.organization_cost_elasticity
    )
    coordination = (
        primitives.pair_coordination_cost * owned_size * (owned_size - 1) / 2.0
    )
    neutrality = (
        primitives.neutrality_penalty
        * primitives.boundary_customer_value_per_unordered_pair
        * owned_size
        * (total - owned_size)
    )
    costs = fixed + organization + coordination + neutrality
    return {
        "owned_operating_surplus": operating,
        "internal_learning": internal,
        "incoming_customer_learning": incoming,
        "internalization_value": direct,
        "capture_upgrade": capture,
        "productive_learning_upgrade": learning,
        "external_access_slope": (
            primitives.owner_capture_share - primitives.platform_capture_share
        )
        * incoming
        - primitives.platform_capture_share * internal,
        "ownership_cost": costs,
        "incremental_private_value": direct + capture + learning - costs,
    }


def _select_homogeneous(
    primitives: HomogeneousValueAppropriationPrimitives,
) -> tuple[int, dict[str, float], float]:
    values = np.array(
        [
            homogeneous_value_candidate_increment(size, primitives)
            for size in range(primitives.asset_count + 1)
        ]
    )
    best = float(values.max())
    maximizing = np.flatnonzero(np.isclose(values, best, atol=1e-10, rtol=0.0))
    selected = int(maximizing.min())
    alternatives = np.delete(values, selected)
    margin = best - float(alternatives.max()) if alternatives.size else 0.0
    return selected, _homogeneous_components(selected, primitives), margin


def solve_grid(
    efficiencies: np.ndarray,
    capture_shares: np.ndarray,
    *,
    neutrality_penalty: float,
) -> dict[str, np.ndarray]:
    shape = (capture_shares.size, efficiencies.size)
    regime_code = np.empty(shape, dtype=int)
    ownership_size = np.empty(shape, dtype=int)
    incremental = np.empty(shape)
    capture_upgrade = np.empty(shape)
    learning_upgrade = np.empty(shape)
    access_slope = np.empty(shape)
    selection_margin = np.empty(shape)
    base = HomogeneousValueAppropriationPrimitives(
        neutrality_penalty=neutrality_penalty
    )
    for row, capture in enumerate(capture_shares):
        for column, efficiency in enumerate(efficiencies):
            primitives = replace(
                base,
                external_learning_efficiency=float(efficiency),
                platform_capture_share=float(capture),
            )
            size, components, margin = _select_homogeneous(primitives)
            regime = _regime_for_size(size, primitives.asset_count)
            regime_code[row, column] = REGIME_CODE[regime]
            ownership_size[row, column] = size
            incremental[row, column] = components["incremental_private_value"]
            capture_upgrade[row, column] = components["capture_upgrade"]
            learning_upgrade[row, column] = components["productive_learning_upgrade"]
            access_slope[row, column] = components["external_access_slope"]
            selection_margin[row, column] = margin
    return {
        "regime_code": regime_code,
        "ownership_size": ownership_size,
        "incremental_private_value": incremental,
        "capture_upgrade": capture_upgrade,
        "productive_learning_upgrade": learning_upgrade,
        "external_access_slope": access_slope,
        "selection_margin": selection_margin,
    }


def save_regime_map(
    output_base: Path,
    efficiencies: np.ndarray,
    capture_shares: np.ndarray,
    high_conflict: dict[str, np.ndarray],
    low_conflict: dict[str, np.ndarray],
) -> None:
    cmap = ListedColormap([REGIME_COLORS[regime] for regime in REGIME_ORDER])
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.7), constrained_layout=True)
    panels = [
        (axes[0], high_conflict, "A. Customer conflict eliminates hybrids"),
        (axes[1], low_conflict, "B. Neutral customers permit partial ownership"),
    ]
    for ax, result, title in panels:
        ax.imshow(
            result["regime_code"],
            origin="lower",
            aspect="auto",
            interpolation="nearest",
            extent=(0.0, 1.0, 0.0, 0.5),
            cmap=cmap,
            vmin=-0.5,
            vmax=len(REGIME_ORDER) - 0.5,
        )
        boundary = np.array(
            [
                platform_rollup_capture_threshold(
                    replace(
                        HomogeneousValueAppropriationPrimitives(),
                        external_learning_efficiency=float(efficiency),
                    )
                )
                for efficiency in efficiencies
            ]
        )
        ax.plot(
            efficiencies,
            boundary,
            color="#1B1B1B",
            linestyle="--",
            linewidth=1.5,
        )
        alpha_anchor = solve_pareto_pricing(
            ParetoTaskPrimitives(tail_index=1.5)
        ).provider_capture_share
        ax.axhline(
            alpha_anchor,
            color="#555555",
            linestyle=":",
            linewidth=1.2,
        )
        ax.set(
            xlim=(0.0, 1.0),
            ylim=(0.0, 0.5),
            xlabel="Learning available without ownership, q",
            title=title,
        )
        ax.grid(False)
    axes[0].set_ylabel("Platform share of AI-created operating value")
    axes[0].text(0.15, 0.15, "FULL\nROLLUP", ha="center", va="center", fontsize=10)
    axes[0].text(0.82, 0.43, "NEUTRAL\nPLATFORM", ha="center", va="center", fontsize=10)
    axes[0].annotate(
        "Ownership can win even when q = 1",
        xy=(0.995, 0.20),
        xytext=(0.55, 0.08),
        arrowprops={"arrowstyle": "->", "color": "#444444"},
        fontsize=9,
    )
    axes[1].text(
        0.52,
        0.29,
        "PARTIAL\nPLATFORM-OWNER",
        ha="center",
        va="center",
        fontsize=9,
    )
    axes[1].text(0.82, 0.43, "NEUTRAL\nPLATFORM", ha="center", va="center", fontsize=10)
    pareto_ticks = []
    pareto_labels = []
    for alpha in (1.2, 1.5, 2.0, 3.0, 5.0):
        share = solve_pareto_pricing(
            ParetoTaskPrimitives(tail_index=alpha)
        ).provider_capture_share
        pareto_ticks.append(share)
        pareto_labels.append(f"α={alpha:g}")
    alpha_axis = axes[1].twinx()
    alpha_axis.set_ylim(axes[1].get_ylim())
    alpha_axis.set_yticks(pareto_ticks, labels=pareto_labels)
    alpha_axis.set_ylabel("Equivalent Pareto task-value tail")

    handles = [
        Patch(color=REGIME_COLORS[regime], label=REGIME_LABELS[regime])
        for regime in REGIME_ORDER
    ]
    handles.extend(
        [
            Line2D(
                [0],
                [0],
                color="#1B1B1B",
                linestyle="--",
                label="Platform/full-rollup indifference",
            ),
            Line2D(
                [0],
                [0],
                color="#555555",
                linestyle=":",
                label="Blog calibration: α=1.5, capture=25%",
            ),
        ]
    )
    fig.legend(handles=handles, loc="outside lower center", ncol=3, frameon=False)
    fig.suptitle(
        "Access is not appropriation: learning can travel while its value cannot be priced",
        fontsize=14,
        fontweight="semibold",
    )
    for suffix in ("png", "svg"):
        path = output_base.with_suffix(f".{suffix}")
        fig.savefig(path, dpi=190, bbox_inches="tight")
        if suffix == "svg":
            add_svg_accessibility(
                path,
                FIGURE_TITLE,
                FIGURE_DESCRIPTION,
                "value-appropriation-map",
            )
    plt.close(fig)


def write_grid(
    path: Path,
    efficiencies: np.ndarray,
    capture_shares: np.ndarray,
    result: dict[str, np.ndarray],
    *,
    neutrality_penalty: float,
) -> None:
    base = HomogeneousValueAppropriationPrimitives(
        neutrality_penalty=neutrality_penalty
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "external_learning_efficiency",
                "platform_capture_share",
                "equivalent_pareto_tail_index",
                "neutrality_penalty",
                "regime",
                "ownership_size",
                "incremental_private_value",
                "capture_upgrade",
                "productive_learning_upgrade",
                "external_access_slope",
                "selection_margin",
                "platform_full_rollup_capture_threshold",
            ]
        )
        for row, capture in enumerate(capture_shares):
            alpha = equivalent_pareto_tail(float(capture))
            for column, efficiency in enumerate(efficiencies):
                size = int(result["ownership_size"][row, column])
                regime = _regime_for_size(size, base.asset_count)
                threshold = platform_rollup_capture_threshold(
                    replace(base, external_learning_efficiency=float(efficiency))
                )
                writer.writerow(
                    [
                        f"{efficiency:.8f}",
                        f"{capture:.8f}",
                        "" if alpha is None else f"{alpha:.8f}",
                        f"{neutrality_penalty:.8f}",
                        regime.value,
                        size,
                        f"{result['incremental_private_value'][row, column]:.8f}",
                        f"{result['capture_upgrade'][row, column]:.8f}",
                        f"{result['productive_learning_upgrade'][row, column]:.8f}",
                        f"{result['external_access_slope'][row, column]:.8f}",
                        f"{result['selection_margin'][row, column]:.8f}",
                        "" if threshold is None else f"{threshold:.8f}",
                    ]
                )


def write_pareto_benchmark(path: Path) -> None:
    alphas = np.concatenate([np.linspace(1.05, 2.0, 39), np.linspace(2.1, 10.0, 80)])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "tail_index",
                "monopoly_price",
                "quantity",
                "provider_profit",
                "customer_surplus",
                "platform_total_surplus",
                "integrated_operating_surplus",
                "provider_capture_share",
                "pricing_deadweight_loss",
            ]
        )
        for alpha in alphas:
            outcome = solve_pareto_pricing(
                ParetoTaskPrimitives(tail_index=float(alpha))
            )
            writer.writerow(
                [
                    f"{alpha:.8f}",
                    f"{outcome.monopoly_price:.8f}",
                    f"{outcome.quantity:.8f}",
                    f"{outcome.provider_profit:.8f}",
                    f"{outcome.customer_surplus:.8f}",
                    f"{outcome.platform_total_surplus:.8f}",
                    f"{outcome.integrated_operating_surplus:.8f}",
                    f"{outcome.provider_capture_share:.8f}",
                    f"{outcome.pricing_deadweight_loss:.8f}",
                ]
            )


def _serialize_outcome(
    name: str,
    primitives: HomogeneousValueAppropriationPrimitives,
) -> dict:
    outcome = solve_value_appropriation(homogeneous_value_network(primitives))
    return {
        "name": name,
        "external_learning_efficiency": primitives.external_learning_efficiency,
        "platform_capture_share": primitives.platform_capture_share,
        "owner_capture_share": primitives.owner_capture_share,
        "neutrality_penalty": primitives.neutrality_penalty,
        "regime": outcome.regime.value,
        "ownership_size": outcome.ownership_size,
        "incremental_private_value": outcome.incremental_private_value,
        "capture_upgrade": outcome.chosen.capture_upgrade,
        "productive_learning_upgrade": (outcome.chosen.productive_learning_upgrade),
        "external_access_slope": outcome.chosen.external_access_slope,
        "selection_margin": outcome.selection_margin,
        "maximum_deviation_gain": outcome.maximum_deviation_gain,
    }


def write_examples(path: Path) -> dict[str, dict]:
    high_conflict = 5.0
    low_conflict = 0.0
    scenarios = {
        "learning_driven_rollup": HomogeneousValueAppropriationPrimitives(
            external_learning_efficiency=0.05,
            platform_capture_share=0.40,
            neutrality_penalty=high_conflict,
        ),
        "capture_driven_rollup_at_full_access": (
            HomogeneousValueAppropriationPrimitives(
                external_learning_efficiency=1.0,
                platform_capture_share=0.25,
                neutrality_penalty=high_conflict,
            )
        ),
        "neutral_platform": HomogeneousValueAppropriationPrimitives(
            external_learning_efficiency=0.90,
            platform_capture_share=0.40,
            neutrality_penalty=high_conflict,
        ),
        "platform_fed_partial_owner": HomogeneousValueAppropriationPrimitives(
            external_learning_efficiency=0.97,
            platform_capture_share=0.17,
            neutrality_penalty=low_conflict,
        ),
    }
    serialized = {
        key: _serialize_outcome(key, primitives)
        for key, primitives in scenarios.items()
    }
    payload = {
        "model_version": __version__,
        "claim_status": "Calibrated theoretical examples, not empirical evidence.",
        "scenarios": serialized,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return serialized


def write_robustness(
    path: Path,
    *,
    draws: int,
    seed: int,
) -> dict[str, dict]:
    rng = np.random.default_rng(seed)
    anchors = {
        "learning_driven_rollup": (0.05, 0.40, 5.0),
        "capture_driven_rollup_at_full_access": (1.00, 0.25, 5.0),
        "neutral_platform": (0.90, 0.40, 5.0),
        "platform_fed_partial_owner": (0.97, 0.17, 0.0),
    }
    counts = {name: {regime.value: 0 for regime in REGIME_ORDER} for name in anchors}
    size_totals = {name: 0.0 for name in anchors}
    for _ in range(draws):
        value_scale = rng.lognormal(mean=-0.5 * 0.15**2, sigma=0.15)
        learning_scale = rng.lognormal(mean=-0.5 * 0.18**2, sigma=0.18)
        operating_scale = rng.lognormal(mean=-0.5 * 0.18**2, sigma=0.18)
        cost_scale = rng.lognormal(mean=-0.5 * 0.12**2, sigma=0.12)
        owner_share = float(np.clip(rng.normal(0.45, 0.025), 0.0, 1.0))
        for name, (efficiency, capture, conflict) in anchors.items():
            primitives = HomogeneousValueAppropriationPrimitives(
                internalization_advantage=0.215 * value_scale,
                directed_pair_learning=0.105 * learning_scale,
                per_asset_operating_surplus=0.80 * operating_scale,
                external_learning_efficiency=efficiency,
                platform_capture_share=capture,
                owner_capture_share=owner_share,
                fixed_ownership_cost=0.150 * cost_scale,
                organization_cost_scale=0.100 * cost_scale,
                pair_coordination_cost=0.027 * cost_scale,
                neutrality_penalty=conflict,
            )
            size, _, _ = _select_homogeneous(primitives)
            regime = _regime_for_size(size, primitives.asset_count)
            counts[name][regime.value] += 1
            size_totals[name] += size

    summary = {}
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "scenario",
                "draws",
                "regime",
                "frequency",
                "mean_ownership_size",
                "seed",
            ]
        )
        for name in anchors:
            frequencies = {
                regime.value: counts[name][regime.value] / draws
                for regime in REGIME_ORDER
            }
            mean_size = size_totals[name] / draws
            summary[name] = {
                "frequencies": frequencies,
                "mean_ownership_size": mean_size,
            }
            for regime in REGIME_ORDER:
                writer.writerow(
                    [
                        name,
                        draws,
                        regime.value,
                        f"{frequencies[regime.value]:.8f}",
                        f"{mean_size:.8f}",
                        seed,
                    ]
                )
    return summary


def write_explorer(path: Path) -> None:
    path.write_text(
        """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Access versus appropriation explorer</title>
<style>
:root{color-scheme:light dark;font-family:ui-sans-serif,system-ui,sans-serif}
body{margin:0;padding:1.25rem;background:Canvas;color:CanvasText}
main{max-width:900px;margin:auto}fieldset{border:1px solid color-mix(in srgb,CanvasText 25%,transparent);border-radius:.5rem;margin:1rem 0;padding:1rem}
.controls{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem}label{display:grid;gap:.35rem}input{width:100%}
svg{display:block;width:100%;height:auto}.axis{stroke:CanvasText;stroke-width:1}.boundary{stroke:CanvasText;stroke-width:2;fill:none;stroke-dasharray:6 4}.platform{fill:#6f9fb7;fill-opacity:.38}.rollup{fill:#c9584c;fill-opacity:.42}.marker{fill:CanvasText}.muted{opacity:.7}.result{font-weight:600}
</style>
</head>
<body><main>
<h1>Access versus appropriation</h1>
<p>This explorer compares a neutral AI platform with a full six-asset rollup. Partial ownership is suppressed so the pure boundary remains visible.</p>
<fieldset><legend>Assumptions</legend><div class="controls">
<label>External learning efficiency q <output id="qv">0.55</output><input id="q" type="range" min="0" max="1" step="0.01" value="0.55"></label>
<label>Platform capture share p <output id="pv">0.25</output><input id="p" type="range" min="0" max="0.5" step="0.01" value="0.25"></label>
<label>Owner retained share o <output id="ov">0.45</output><input id="o" type="range" min="0" max="1" step="0.01" value="0.45"></label>
</div></fieldset>
<svg viewBox="0 0 760 420" role="img" aria-labelledby="title desc"><title id="title">Platform and rollup boundary</title><desc id="desc">The selected point moves over a map of external learning efficiency and platform value capture.</desc>
<path id="rollup" class="rollup"></path><path id="platform" class="platform"></path><path id="boundary" class="boundary"></path><path class="axis" d="M70 25V360H720"></path>
<g font-size="13" fill="currentColor"><text x="395" y="405" text-anchor="middle">Learning available without ownership, q</text><text x="16" y="192" transform="rotate(-90 16 192)" text-anchor="middle">Platform capture share</text><text x="92" y="325">Full rollup</text><text x="570" y="70">Neutral platform</text></g><circle id="marker" class="marker" r="6"></circle>
</svg>
<p id="result" class="result"></p><p id="detail" class="muted"></p>
<script>
(()=>{const q=document.getElementById('q'),p=document.getElementById('p'),o=document.getElementById('o');const qv=document.getElementById('qv'),pv=document.getElementById('pv'),ov=document.getElementById('ov'),marker=document.getElementById('marker'),boundary=document.getElementById('boundary'),rollup=document.getElementById('rollup'),platform=document.getElementById('platform'),result=document.getElementById('result'),detail=document.getElementById('detail');const X=x=>70+650*x,Y=y=>360-670*y;const n=6,a=.215,b=.8,g=.105,K=.15,c=.1,rho=1.7,h=.027;const learning=g*n*(n-1),operating=b*n,cost=K+c*n**rho+h*n*(n-1)/2;
function threshold(x,owner){return(n*a+owner*(operating+learning)-cost)/(operating+x*learning)}
function render(){const Q=+q.value,P=+p.value,O=+o.value;qv.value=Q.toFixed(2);pv.value=P.toFixed(2);ov.value=O.toFixed(2);let pts=[];for(let i=0;i<=100;i++){const x=i/100;pts.push([X(x),Y(Math.max(0,Math.min(.5,threshold(x,O))))])}const line=pts.map((z,i)=>(i?'L':'M')+z[0].toFixed(2)+' '+z[1].toFixed(2)).join(' '),reverse=[...pts].reverse().map(z=>z[0].toFixed(2)+' '+z[1].toFixed(2)).join('L');boundary.setAttribute('d',line);rollup.setAttribute('d','M70 360L720 360L'+reverse+'Z');platform.setAttribute('d','M70 25L720 25L'+reverse+'Z');marker.setAttribute('cx',X(Q));marker.setAttribute('cy',Y(P));const platformValue=P*(operating+Q*learning),rollupValue=n*a+O*(operating+learning)-cost;const owns=rollupValue>platformValue;result.textContent=owns?'Full rollup is privately preferred.':'Neutral platform is privately preferred.';detail.textContent=`Platform value ${platformValue.toFixed(2)}; rollup value ${rollupValue.toFixed(2)}; difference ${(rollupValue-platformValue).toFixed(2)}.`}
[q,p,o].forEach(x=>x.addEventListener('input',render));render()})();
</script>
</main></body></html>
""",
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    if args.grid < 11:
        raise SystemExit("--grid must be at least 11")
    if args.draws <= 0:
        raise SystemExit("--draws must be positive")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    efficiencies = np.linspace(0.0, 1.0, args.grid)
    capture_shares = np.linspace(0.0, 0.5, args.grid)
    high_conflict = solve_grid(efficiencies, capture_shares, neutrality_penalty=5.0)
    low_conflict = solve_grid(efficiencies, capture_shares, neutrality_penalty=0.0)
    save_regime_map(
        args.output_dir / "value-appropriation-regime-map",
        efficiencies,
        capture_shares,
        high_conflict,
        low_conflict,
    )
    write_grid(
        args.output_dir / "value-appropriation-grid.csv",
        efficiencies,
        capture_shares,
        high_conflict,
        neutrality_penalty=5.0,
    )
    write_pareto_benchmark(args.output_dir / "pareto-capture-benchmark.csv")
    examples = write_examples(args.output_dir / "value-appropriation-examples.json")
    robustness = write_robustness(
        args.output_dir / "value-appropriation-robustness.csv",
        draws=args.draws,
        seed=args.seed,
    )
    write_explorer(args.output_dir / "value-appropriation-explorer.html")

    alpha_15 = solve_pareto_pricing(ParetoTaskPrimitives(tail_index=1.5))
    baseline = HomogeneousValueAppropriationPrimitives()
    summary = {
        "model_version": __version__,
        "result_status": (
            "Calibrated theoretical computation; synthetic sensitivity evidence, "
            "not empirical evidence."
        ),
        "proposed_result": (
            "A platform requires both learning access and value appropriation. "
            "When service prices cannot capture AI-created operating value, "
            "ownership can dominate even if learning travels perfectly; at partial "
            "boundaries, outside customer learning can feed owned operations."
        ),
        "grid_points_per_axis": args.grid,
        "robustness_draws": args.draws,
        "seed": args.seed,
        "python": platform.python_version(),
        "baseline": {
            "asset_count": baseline.asset_count,
            "owner_capture_share": baseline.owner_capture_share,
            "per_asset_operating_surplus": baseline.per_asset_operating_surplus,
            "directed_pair_learning": baseline.directed_pair_learning,
            "platform_capture_share": baseline.platform_capture_share,
            "external_learning_efficiency": baseline.external_learning_efficiency,
        },
        "pareto_alpha_1_5": {
            "provider_capture_share": alpha_15.provider_capture_share,
            "provider_profit": alpha_15.provider_profit,
            "customer_surplus": alpha_15.customer_surplus,
            "pricing_deadweight_loss": alpha_15.pricing_deadweight_loss,
        },
        "examples": examples,
        "robustness": robustness,
    }
    (args.output_dir / "value-appropriation-run-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
