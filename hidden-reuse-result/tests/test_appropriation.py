import math
from dataclasses import replace

import numpy as np
import pytest

from hidden_reuse import (
    CaptureShareFrictions,
    HomogeneousValueAppropriationPrimitives,
    NetworkNode,
    OwnershipAccessPrimitives,
    OwnershipAccessRegime,
    ParetoTaskPrimitives,
    ValueAppropriationPrimitives,
    derive_capture_shares,
    evaluate_value_appropriation_subset,
    with_derived_capture_shares,
    homogeneous_candidate_increment,
    homogeneous_value_candidate_increment,
    homogeneous_value_network,
    platform_rollup_capture_threshold,
    solve_pareto_pricing,
    solve_value_appropriation,
)


def test_pareto_benchmark_reproduces_capture_formula() -> None:
    for alpha in (1.2, 1.5, 2.0, 4.0):
        outcome = solve_pareto_pricing(ParetoTaskPrimitives(tail_index=alpha))
        expected_share = (alpha - 1.0) / (2.0 * alpha - 1.0)
        assert math.isclose(outcome.provider_capture_share, expected_share)
        assert outcome.pricing_deadweight_loss >= 0.0


def test_matrix_game_matches_homogeneous_formula_at_every_size() -> None:
    primitives = HomogeneousValueAppropriationPrimitives()
    network = homogeneous_value_network(primitives)
    for size in range(primitives.asset_count + 1):
        candidate = evaluate_value_appropriation_subset(network, range(size))
        assert math.isclose(
            candidate.incremental_private_value,
            homogeneous_value_candidate_increment(size, primitives),
            abs_tol=1e-12,
        )


def test_old_ownership_access_model_is_nested() -> None:
    value_primitives = HomogeneousValueAppropriationPrimitives(
        platform_capture_share=1.0,
        owner_capture_share=1.0,
    )
    old_primitives = value_primitives.ownership_primitives()
    for size in range(value_primitives.asset_count + 1):
        assert math.isclose(
            homogeneous_value_candidate_increment(size, value_primitives),
            homogeneous_candidate_increment(size, old_primitives),
            abs_tol=1e-12,
        )


def test_platform_rollup_capture_threshold_is_exact() -> None:
    base = HomogeneousValueAppropriationPrimitives()
    threshold = platform_rollup_capture_threshold(base)
    assert threshold is not None
    at_threshold = replace(base, platform_capture_share=threshold)
    assert math.isclose(
        homogeneous_value_candidate_increment(base.asset_count, at_threshold),
        0.0,
        abs_tol=1e-12,
    )
    below = replace(base, platform_capture_share=threshold - 1e-4)
    above = replace(base, platform_capture_share=threshold + 1e-4)
    assert homogeneous_value_candidate_increment(base.asset_count, below) > 0
    assert homogeneous_value_candidate_increment(base.asset_count, above) < 0


def test_capture_can_support_rollup_even_when_learning_travels_perfectly() -> None:
    base = HomogeneousValueAppropriationPrimitives(
        external_learning_efficiency=1.0,
        neutrality_penalty=2.0,
    )
    low_capture = solve_value_appropriation(
        homogeneous_value_network(replace(base, platform_capture_share=0.15))
    )
    high_capture = solve_value_appropriation(
        homogeneous_value_network(replace(base, platform_capture_share=0.45))
    )
    assert low_capture.regime is OwnershipAccessRegime.FULL_ROLLUP
    assert high_capture.regime is OwnershipAccessRegime.PLATFORM
    assert low_capture.chosen.productive_learning_upgrade == 0.0


def test_platform_capture_weakly_reduces_every_ownership_candidate() -> None:
    base = HomogeneousValueAppropriationPrimitives()
    low = homogeneous_value_network(replace(base, platform_capture_share=0.10))
    high = homogeneous_value_network(replace(base, platform_capture_share=0.50))
    for size in range(1, base.asset_count + 1):
        low_value = evaluate_value_appropriation_subset(
            low, range(size)
        ).incremental_private_value
        high_value = evaluate_value_appropriation_subset(
            high, range(size)
        ).incremental_private_value
        assert high_value <= low_value + 1e-12


def test_customer_access_can_feed_selective_ownership() -> None:
    nodes = (
        NetworkNode("source_customer", "source", 0.0),
        NetworkNode("owned_target", "target", 0.0),
    )
    zero = ((0.0, 0.0), (0.0, 0.0))
    coordination = ((0.0, 0.80), (0.80, 0.0))
    learning = ((0.0, 1.0), (0.0, 0.0))
    base_network = OwnershipAccessPrimitives(
        nodes=nodes,
        learning=learning,
        customer_dependence=zero,
        coordination_cost=coordination,
        fixed_ownership_cost=0.05,
        organization_cost_scale=0.0,
    )
    low = ValueAppropriationPrimitives(
        network=replace(base_network, external_learning_efficiency=0.0),
        operating_surplus=(0.0, 0.0),
        platform_capture_share=0.20,
        owner_capture_share=0.80,
    )
    high = replace(
        low,
        network=replace(base_network, external_learning_efficiency=1.0),
    )
    low_candidate = evaluate_value_appropriation_subset(low, (1,))
    high_candidate = evaluate_value_appropriation_subset(high, (1,))
    assert low_candidate.incremental_private_value < 0
    assert high_candidate.incremental_private_value > 0
    assert high_candidate.external_access_slope > 0
    assert solve_value_appropriation(low).regime is OwnershipAccessRegime.PLATFORM
    assert solve_value_appropriation(high).owned_names == ("owned_target",)


