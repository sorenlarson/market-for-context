import math
import sys
from pathlib import Path

MODEL_SOURCE = Path(__file__).resolve().parents[1] / "src"
if str(MODEL_SOURCE) not in sys.path:
    sys.path.insert(0, str(MODEL_SOURCE))

from hidden_reuse import (  # noqa: E402
    HiddenReusePrimitives,
    HiddenReuseRegime,
    PeriodTwoRoute,
    PledgeabilityPrimitives,
    PostedPricePolicy,
    PrivateSignalPrimitives,
    deterrence_threshold,
    provider_reuse_gain,
    realized_payment,
    required_monitoring_to_deter,
    solve_hidden_reuse,
    solve_period_two,
    solve_pledgeability,
    solve_private_signal_pricing,
    solve_with_pledgeability,
)


def test_reuse_shifts_period_two_payoff_toward_provider() -> None:
    primitives = HiddenReusePrimitives()
    clean = solve_period_two(0.0, primitives)
    reused = solve_period_two(1.0, primitives)
    assert clean.route is PeriodTwoRoute.RENEW
    assert reused.route is PeriodTwoRoute.RENEW
    assert reused.provider_payoff > clean.provider_payoff
    assert reused.owner_payoff < clean.owner_payoff
    assert math.isclose(clean.owner_payoff + clean.provider_payoff, clean.total_payoff)
    assert math.isclose(
        reused.owner_payoff + reused.provider_payoff, reused.total_payoff
    )


def test_required_monitoring_exactly_matches_provider_incentive() -> None:
    primitives = HiddenReusePrimitives(enforcement_capacity=0.4)
    gain = provider_reuse_gain(1.0, primitives)
    required = required_monitoring_to_deter(1.0, primitives)
    assert gain > 0
    assert 0 < required < 1
    assert math.isclose(primitives.enforcement_capacity * required, gain)


def test_weak_enforcement_and_cheap_integration_produce_ownership() -> None:
    outcome = solve_hidden_reuse(
        HiddenReusePrimitives(
            integration_cost=0.4,
            enforcement_capacity=0.2,
            context_payment_cap=0.0,
        )
    )
    assert outcome.regime is HiddenReuseRegime.OWNERSHIP
    assert not outcome.agreement


def test_enough_enforcement_restores_secure_modularity() -> None:
    outcome = solve_hidden_reuse(
        HiddenReusePrimitives(
            integration_cost=0.4,
            enforcement_capacity=0.4,
            context_payment_cap=0.0,
        )
    )
    assert outcome.regime is HiddenReuseRegime.SECURE_MODULAR
    assert outcome.agreement
    assert outcome.disclosure == 1.0
    assert outcome.reuse == 0.0
    assert 0 < outcome.monitoring < 1


def test_pricing_capacity_converts_withholding_to_compensated_reuse() -> None:
    common = {
        "integration_cost": 0.8,
        "enforcement_capacity": 0.0,
    }
    constrained = solve_hidden_reuse(
        HiddenReusePrimitives(**common, context_payment_cap=0.0)
    )
    pledgeable = solve_hidden_reuse(
        HiddenReusePrimitives(**common, context_payment_cap=0.15)
    )
    assert constrained.regime is HiddenReuseRegime.WITHHOLDING
    assert 0 < constrained.disclosure < 1
    assert pledgeable.regime is HiddenReuseRegime.PRICED_REUSE
    assert pledgeable.disclosure == 1.0
    assert pledgeable.reuse == 1.0
    assert pledgeable.transfer_to_provider < 0
    assert pledgeable.payment_cap_binding


def test_future_provider_leverage_raises_the_enforcement_requirement() -> None:
    weak_feedback = HiddenReusePrimitives(
        provider_outside_gain=0.1, enforcement_capacity=0.5
    )
    strong_feedback = HiddenReusePrimitives(
        provider_outside_gain=0.6, enforcement_capacity=0.5
    )
    assert provider_reuse_gain(1.0, strong_feedback) > provider_reuse_gain(
        1.0, weak_feedback
    )
    assert required_monitoring_to_deter(
        1.0, strong_feedback
    ) > required_monitoring_to_deter(1.0, weak_feedback)


def test_contract_respects_individual_rationality_and_payment_cap() -> None:
    primitives = HiddenReusePrimitives(
        integration_cost=0.8,
        enforcement_capacity=0.0,
        context_payment_cap=0.15,
    )
    outcome = solve_hidden_reuse(primitives)
    assert outcome.agreement
    assert outcome.owner_payoff > outcome.owner_initial_outside
    assert outcome.provider_payoff > primitives.provider_initial_outside_option
    assert outcome.transfer_to_provider >= (
        -primitives.context_payment_cap * outcome.disclosure - 1e-12
    )
    assert math.isclose(
        outcome.owner_payoff + outcome.provider_payoff, outcome.total_payoff
    )


