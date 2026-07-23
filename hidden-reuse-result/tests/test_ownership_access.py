import math
from dataclasses import replace

import numpy as np
import pytest

from hidden_reuse import (
    HomogeneousOwnershipAccessPrimitives,
    NetworkNode,
    OwnershipAccessPrimitives,
    OwnershipAccessRegime,
    evaluate_ownership_subset,
    homogeneous_candidate_increment,
    homogeneous_network,
    hybrid_suppression_threshold,
    platform_rollup_indifference_efficiency,
    solve_ownership_access,
    vertical_customer_network,
)
from hidden_reuse.ownership_access import (
    homogeneous_internal_learning_total,
    homogeneous_optimal_ownership_size,
)


def test_matrix_game_matches_homogeneous_formula_at_every_size() -> None:
    primitives = HomogeneousOwnershipAccessPrimitives()
    network = homogeneous_network(primitives)
    for size in range(primitives.asset_count + 1):
        candidate = evaluate_ownership_subset(network, range(size))
        assert math.isclose(
            candidate.incremental_value,
            homogeneous_candidate_increment(size, primitives),
            abs_tol=1e-12,
        )


def test_platform_rollup_threshold_is_exact() -> None:
    base = HomogeneousOwnershipAccessPrimitives()
    threshold = platform_rollup_indifference_efficiency(base)
    assert threshold is not None
    at_threshold = replace(base, external_learning_efficiency=threshold)
    platform = homogeneous_candidate_increment(0, at_threshold)
    rollup = homogeneous_candidate_increment(base.asset_count, at_threshold)
    assert math.isclose(platform, rollup, abs_tol=1e-12)
    below = replace(base, external_learning_efficiency=threshold - 1e-4)
    above = replace(base, external_learning_efficiency=threshold + 1e-4)
    assert homogeneous_candidate_increment(base.asset_count, below) > 0
    assert homogeneous_candidate_increment(base.asset_count, above) < 0


def test_customer_conflict_suppresses_hybrids_and_polarizes_ownership() -> None:
    low_access = replace(
        HomogeneousOwnershipAccessPrimitives(),
        external_learning_efficiency=0.55,
    )
    high_access = replace(low_access, external_learning_efficiency=0.60)
    for primitives, endpoint_size in [(low_access, 6), (high_access, 0)]:
        no_conflict = solve_ownership_access(
            homogeneous_network(replace(primitives, neutrality_penalty=0.0))
        )
        threshold = hybrid_suppression_threshold(primitives)
        assert threshold is not None and threshold > 0
        conflict = solve_ownership_access(
            homogeneous_network(
                replace(primitives, neutrality_penalty=threshold + 1e-6)
            )
        )
        assert 0 < no_conflict.ownership_size < primitives.asset_count
        assert conflict.ownership_size == endpoint_size


def test_external_access_substitutes_for_owned_learning() -> None:
    base = vertical_customer_network(neutrality_penalty=0.0)
    low_access = solve_ownership_access(
        replace(base, external_learning_efficiency=0.20)
    )
    high_access = solve_ownership_access(
        replace(base, external_learning_efficiency=1.00)
    )
    assert low_access.ownership_size > high_access.ownership_size
    assert high_access.regime is OwnershipAccessRegime.PLATFORM
    assert high_access.chosen.learning_upgrade == 0.0


def test_directed_learning_topology_changes_which_assets_share_a_boundary() -> None:
    complementary = solve_ownership_access(
        vertical_customer_network(
            learning_topology="complementary",
            external_learning_efficiency=0.85,
            neutrality_penalty=0.10,
        )
    )
    within_type = solve_ownership_access(
        vertical_customer_network(
            learning_topology="within_type",
            external_learning_efficiency=0.85,
            neutrality_penalty=0.10,
        )
    )
    assert complementary.regime is OwnershipAccessRegime.PLATFORM
    assert complementary.owned_names == ()
    assert within_type.regime is OwnershipAccessRegime.SPECIALIZED_ROLLUP
    assert within_type.owned_names == ("clinic_east", "clinic_west")
    complementary_total = sum(
        sum(row)
        for row in vertical_customer_network(learning_topology="complementary").learning
    )
    within_total = sum(
        sum(row)
        for row in vertical_customer_network(learning_topology="within_type").learning
    )
    assert math.isclose(complementary_total, within_total)


def test_vertical_customer_links_create_endpoint_switch() -> None:
    network = vertical_customer_network(external_learning_efficiency=0.60)
    partial = solve_ownership_access(replace(network, neutrality_penalty=0.10))
    platform = solve_ownership_access(replace(network, neutrality_penalty=0.80))
    assert partial.regime is OwnershipAccessRegime.CROSS_TYPE_ROLLUP
    assert platform.regime is OwnershipAccessRegime.PLATFORM

    low_access = replace(network, external_learning_efficiency=0.50)
    partial_low = solve_ownership_access(replace(low_access, neutrality_penalty=0.10))
    full_low = solve_ownership_access(replace(low_access, neutrality_penalty=0.80))
    assert 0 < partial_low.ownership_size < len(network.nodes)
    assert full_low.regime is OwnershipAccessRegime.FULL_ROLLUP


