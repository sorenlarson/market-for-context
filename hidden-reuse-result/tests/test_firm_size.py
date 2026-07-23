import math
from dataclasses import replace

import numpy as np
import pytest

from hidden_reuse import (
    FirmSizePrimitives,
    FirmSizeRegime,
    HiddenReusePrimitives,
    HiddenReuseRegime,
    PledgeabilityPrimitives,
    continuous_target_size,
    derive_owner_internalization_advantage,
    learning_fraction,
    per_node_surplus,
    per_node_surplus_derivative,
    scale_component_per_node,
    solve_firm_size,
)


def test_one_node_has_no_cross_node_learning() -> None:
    primitives = FirmSizePrimitives()
    assert learning_fraction(1, primitives) == 0.0
    assert math.isclose(
        per_node_surplus(1, primitives),
        primitives.internalization_advantage
        - primitives.shared_fixed_cost
        - primitives.organization_cost_scale,
    )


def test_baseline_selects_a_finite_four_node_rollup() -> None:
    outcome = solve_firm_size(FirmSizePrimitives())
    assert outcome.regime is FirmSizeRegime.ROLLUP
    assert outcome.equilibrium_firm_size == 4
    assert outcome.conditional_target_size == 4
    assert math.isclose(outcome.integration_threshold, 0.5732202253184497)
    assert outcome.per_node_surplus_at_target > 0


def test_internalization_advantage_changes_entry_but_not_conditional_size() -> None:
    base = FirmSizePrimitives()
    low = solve_firm_size(replace(base, internalization_advantage=0.40))
    high = solve_firm_size(replace(base, internalization_advantage=0.80))
    assert low.regime is FirmSizeRegime.MODULAR
    assert high.regime is FirmSizeRegime.ROLLUP
    assert low.conditional_target_size == high.conditional_target_size == 4
    assert math.isclose(low.integration_threshold, high.integration_threshold)
    shifts = [
        high_point.per_node_surplus - low_point.per_node_surplus
        for low_point, high_point in zip(low.profile, high.profile)
    ]
    assert np.allclose(shifts, 0.40)


def test_integration_threshold_is_strict_entry_boundary() -> None:
    base = FirmSizePrimitives(internalization_advantage=0.0)
    threshold = solve_firm_size(base).integration_threshold
    tie = solve_firm_size(replace(base, internalization_advantage=threshold))
    above = solve_firm_size(replace(base, internalization_advantage=threshold + 1e-6))
    assert not tie.integrates
    assert tie.regime is FirmSizeRegime.MODULAR
    assert above.integrates


def test_target_maximizes_per_node_surplus_and_blocks_other_coalitions() -> None:
    outcome = solve_firm_size(FirmSizePrimitives())
    target_payoff = outcome.per_node_surplus_at_target
    assert all(
        point.per_node_surplus <= target_payoff + 1e-12 for point in outcome.profile
    )


def test_continuous_target_satisfies_first_order_condition() -> None:
    primitives = FirmSizePrimitives()
    outcome = solve_firm_size(primitives)
    assert 1 < outcome.continuous_target_size < primitives.max_firm_size
    assert (
        abs(per_node_surplus_derivative(outcome.continuous_target_size, primitives))
        < 1e-10
    )
    assert abs(outcome.conditional_target_size - outcome.continuous_target_size) < 1


def test_fixed_cost_and_learning_raise_target_while_organization_cost_lowers_it() -> (
    None
):
    base = FirmSizePrimitives()
    low_fixed = solve_firm_size(replace(base, shared_fixed_cost=0.50))
    high_fixed = solve_firm_size(replace(base, shared_fixed_cost=2.50))
    low_learning = solve_firm_size(replace(base, cross_node_learning=0.00))
    high_learning = solve_firm_size(replace(base, cross_node_learning=1.00))
    low_cost = solve_firm_size(replace(base, organization_cost_scale=0.015))
    high_cost = solve_firm_size(replace(base, organization_cost_scale=0.10))
    assert high_fixed.conditional_target_size >= low_fixed.conditional_target_size
    assert high_learning.conditional_target_size >= low_learning.conditional_target_size
    assert high_cost.conditional_target_size <= low_cost.conditional_target_size