def test_unverifiable_value_without_collateral_cannot_be_pledged() -> None:
    pricing = solve_pledgeability(
        PledgeabilityPrimitives(
            expected_net_capability_value=0.30,
            verifiable_share=0.0,
            collateral=0.0,
        )
    )
    assert pricing.maximum_pledgeable_payment == 0.0
    assert pricing.unpledgeable_expected_value == 0.30


def test_pledgeable_payment_is_the_tighter_of_participation_and_enforcement() -> None:
    constrained = solve_pledgeability(
        PledgeabilityPrimitives(
            expected_net_capability_value=0.30,
            verifiable_share=0.20,
            collateral=0.03,
        )
    )
    assert math.isclose(constrained.enforceability_ceiling, 0.09)
    assert math.isclose(constrained.maximum_pledgeable_payment, 0.09)
    assert math.isclose(constrained.pledgeable_share, 0.30)
    assert math.isclose(constrained.secured_upfront_payment, 0.03)
    assert math.isclose(constrained.royalty_share, 0.20)

    fully_pledgeable = solve_pledgeability(
        PledgeabilityPrimitives(
            expected_net_capability_value=0.30,
            verifiable_share=0.50,
            collateral=0.20,
        )
    )
    assert math.isclose(fully_pledgeable.maximum_pledgeable_payment, 0.30)
    assert math.isclose(fully_pledgeable.pledgeable_share, 1.0)
    assert math.isclose(fully_pledgeable.secured_upfront_payment, 0.15)


def test_uncertainty_changes_realizations_not_the_risk_neutral_expected_ceiling() -> (
    None
):
    certain = solve_pledgeability(
        PledgeabilityPrimitives(
            expected_net_capability_value=0.30,
            verifiable_share=0.20,
            collateral=0.03,
            value_log_sigma=0.0,
        )
    )
    uncertain = solve_pledgeability(
        PledgeabilityPrimitives(
            expected_net_capability_value=0.30,
            verifiable_share=0.20,
            collateral=0.03,
            value_log_sigma=1.0,
        )
    )
    assert math.isclose(
        certain.maximum_pledgeable_payment,
        uncertain.maximum_pledgeable_payment,
    )
    assert certain.p90_realized_value == 0.30
    assert uncertain.p90_realized_value > 0.30


def test_competition_cannot_exceed_the_pledgeability_ceiling() -> None:
    pricing = solve_pledgeability(
        PledgeabilityPrimitives(
            expected_net_capability_value=0.30,
            verifiable_share=0.10,
            collateral=0.02,
            bilateral_owner_capture=0.40,
        )
    )
    assert math.isclose(pricing.maximum_pledgeable_payment, 0.05)
    assert math.isclose(pricing.bilateral_benchmark_payment, 0.02)
    assert pricing.competitive_benchmark_payment == pricing.maximum_pledgeable_payment


def test_unpledgeable_value_grows_when_capability_outpaces_verifiability() -> None:
    common = {
        "verifiable_share": 0.10,
        "collateral": 0.02,
    }
    low = solve_pledgeability(
        PledgeabilityPrimitives(
            expected_net_capability_value=0.20,
            **common,
        )
    )
    high = solve_pledgeability(
        PledgeabilityPrimitives(
            expected_net_capability_value=0.40,
            **common,
        )
    )
    assert math.isclose(
        high.maximum_pledgeable_payment - low.maximum_pledgeable_payment,
        0.10 * (0.40 - 0.20),
    )
    assert high.unpledgeable_expected_value > low.unpledgeable_expected_value


def test_realized_payment_only_tracks_the_contractible_part_of_true_value() -> None:
    pricing = solve_pledgeability(
        PledgeabilityPrimitives(
            expected_net_capability_value=0.30,
            verifiable_share=0.10,
            collateral=0.02,
        )
    )
    assert math.isclose(realized_payment(1.00, pricing), 0.12)
    assert realized_payment(1.00, pricing) < 1.00


def test_endogenous_pledgeability_moves_governance_from_withholding_to_priced_reuse() -> (
    None
):
    hidden = HiddenReusePrimitives(
        enforcement_capacity=0.20,
        integration_cost=0.80,
    )
    unpledgeable = solve_with_pledgeability(
        hidden,
        PledgeabilityPrimitives(verifiable_share=0.0, collateral=0.0),
    )
    pledgeable = solve_with_pledgeability(
        hidden,
        PledgeabilityPrimitives(verifiable_share=0.60, collateral=0.0),
    )
    assert unpledgeable.governance.regime is HiddenReuseRegime.WITHHOLDING
    assert pledgeable.governance.regime is HiddenReuseRegime.PRICED_REUSE
    assert math.isclose(
        pledgeable.pricing.expected_net_capability_value,
        provider_reuse_gain(1.0, hidden),
    )


