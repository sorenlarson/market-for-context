import math
import sys
from pathlib import Path

import numpy as np

CONTRACT_GAME_SOURCE = (
    Path(__file__).resolve().parents[1] / "src" / "endogenous_context_game"
)
if str(CONTRACT_GAME_SOURCE) not in sys.path:
    sys.path.insert(0, str(CONTRACT_GAME_SOURCE))

from model import (  # noqa: E402
    ContractPrimitives,
    Regime,
    arm_length_value,
    effective_joint_friction,
    gross_benefit,
    optimal_disclosure,
    optimal_protection,
    protection_cost_per_unit,
    solve_contract,
)
from simulation import (  # noqa: E402
    ContractHeterogeneity,
    simulate_contract_grid,
)


def test_interior_protection_satisfies_closed_form_first_order_condition() -> None:
    primitives = ContractPrimitives(
        context_rent=1.0,
        provider_learning_value=0.2,
        leakage=0.5,
        protectability=0.75,
        protection_cost=0.6,
    )
    expected = (1.0 - 0.2) * 0.5 * 0.75 / 0.6
    assert 0 < expected < 1
    assert math.isclose(optimal_protection(primitives), expected)


def test_closed_form_contract_matches_dense_global_search() -> None:
    cases = [
        (0.0, 0.8, 0.4, 0.25),
        (0.4, 0.0, 0.4, 0.25),
        (0.6, 0.7, 0.3, 0.10),
        (0.9, 1.0, 0.1, 0.20),
        (1.0, 0.8, 1.2, 0.25),
        (1.0, 1.0, 2.0, 0.80),
    ]
    grid = np.linspace(0.0, 1.0, 401)
    for leakage, protectability, protection_cost, learning_value in cases:
        primitives = ContractPrimitives(
            leakage=leakage,
            protectability=protectability,
            protection_cost=protection_cost,
            provider_learning_value=learning_value,
            integration_cost=2.0,
        )
        dissipation = primitives.context_rent - learning_value
        friction_by_protection = (
            dissipation * leakage * (1.0 - protectability * grid)
            + 0.5 * protection_cost * grid * grid
        )
        benefit_by_disclosure = (
            primitives.marginal_value_at_full + primitives.curvature
        ) * grid - 0.5 * primitives.curvature * grid * grid
        brute_force = np.max(
            benefit_by_disclosure[:, None]
            - grid[:, None] * friction_by_protection[None, :]
        )
        assert arm_length_value(primitives) + 1e-12 >= brute_force
        assert arm_length_value(primitives) - brute_force < 5e-5
        assert 0 <= optimal_disclosure(primitives) <= 1
        assert effective_joint_friction(primitives) >= 0


def test_cheap_protection_converts_ownership_to_modular_contracting() -> None:
    common = {
        "provider_learning_value": 0.2,
        "leakage": 0.9,
        "protectability": 1.0,
        "integration_cost": 0.5,
    }
    expensive = solve_contract(ContractPrimitives(**common, protection_cost=10.0))
    cheap = solve_contract(ContractPrimitives(**common, protection_cost=0.1))
    assert expensive.regime is Regime.OWNERSHIP
    assert cheap.regime is Regime.MODULAR
    assert cheap.agreement
    assert cheap.protection == 1.0


def test_bargaining_weight_changes_rents_but_not_contract_terms() -> None:
    common = {
        "leakage": 0.6,
        "protection_cost": 0.4,
        "integration_cost": 0.9,
    }
    weak_owner = solve_contract(
        ContractPrimitives(**common, owner_bargaining_weight=0.2)
    )
    strong_owner = solve_contract(
        ContractPrimitives(**common, owner_bargaining_weight=0.8)
    )
    assert weak_owner.agreement and strong_owner.agreement
    assert weak_owner.regime is strong_owner.regime
    assert math.isclose(weak_owner.disclosure, strong_owner.disclosure)
    assert math.isclose(weak_owner.protection, strong_owner.protection)
    assert strong_owner.owner_payoff > weak_owner.owner_payoff
    assert strong_owner.provider_payoff < weak_owner.provider_payoff