def test_exhaustive_solution_has_no_profitable_subset_deviation() -> None:
    outcome = solve_ownership_access(vertical_customer_network())
    assert outcome.maximum_deviation_gain == 0.0
    assert all(
        candidate.incremental_value <= outcome.incremental_value + 1e-10
        for candidate in outcome.candidates
    )


def test_monotone_access_force_holds_across_heterogeneous_network_draws() -> None:
    rng = np.random.default_rng(20260721)
    base = vertical_customer_network()
    for _ in range(50):
        learning_scale = rng.lognormal(mean=-0.5 * 0.25**2, sigma=0.25, size=(6, 6))
        learning = tuple(
            tuple(
                0.0
                if source == target
                else base.learning[source][target] * learning_scale[source, target]
                for target in range(6)
            )
            for source in range(6)
        )
        perturbed = replace(base, learning=learning, neutrality_penalty=0.0)
        low = solve_ownership_access(
            replace(perturbed, external_learning_efficiency=0.20)
        )
        high = solve_ownership_access(
            replace(perturbed, external_learning_efficiency=0.90)
        )
        assert low.incremental_value >= high.incremental_value - 1e-12


def test_defaults_reproduce_published_anchor_values() -> None:
    base = HomogeneousOwnershipAccessPrimitives()
    assert base.fringe_customer_value_per_owned_asset == 0.0
    assert base.learning_saturation is None
    assert math.isclose(
        platform_rollup_indifference_efficiency(base),
        0.5656868406843443,
        abs_tol=1e-12,
    )
    assert math.isclose(
        hybrid_suppression_threshold(replace(base, external_learning_efficiency=0.55)),
        0.08001795044291382,
        abs_tol=1e-9,
    )
    assert math.isclose(
        hybrid_suppression_threshold(replace(base, external_learning_efficiency=0.60)),
        0.10388453337567773,
        abs_tol=1e-9,
    )


def test_fringe_customers_make_full_rollup_bear_conflict_cost() -> None:
    base = HomogeneousOwnershipAccessPrimitives()
    fringe = replace(base, fringe_customer_value_per_owned_asset=0.02)
    size = base.asset_count
    expected_loss = base.neutrality_penalty * 0.02 * size
    assert math.isclose(
        homogeneous_candidate_increment(size, base)
        - homogeneous_candidate_increment(size, fringe),
        expected_loss,
        abs_tol=1e-12,
    )
    full = evaluate_ownership_subset(homogeneous_network(fringe), range(size))
    assert full.neutrality_loss > 0
    assert math.isclose(full.neutrality_loss, expected_loss, abs_tol=1e-12)
    closed_free = evaluate_ownership_subset(homogeneous_network(base), range(size))
    assert closed_free.neutrality_loss == 0.0


def test_fringe_matrix_game_matches_homogeneous_formula_at_every_size() -> None:
    primitives = replace(
        HomogeneousOwnershipAccessPrimitives(),
        fringe_customer_value_per_owned_asset=0.05,
        neutrality_penalty=0.60,
    )
    network = homogeneous_network(primitives)
    for size in range(primitives.asset_count + 1):
        candidate = evaluate_ownership_subset(network, range(size))
        assert math.isclose(
            candidate.incremental_value,
            homogeneous_candidate_increment(size, primitives),
            abs_tol=1e-12,
        )


def test_fringe_generalizes_platform_rollup_threshold_exactly() -> None:
    primitives = replace(
        HomogeneousOwnershipAccessPrimitives(),
        fringe_customer_value_per_owned_asset=0.02,
        neutrality_penalty=0.80,
    )
    threshold = platform_rollup_indifference_efficiency(primitives)
    assert threshold is not None
    at_threshold = replace(primitives, external_learning_efficiency=threshold)
    assert math.isclose(
        homogeneous_candidate_increment(primitives.asset_count, at_threshold),
        0.0,
        abs_tol=1e-12,
    )


def test_fringe_hybrid_suppression_threshold_is_exact() -> None:
    primitives = replace(
        HomogeneousOwnershipAccessPrimitives(),
        fringe_customer_value_per_owned_asset=0.02,
        external_learning_efficiency=0.55,
    )
    size = primitives.asset_count
    threshold = hybrid_suppression_threshold(primitives)
    assert threshold is not None and threshold > 0

    def dominated(chi: float) -> bool:
        at = replace(primitives, neutrality_penalty=chi)
        endpoint = max(0.0, homogeneous_candidate_increment(size, at))
        return all(
            homogeneous_candidate_increment(owned, at) <= endpoint + 1e-9
            for owned in range(1, size)
        )

    assert not dominated(threshold - 1e-4)
    for chi in (threshold + 1e-4, threshold + 0.5, threshold + 5.0):
        assert dominated(chi)