def test_zero_scale_economies_can_support_standalone_integration() -> None:
    outcome = solve_firm_size(
        FirmSizePrimitives(
            internalization_advantage=0.20,
            shared_fixed_cost=0.00,
            cross_node_learning=0.00,
            organization_cost_scale=0.05,
            organization_cost_elasticity=1.0,
        )
    )
    assert outcome.regime is FirmSizeRegime.STANDALONE
    assert outcome.equilibrium_firm_size == 1


def test_unbounded_scale_at_the_computational_cap_is_reported() -> None:
    outcome = solve_firm_size(
        FirmSizePrimitives(
            internalization_advantage=0.20,
            shared_fixed_cost=0.40,
            cross_node_learning=0.40,
            organization_cost_scale=0.00,
            max_firm_size=20,
        )
    )
    assert outcome.regime is FirmSizeRegime.INDUSTRY_WIDE
    assert outcome.equilibrium_firm_size == 20
    assert outcome.industry_boundary_binding


def test_degenerate_ties_are_exposed_and_resolved_toward_smaller_size() -> None:
    outcome = solve_firm_size(
        FirmSizePrimitives(
            internalization_advantage=0.10,
            shared_fixed_cost=0.00,
            cross_node_learning=0.00,
            organization_cost_scale=0.00,
            max_firm_size=5,
        )
    )
    assert outcome.co_maximizing_sizes == (1, 2, 3, 4, 5)
    assert outcome.conditional_target_size == 1
    assert outcome.regime is FirmSizeRegime.STANDALONE


def test_hidden_reuse_bridge_makes_weak_enforcement_more_integration_prone() -> None:
    weak = derive_owner_internalization_advantage(
        HiddenReusePrimitives(enforcement_capacity=0.20)
    )
    strong = derive_owner_internalization_advantage(
        HiddenReusePrimitives(enforcement_capacity=0.80)
    )
    assert weak.modular_regime is HiddenReuseRegime.WITHHOLDING
    assert strong.modular_regime is HiddenReuseRegime.SECURE_MODULAR
    assert weak.internalization_advantage > strong.internalization_advantage


def test_pledgeable_reuse_value_reduces_the_private_internalization_advantage() -> None:
    hidden = HiddenReusePrimitives(enforcement_capacity=0.20)
    unpriced = derive_owner_internalization_advantage(
        hidden,
        PledgeabilityPrimitives(verifiable_share=0.00, collateral=0.00),
    )
    priced = derive_owner_internalization_advantage(
        hidden,
        PledgeabilityPrimitives(verifiable_share=0.60, collateral=0.00),
    )
    assert priced.applied_context_payment_cap > 0
    assert priced.modular_regime is HiddenReuseRegime.PRICED_REUSE
    assert priced.internalization_advantage < unpriced.internalization_advantage


def test_default_dilution_is_zero_and_reproduces_the_documented_anchor() -> None:
    default = FirmSizePrimitives()
    assert default.advantage_dilution_elasticity == 0.0
    baseline = solve_firm_size(default)
    explicit = solve_firm_size(replace(default, advantage_dilution_elasticity=0.0))
    assert explicit.regime is FirmSizeRegime.ROLLUP
    assert explicit.conditional_target_size == baseline.conditional_target_size == 4
    assert explicit.equilibrium_firm_size == baseline.equilibrium_firm_size == 4
    assert explicit.co_maximizing_sizes == baseline.co_maximizing_sizes
    assert explicit.integration_threshold == baseline.integration_threshold
    assert math.isclose(explicit.integration_threshold, 0.5732202253184497)
    assert explicit.continuous_target_size == baseline.continuous_target_size
    assert math.isclose(explicit.continuous_target_size, 4.007, abs_tol=5e-4)
    assert explicit.per_node_surplus_at_target == baseline.per_node_surplus_at_target
    assert explicit.profile == baseline.profile


