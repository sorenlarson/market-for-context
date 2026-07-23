import math

import numpy as np

from context_game.model import Primitives, Regime, solve
from context_game.simulation import Heterogeneity, simulate_grid


def test_zero_leakage_supports_modular_sharing() -> None:
    outcome = solve(Primitives(leakage=0.0, integration_cost=0.1))
    assert outcome.regime is Regime.MODULAR
    assert outcome.disclosure == 1.0
    assert outcome.integration_threshold == 0.0


def test_perfect_protection_eliminates_arrow_friction() -> None:
    outcome = solve(
        Primitives(leakage=1.0, protection=1.0, integration_cost=0.1)
    )
    assert outcome.regime is Regime.MODULAR
    assert outcome.disclosure == 1.0
    assert outcome.effective_friction == 0.0


def test_intermediate_friction_produces_partial_withholding() -> None:
    outcome = solve(
        Primitives(
            marginal_value_at_full=0.4,
            curvature=0.6,
            context_rent=1.0,
            leakage=0.7,
            protection=0.0,
            integration_cost=2.0,
        )
    )
    assert outcome.regime is Regime.WITHHOLDING
    assert math.isclose(outcome.disclosure, 0.5)


def test_cheap_integration_converts_withholding_to_ownership() -> None:
    expensive = solve(
        Primitives(leakage=0.9, protection=0.0, integration_cost=2.0)
    )
    cheap = solve(
        Primitives(leakage=0.9, protection=0.0, integration_cost=0.1)
    )
    assert expensive.regime is Regime.WITHHOLDING
    assert cheap.regime is Regime.OWNERSHIP


def test_ownership_boundary_is_continuous_at_full_sharing_cutoff() -> None:
    base = Primitives(
        marginal_value_at_full=0.55,
        curvature=0.45,
        context_rent=1.0,
        protection=0.0,
        integration_cost=0.0,
    )
    below = solve(Primitives(**{**base.__dict__, "leakage": 0.55 - 1e-8}))
    above = solve(Primitives(**{**base.__dict__, "leakage": 0.55 + 1e-8}))
    assert abs(below.integration_threshold - above.integration_threshold) < 1e-6


def test_disclosure_falls_and_ownership_threshold_rises_with_leakage() -> None:
    outcomes = [
        solve(Primitives(leakage=float(leakage), protection=0.1))
        for leakage in np.linspace(0.0, 1.0, 101)
    ]
    disclosures = np.array([outcome.disclosure for outcome in outcomes])
    thresholds = np.array([outcome.integration_threshold for outcome in outcomes])
    assert np.all(np.diff(disclosures) <= 1e-12)
    assert np.all(np.diff(thresholds) >= -1e-12)


def test_protection_raises_disclosure_and_lowers_integration_threshold() -> None:
    outcomes = [
        solve(Primitives(leakage=0.9, protection=float(protection)))
        for protection in np.linspace(0.0, 1.0, 101)
    ]
    disclosures = np.array([outcome.disclosure for outcome in outcomes])
    thresholds = np.array([outcome.integration_threshold for outcome in outcomes])
    assert np.all(np.diff(disclosures) >= -1e-12)
    assert np.all(np.diff(thresholds) <= 1e-12)


def test_integration_cost_above_full_internal_value_rules_out_ownership() -> None:
    outcome = solve(
        Primitives(leakage=1.0, protection=0.0, integration_cost=0.8)
    )
    assert outcome.regime is not Regime.OWNERSHIP


def test_monte_carlo_probabilities_sum_to_one() -> None:
    result = simulate_grid(
        np.array([0.0, 0.5, 1.0]),
        np.array([0.0, 0.5, 1.0]),
        draws=1_000,
        heterogeneity=Heterogeneity(0.1, 0.1, 0.1),
    )
    total = (
        result.modular_probability
        + result.withholding_probability
        + result.ownership_probability
    )
    assert np.allclose(total, 1.0)


def test_protection_weakly_reduces_ownership_probability() -> None:
    leakages = np.array([0.8])
    costs = np.array([0.4])
    weak = simulate_grid(
        leakages, costs, protection=0.0, draws=2_000, seed=3
    )
    strong = simulate_grid(
        leakages, costs, protection=0.8, draws=2_000, seed=3
    )
    assert strong.ownership_probability[0, 0] <= weak.ownership_probability[0, 0]