def test_exhaustive_solution_has_no_profitable_subset_deviation() -> None:
    outcome = solve_value_appropriation(
        homogeneous_value_network(HomogeneousValueAppropriationPrimitives())
    )
    assert outcome.maximum_deviation_gain == 0.0
    assert all(
        candidate.incremental_private_value <= outcome.incremental_private_value + 1e-10
        for candidate in outcome.candidates
    )


def test_invalid_value_capture_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        solve_pareto_pricing(ParetoTaskPrimitives(tail_index=1.0))
    primitives = homogeneous_value_network(HomogeneousValueAppropriationPrimitives())
    with pytest.raises(ValueError):
        solve_value_appropriation(replace(primitives, platform_capture_share=1.1))
    with pytest.raises(ValueError):
        solve_value_appropriation(replace(primitives, operating_surplus=(1.0,)))


def test_capture_monotonicity_survives_random_heterogeneity() -> None:
    rng = np.random.default_rng(20260722)
    base = homogeneous_value_network(HomogeneousValueAppropriationPrimitives())
    for _ in range(25):
        surplus = tuple(rng.lognormal(mean=-0.03, sigma=0.25, size=6))
        low = replace(base, operating_surplus=surplus, platform_capture_share=0.1)
        high = replace(base, operating_surplus=surplus, platform_capture_share=0.5)
        assert (
            solve_value_appropriation(low).incremental_private_value
            >= solve_value_appropriation(high).incremental_private_value - 1e-12
        )


def test_derived_capture_shares_reproduce_baseline_calibration() -> None:
    shares = derive_capture_shares(CaptureShareFrictions())
    assert math.isclose(shares.platform_capture_share, 0.25)
    assert math.isclose(shares.owner_capture_share, 0.45)
    assert math.isclose(shares.capture_wedge, 0.20)


def test_symmetric_frictions_sign_the_capture_wedge_at_one_half() -> None:
    for pledgeable, expected_positive in ((0.20, True), (0.49, True), (0.51, False)):
        frictions = CaptureShareFrictions(
            service_verifiable_share=pledgeable,
            service_commitment_share=0.0,
            acquisition_verifiable_share=pledgeable,
            acquisition_commitment_share=0.0,
            seller_bargaining_weight=1.0,
            downstream_passthrough_share=0.0,
        )
        wedge = derive_capture_shares(frictions).capture_wedge
        assert (wedge > 0) == expected_positive
    boundary = CaptureShareFrictions(
        service_verifiable_share=0.5,
        service_commitment_share=0.0,
        acquisition_verifiable_share=0.5,
        acquisition_commitment_share=0.0,
        seller_bargaining_weight=1.0,
        downstream_passthrough_share=0.0,
    )
    assert math.isclose(
        derive_capture_shares(boundary).capture_wedge, 0.0, abs_tol=1e-12
    )


def test_derived_shares_move_with_market_verifiability() -> None:
    base = CaptureShareFrictions()
    better_service_metering = replace(base, service_verifiable_share=0.30)
    assert (
        derive_capture_shares(better_service_metering).platform_capture_share
        > derive_capture_shares(base).platform_capture_share
    )
    better_diligence = replace(base, acquisition_verifiable_share=0.60)
    assert (
        derive_capture_shares(better_diligence).owner_capture_share
        < derive_capture_shares(base).owner_capture_share
    )
    weaker_seller = replace(base, seller_bargaining_weight=0.5)
    assert (
        derive_capture_shares(weaker_seller).owner_capture_share
        > derive_capture_shares(base).owner_capture_share
    )


def test_with_derived_capture_shares_feeds_the_subset_solver() -> None:
    base = homogeneous_value_network(HomogeneousValueAppropriationPrimitives())
    derived = with_derived_capture_shares(base, CaptureShareFrictions())
    assert math.isclose(derived.platform_capture_share, base.platform_capture_share)
    assert math.isclose(derived.owner_capture_share, base.owner_capture_share)
    assert math.isclose(
        solve_value_appropriation(derived).incremental_private_value,
        solve_value_appropriation(base).incremental_private_value,
        abs_tol=1e-9,
    )


def test_invalid_capture_frictions_are_rejected() -> None:
    with pytest.raises(ValueError):
        derive_capture_shares(CaptureShareFrictions(service_verifiable_share=1.2))
    with pytest.raises(ValueError):
        derive_capture_shares(CaptureShareFrictions(seller_bargaining_weight=-0.1))