def test_saturating_learning_matches_quadratic_at_two_and_is_below_after() -> None:
    base = HomogeneousOwnershipAccessPrimitives()
    saturating = replace(base, learning_saturation=4.0)
    assert homogeneous_internal_learning_total(2, saturating) == pytest.approx(
        homogeneous_internal_learning_total(2, base), abs=1e-12
    )
    for owned in (0, 1, 2):
        assert math.isclose(
            homogeneous_candidate_increment(owned, saturating),
            homogeneous_candidate_increment(owned, base),
            abs_tol=1e-12,
        )
    for owned in range(3, base.asset_count + 1):
        assert homogeneous_internal_learning_total(
            owned, saturating
        ) < homogeneous_internal_learning_total(owned, base)
        assert homogeneous_candidate_increment(
            owned, saturating
        ) < homogeneous_candidate_increment(owned, base)


def test_saturating_closed_form_matches_direct_evaluation() -> None:
    for kappa in (0.5, 2.0, 4.0, 10.0):
        primitives = replace(
            HomogeneousOwnershipAccessPrimitives(),
            learning_saturation=kappa,
            fringe_customer_value_per_owned_asset=0.03,
        )
        gamma = primitives.directed_pair_learning
        calibrated_level = gamma * (kappa + 1.0)
        assert math.isclose(
            2 * calibrated_level * 1.0 / (kappa + 1.0), 2 * gamma, abs_tol=1e-12
        )
        for owned in range(primitives.asset_count + 1):
            per_asset = (
                calibrated_level * (owned - 1) / (kappa + owned - 1)
                if owned >= 2
                else 0.0
            )
            direct_total = sum(per_asset for _ in range(owned))
            assert math.isclose(
                homogeneous_internal_learning_total(owned, primitives),
                direct_total,
                abs_tol=1e-12,
            )
            if owned == 0:
                direct_increment = 0.0
            else:
                direct_increment = (
                    owned * primitives.internalization_advantage
                    + (1.0 - primitives.external_learning_efficiency) * direct_total
                    - primitives.fixed_ownership_cost
                    - primitives.organization_cost_scale
                    * owned**primitives.organization_cost_elasticity
                    - primitives.pair_coordination_cost * owned * (owned - 1) / 2.0
                    - primitives.neutrality_penalty
                    * (
                        primitives.boundary_customer_value_per_unordered_pair
                        * owned
                        * (primitives.asset_count - owned)
                        + primitives.fringe_customer_value_per_owned_asset * owned
                    )
                )
            assert math.isclose(
                homogeneous_candidate_increment(owned, primitives),
                direct_increment,
                abs_tol=1e-12,
            )


def test_saturating_learning_cannot_be_materialized_as_a_matrix() -> None:
    primitives = replace(
        HomogeneousOwnershipAccessPrimitives(), learning_saturation=4.0
    )
    with pytest.raises(ValueError):
        homogeneous_network(primitives)
    with pytest.raises(ValueError):
        HomogeneousOwnershipAccessPrimitives(learning_saturation=0.0).validate()
    with pytest.raises(ValueError):
        replace(
            HomogeneousOwnershipAccessPrimitives(),
            fringe_customer_value_per_owned_asset=-0.1,
        ).validate()


def test_stress_features_reshape_the_polarization_anchor() -> None:
    high_conflict = HomogeneousOwnershipAccessPrimitives(neutrality_penalty=0.80)
    grid = [step / 200 for step in range(201)]

    def sizes(primitives: HomogeneousOwnershipAccessPrimitives) -> list[int]:
        return [
            homogeneous_optimal_ownership_size(
                replace(primitives, external_learning_efficiency=q)
            )
            for q in grid
        ]

    # Baseline and fringe keep the all-or-nothing switch across the q sweep.
    for case in (
        high_conflict,
        replace(high_conflict, fringe_customer_value_per_owned_asset=0.02),
    ):
        assert all(size in (0, 6) for size in sizes(case))

    # Saturating learning restores interior optima at the same conflict level.
    for case in (
        replace(high_conflict, learning_saturation=4.0),
        replace(
            high_conflict,
            learning_saturation=4.0,
            fringe_customer_value_per_owned_asset=0.02,
        ),
    ):
        assert any(0 < size < 6 for size in sizes(case))


def test_invalid_networks_are_rejected() -> None:
    node = (NetworkNode("one", "asset", 0.1),)
    zero = ((0.0,),)
    with pytest.raises(ValueError):
        solve_ownership_access(
            OwnershipAccessPrimitives(
                nodes=node,
                learning=((0.1,),),
                customer_dependence=zero,
                coordination_cost=zero,
            )
        )
    with pytest.raises(ValueError):
        vertical_customer_network(learning_topology="unknown")
