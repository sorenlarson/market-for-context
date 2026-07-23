"""Monte Carlo regime maps around the analytical context-game benchmark."""

from dataclasses import dataclass
from typing import Dict

import numpy as np


@dataclass(frozen=True)
class Heterogeneity:
    """Lognormal dispersion in initial conditions.

    All shocks have mean one. ``value_sigma`` scales current complementarity,
    ``context_sigma`` scales the exclusive context rent, and
    ``integration_sigma`` scales effective acquisition/integration difficulty.
    """

    value_sigma: float = 0.20
    context_sigma: float = 0.30
    integration_sigma: float = 0.25

    def validate(self) -> None:
        if min(self.value_sigma, self.context_sigma, self.integration_sigma) < 0:
            raise ValueError("heterogeneity sigmas cannot be negative")


@dataclass(frozen=True)
class GridResult:
    leakages: np.ndarray
    integration_costs: np.ndarray
    modular_probability: np.ndarray
    withholding_probability: np.ndarray
    ownership_probability: np.ndarray
    mean_disclosure: np.ndarray


def _mean_one_lognormal(rng: np.random.Generator, sigma: float, size: int) -> np.ndarray:
    if sigma == 0:
        return np.ones(size)
    return np.exp(sigma * rng.standard_normal(size) - 0.5 * sigma * sigma)


def simulate_grid(
    leakages: np.ndarray,
    integration_costs: np.ndarray,
    *,
    protection: float = 0.2,
    marginal_value_at_full: float = 0.55,
    curvature: float = 0.45,
    context_rent: float = 1.0,
    draws: int = 10_000,
    seed: int = 7,
    heterogeneity: Heterogeneity = Heterogeneity(),
) -> GridResult:
    """Estimate regime probabilities over a leakage/cost grid.

    Common initial-condition draws are used at every grid cell, reducing Monte
    Carlo noise in comparisons across counterfactuals.
    """

    if not 0 <= protection <= 1:
        raise ValueError("protection must lie in [0, 1]")
    if draws <= 0:
        raise ValueError("draws must be positive")
    if marginal_value_at_full <= 0 or curvature <= 0 or context_rent < 0:
        raise ValueError("value and curvature must be positive; rent nonnegative")
    heterogeneity.validate()

    leakages = np.asarray(leakages, dtype=float)
    integration_costs = np.asarray(integration_costs, dtype=float)
    if np.any((leakages < 0) | (leakages > 1)):
        raise ValueError("all leakages must lie in [0, 1]")
    if np.any(integration_costs < 0):
        raise ValueError("integration costs cannot be negative")

    rng = np.random.default_rng(seed)
    value_scale = _mean_one_lognormal(rng, heterogeneity.value_sigma, draws)
    rent_scale = _mean_one_lognormal(rng, heterogeneity.context_sigma, draws)
    integration_scale = _mean_one_lognormal(
        rng, heterogeneity.integration_sigma, draws
    )

    m = marginal_value_at_full * value_scale
    c = curvature * value_scale
    full_internal = m + 0.5 * c

    shape = (integration_costs.size, leakages.size)
    modular = np.empty(shape)
    withholding = np.empty(shape)
    ownership = np.empty(shape)
    mean_disclosure = np.empty(shape)

    for row, base_cost in enumerate(integration_costs):
        integrated = full_internal - base_cost * integration_scale
        for col, leakage in enumerate(leakages):
            friction = context_rent * rent_scale * leakage * (1.0 - protection)
            disclosure = np.clip((m + c - friction) / c, 0.0, 1.0)
            benefit = (m + c) * disclosure - 0.5 * c * disclosure * disclosure
            separate = np.maximum(0.0, benefit - friction * disclosure)
            owns = (integrated > separate + 1e-12) & (integrated > 1e-12)
            shares_fully = disclosure >= 1.0 - 1e-12

            ownership[row, col] = np.mean(owns)
            modular[row, col] = np.mean((~owns) & shares_fully)
            withholding[row, col] = np.mean((~owns) & (~shares_fully))
            mean_disclosure[row, col] = np.mean(np.where(owns, 1.0, disclosure))

    return GridResult(
        leakages=leakages,
        integration_costs=integration_costs,
        modular_probability=modular,
        withholding_probability=withholding,
        ownership_probability=ownership,
        mean_disclosure=mean_disclosure,
    )


def probability_arrays(result: GridResult) -> Dict[str, np.ndarray]:
    """Return the three regime probability surfaces by stable name."""

    return {
        "modular_sharing": result.modular_probability,
        "strategic_withholding": result.withholding_probability,
        "ownership": result.ownership_probability,
    }