def test_private_signal_pooling_price_serves_both_types_when_high_type_is_rare() -> (
    None
):
    result = solve_private_signal_pricing(
        PrivateSignalPrimitives(
            low_expected_value=0.20,
            high_expected_value=0.40,
            high_type_probability=0.20,
            verifiable_share=1.0,
            collateral=0.0,
        )
    )
    assert result.policy is PostedPricePolicy.POOL
    assert result.low_type_accepts
    assert result.high_type_accepts
    assert math.isclose(result.offered_price, 0.20)


def test_private_signal_screening_excludes_low_type_when_high_type_is_likely() -> None:
    result = solve_private_signal_pricing(
        PrivateSignalPrimitives(
            low_expected_value=0.20,
            high_expected_value=0.40,
            high_type_probability=0.80,
            verifiable_share=1.0,
            collateral=0.0,
        )
    )
    assert result.policy is PostedPricePolicy.SCREEN_HIGH
    assert not result.low_type_accepts
    assert result.high_type_accepts
    assert math.isclose(result.trade_probability, 0.80)


def test_private_high_type_keeps_unverifiable_rent_even_when_screened() -> None:
    result = solve_private_signal_pricing(
        PrivateSignalPrimitives(
            low_expected_value=0.15,
            high_expected_value=0.45,
            high_type_probability=0.90,
            verifiable_share=0.10,
            collateral=0.02,
        )
    )
    assert result.policy is PostedPricePolicy.SCREEN_HIGH
    assert math.isclose(result.screening_price, 0.065)
    assert math.isclose(result.high_type_rent_if_served, 0.385)


def test_private_signal_pricing_can_select_no_trade() -> None:
    result = solve_private_signal_pricing(
        PrivateSignalPrimitives(
            low_expected_value=0.15,
            high_expected_value=0.45,
            high_type_probability=0.30,
            verifiable_share=0.10,
            collateral=0.02,
            owner_access_cost=0.10,
        )
    )
    assert result.policy is PostedPricePolicy.NO_TRADE
    assert result.trade_probability == 0.0


def test_reuse_can_make_the_owner_leave_the_incumbent() -> None:
    primitives = HiddenReusePrimitives(provider_outside_gain=1.2)
    reused = solve_period_two(1.0, primitives)
    assert reused.route is not PeriodTwoRoute.RENEW
    assert reused.provider_payoff == primitives.provider_outside_base + 1.2


def test_no_private_learning_requires_no_monitoring() -> None:
    outcome = solve_hidden_reuse(
        HiddenReusePrimitives(
            incumbent_capability_gain=0.0,
            provider_outside_gain=0.0,
            reuse_cost=0.1,
            enforcement_capacity=0.0,
            integration_cost=0.8,
        )
    )
    assert outcome.regime is HiddenReuseRegime.SECURE_MODULAR
    assert outcome.monitoring == 0.0
    assert outcome.reuse == 0.0


def test_deterrence_threshold_is_the_full_monitoring_boundary() -> None:
    primitives = HiddenReusePrimitives(integration_cost=0.8)
    threshold = deterrence_threshold(1.0, primitives)
    gain = provider_reuse_gain(1.0, primitives)
    assert math.isclose(threshold, gain)

    just_below = HiddenReusePrimitives(
        integration_cost=0.8,
        enforcement_capacity=threshold - 1e-6,
    )
    just_above = HiddenReusePrimitives(
        integration_cost=0.8,
        enforcement_capacity=threshold + 1e-6,
    )
    assert required_monitoring_to_deter(1.0, just_below) > 1.0
    assert required_monitoring_to_deter(1.0, just_above) < 1.0


def test_disclosure_grid_solution_is_stable() -> None:
    primitives = HiddenReusePrimitives(
        integration_cost=0.8,
        enforcement_capacity=0.0,
        context_payment_cap=0.0,
    )
    coarse = solve_hidden_reuse(primitives, disclosure_grid_size=101)
    fine = solve_hidden_reuse(primitives, disclosure_grid_size=401)
    assert coarse.regime is fine.regime
    assert abs(coarse.disclosure - fine.disclosure) < 0.02
    assert abs(coarse.total_payoff - fine.total_payoff) < 0.02


def test_complete_withholding_is_distinct_from_ownership() -> None:
    outcome = solve_hidden_reuse(
        HiddenReusePrimitives(
            integration_cost=10.0,
            provider_initial_outside_option=10.0,
        )
    )
    assert outcome.regime is HiddenReuseRegime.WITHHOLDING
    assert not outcome.agreement
    assert outcome.disclosure == 0.0
    assert outcome.waiting_value > outcome.integration_value