def test_positive_dilution_makes_conditional_size_depend_on_the_advantage() -> None:
    base = FirmSizePrimitives(advantage_dilution_elasticity=0.5)
    moderate = solve_firm_size(replace(base, internalization_advantage=1.20))
    strong = solve_firm_size(replace(base, internalization_advantage=2.00))
    assert moderate.integrates and strong.integrates
    assert moderate.conditional_target_size == 3
    assert strong.conditional_target_size == 2
    assert moderate.conditional_target_size != strong.conditional_target_size
    # The same two advantage values leave the additive target at four.
    assert (
        solve_firm_size(
            FirmSizePrimitives(internalization_advantage=1.20)
        ).conditional_target_size
        == solve_firm_size(
            FirmSizePrimitives(internalization_advantage=2.00)
        ).conditional_target_size
        == 4
    )
    # Per-node surplus applies the diluted advantage A * n ** (-zeta).
    primitives = replace(base, internalization_advantage=1.20)
    for size in (1, 2, 3, 4):
        assert math.isclose(
            per_node_surplus(size, primitives),
            1.20 * size**-0.5 + scale_component_per_node(size, primitives),
        )


def test_continuous_benchmark_is_restricted_to_zero_dilution() -> None:
    diluted = FirmSizePrimitives(advantage_dilution_elasticity=0.5)
    with pytest.raises(ValueError):
        continuous_target_size(diluted)
    outcome = solve_firm_size(diluted)
    assert math.isnan(outcome.continuous_target_size)


def test_invalid_firm_size_primitives_are_rejected() -> None:
    with pytest.raises(ValueError):
        solve_firm_size(FirmSizePrimitives(learning_saturation=0.0))
    with pytest.raises(ValueError):
        solve_firm_size(FirmSizePrimitives(organization_cost_elasticity=0.9))
    with pytest.raises(ValueError):
        solve_firm_size(FirmSizePrimitives(max_firm_size=0))
    with pytest.raises(ValueError):
        solve_firm_size(FirmSizePrimitives(advantage_dilution_elasticity=-0.1))


def test_separation_and_integer_optimum_hold_across_parameter_draws() -> None:
    rng = np.random.default_rng(20260721)
    for _ in range(100):
        primitives = FirmSizePrimitives(
            internalization_advantage=float(rng.uniform(-0.20, 1.20)),
            shared_fixed_cost=float(rng.uniform(0.0, 3.0)),
            cross_node_learning=float(rng.uniform(0.0, 1.2)),
            learning_saturation=float(rng.uniform(0.5, 10.0)),
            organization_cost_scale=float(rng.uniform(0.002, 0.15)),
            organization_cost_elasticity=float(rng.uniform(1.0, 2.0)),
            max_firm_size=30,
        )
        outcome = solve_firm_size(primitives)
        shifted = solve_firm_size(
            replace(
                primitives,
                internalization_advantage=(primitives.internalization_advantage + 0.37),
            )
        )
        assert outcome.conditional_target_size == shifted.conditional_target_size
        assert math.isclose(
            outcome.integration_threshold, shifted.integration_threshold
        )
        assert outcome.conditional_target_size in outcome.co_maximizing_sizes
        assert (
            abs(outcome.conditional_target_size - outcome.continuous_target_size) <= 1
        )
        assert outcome.integrates == (
            primitives.internalization_advantage > outcome.integration_threshold + 1e-10
        )


def test_monotone_size_forces_hold_across_parameter_draws() -> None:
    rng = np.random.default_rng(1937)
    for _ in range(60):
        base = FirmSizePrimitives(
            shared_fixed_cost=float(rng.uniform(0.1, 2.0)),
            cross_node_learning=float(rng.uniform(0.0, 0.8)),
            learning_saturation=float(rng.uniform(1.0, 8.0)),
            organization_cost_scale=float(rng.uniform(0.01, 0.10)),
            organization_cost_elasticity=float(rng.uniform(1.0, 1.8)),
            max_firm_size=30,
        )
        target = solve_firm_size(base).conditional_target_size
        assert (
            solve_firm_size(
                replace(base, shared_fixed_cost=base.shared_fixed_cost + 0.30)
            ).conditional_target_size
            >= target
        )
        assert (
            solve_firm_size(
                replace(
                    base,
                    cross_node_learning=base.cross_node_learning + 0.20,
                )
            ).conditional_target_size
            >= target
        )
        assert (
            solve_firm_size(
                replace(
                    base,
                    organization_cost_scale=base.organization_cost_scale + 0.02,
                )
            ).conditional_target_size
            <= target
        )