def test_transfer_exactly_reconciles_individual_and_joint_payoffs() -> None:
    primitives = ContractPrimitives(
        leakage=0.7,
        protectability=0.8,
        protection_cost=0.5,
        integration_cost=0.9,
        owner_bargaining_weight=0.6,
    )
    outcome = solve_contract(primitives)
    assert outcome.agreement
    gross = gross_benefit(
        outcome.disclosure,
        primitives.marginal_value_at_full,
        primitives.curvature,
    )
    owner_direct = (
        gross
        - primitives.context_rent * outcome.residual_leakage * outcome.disclosure
        - outcome.transfer_to_provider
    )
    provider_direct = (
        primitives.provider_learning_value
        * outcome.residual_leakage
        * outcome.disclosure
        - protection_cost_per_unit(primitives, outcome.protection) * outcome.disclosure
        + outcome.transfer_to_provider
    )
    assert math.isclose(owner_direct, outcome.owner_payoff)
    assert math.isclose(provider_direct, outcome.provider_payoff)
    assert math.isclose(owner_direct + provider_direct, outcome.separate_value)


def test_fully_internalized_learning_eliminates_incentive_to_protect() -> None:
    outcome = solve_contract(
        ContractPrimitives(
            context_rent=1.0,
            provider_learning_value=1.0,
            leakage=1.0,
            protection_cost=0.01,
            integration_cost=1.0,
        )
    )
    assert outcome.agreement
    assert outcome.regime is Regime.MODULAR
    assert outcome.protection == 0.0
    assert outcome.effective_joint_friction == 0.0


def test_provider_outside_option_can_tip_contracting_to_ownership() -> None:
    common = {
        "provider_learning_value": 0.2,
        "leakage": 0.9,
        "protectability": 1.0,
        "protection_cost": 0.1,
        "integration_cost": 0.1,
    }
    low = solve_contract(ContractPrimitives(**common, provider_outside_option=0.0))
    high = solve_contract(ContractPrimitives(**common, provider_outside_option=0.1))
    assert low.agreement
    assert high.regime is Regime.OWNERSHIP
    assert not high.agreement


def test_failed_bargaining_and_unprofitable_integration_produce_no_trade() -> None:
    outcome = solve_contract(
        ContractPrimitives(
            leakage=1.0,
            protection_cost=2.0,
            integration_cost=2.0,
            provider_outside_option=1.0,
        )
    )
    assert outcome.regime is Regime.WITHHOLDING
    assert not outcome.agreement
    assert outcome.disclosure == 0.0
    assert outcome.context_use == 0.0


def test_costlier_protection_weakly_raises_integration_threshold() -> None:
    costs = np.linspace(0.05, 2.0, 100)
    thresholds = np.array(
        [
            solve_contract(
                ContractPrimitives(
                    leakage=0.9,
                    protectability=0.9,
                    protection_cost=float(cost),
                    integration_cost=0.5,
                )
            ).integration_threshold
            for cost in costs
        ]
    )
    assert np.all(np.diff(thresholds) >= -1e-12)


def test_monte_carlo_regime_probabilities_sum_to_one() -> None:
    result = simulate_contract_grid(
        np.array([0.0, 0.5, 1.0]),
        np.array([0.0, 0.5, 1.0]),
        draws=1_000,
        heterogeneity=ContractHeterogeneity(0.1, 0.1, 0.1, 0.1),
    )
    total = (
        result.modular_probability
        + result.withholding_probability
        + result.ownership_probability
    )
    assert np.allclose(total, 1.0)
    assert np.all(result.no_trade_probability <= result.withholding_probability)


def test_protectability_weakly_reduces_ownership_probability() -> None:
    leakages = np.array([0.9])
    costs = np.array([0.4])
    weak = simulate_contract_grid(
        leakages,
        costs,
        protectability=0.1,
        draws=3_000,
        seed=12,
    )
    strong = simulate_contract_grid(
        leakages,
        costs,
        protectability=0.9,
        draws=3_000,
        seed=12,
    )
    assert strong.ownership_probability[0, 0] <= weak.ownership_probability[0, 0]


def test_bargaining_weight_does_not_change_monte_carlo_regime_probabilities() -> None:
    kwargs = {
        "leakages": np.array([0.4, 0.8]),
        "integration_costs": np.array([0.3, 0.6]),
        "draws": 2_000,
        "seed": 4,
    }
    weak = simulate_contract_grid(**kwargs, owner_bargaining_weight=0.1)
    strong = simulate_contract_grid(**kwargs, owner_bargaining_weight=0.9)
    assert np.array_equal(weak.modular_probability, strong.modular_probability)
    assert np.array_equal(weak.withholding_probability, strong.withholding_probability)
    assert np.array_equal(weak.ownership_probability, strong.ownership_probability)
    assert np.all(strong.mean_owner_payoff >= weak.mean_owner_payoff - 1e-12)
