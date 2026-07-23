import math
import sys
from pathlib import Path

MODEL_SOURCE = Path(__file__).resolve().parents[1] / "src" / "endogenous_context_game"
if str(MODEL_SOURCE) not in sys.path:
    sys.path.insert(0, str(MODEL_SOURCE))

from hidden_reuse import (  # noqa: E402
    HiddenReusePrimitives,
    HiddenReuseRegime,
    PeriodTwoRoute,
    provider_reuse_gain,
    required_monitoring_to_deter,
    solve_hidden_reuse,
    solve_period_two,
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
    assert pledgeable.regime is HiddenReuseRegime.LEAKY_MODULAR
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
