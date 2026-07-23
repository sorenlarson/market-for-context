"""Price uncertain future capability when only part of its value is pledgeable.

The hidden-reuse model permits the provider to pay for learning rights, but its
baseline payment cap is reduced form.  This module makes that cap endogenous.

Let ``V`` be the provider's future *net* value from the capability created by
reuse.  Its realization is unknown when the context contract is signed and is
privately observed by the provider later.  The contract can claim:

* a secured upfront payment ``b`` no larger than collateral ``W``; and
* a royalty ``rho * V`` with ``rho`` no larger than the verifiable share
  ``phi``.

With risk-neutral parties and a shared prior with mean ``mu``, the provider's
participation constraint limits expected payment to ``mu``.  Enforceability
limits it to ``W + phi * mu``.  The maximum pledgeable payment is therefore

    P* = min(mu, W + phi * mu).

The distinction is deliberate: competition can push the price toward ``P*``,
but it cannot make a privately realized, unverifiable remainder collectible.

When this module is coupled to the hidden-reuse solver, the expected value of
the secured-plus-royalty claim is treated as committed in period one. A royalty
that the provider can avoid by declining to reuse would also reduce the hidden
reuse incentive; jointly solving that incentive effect is a stated extension.
"""

from dataclasses import dataclass, replace
from enum import Enum
from math import exp
from statistics import NormalDist
from typing import Optional

from .model import (
    HiddenReuseOutcome,
    HiddenReusePrimitives,
    provider_reuse_gain,
    solve_hidden_reuse,
)


@dataclass(frozen=True)
class PledgeabilityPrimitives:
    """Primitives governing how future capability can be promised as payment.

    ``expected_net_capability_value`` is the common-prior mean of the
    provider's net learning value at full disclosure.  When it is ``None``,
    :func:`solve_with_pledgeability` uses the hidden-reuse model's endogenous
    full-disclosure reuse gain.

    ``verifiable_share`` is the largest royalty share that can be computed from
    evidence a contract can verify. ``collateral`` is value that can be paid or
    posted before the uncertain capability is realized.

    ``bilateral_owner_capture`` does not expand pledgeability.  It only reports
    a bilateral bargaining benchmark alongside the competitive ceiling.
    """

    expected_net_capability_value: Optional[float] = None
    verifiable_share: float = 0.00
    collateral: float = 0.00
    value_log_sigma: float = 0.80
    bilateral_owner_capture: float = 0.50

    def validate(self) -> None:
        if (
            self.expected_net_capability_value is not None
            and self.expected_net_capability_value < 0
        ):
            raise ValueError("expected_net_capability_value cannot be negative")
        if not 0 <= self.verifiable_share <= 1:
            raise ValueError("verifiable_share must lie in [0, 1]")
        if self.collateral < 0:
            raise ValueError("collateral cannot be negative")
        if self.value_log_sigma < 0:
            raise ValueError("value_log_sigma cannot be negative")
        if not 0 <= self.bilateral_owner_capture <= 1:
            raise ValueError("bilateral_owner_capture must lie in [0, 1]")


@dataclass(frozen=True)
class PledgeabilityOutcome:
    """Maximum enforceable claim on uncertain future capability value."""

    expected_net_capability_value: float
    participation_ceiling: float
    enforceability_ceiling: float
    maximum_pledgeable_payment: float
    pledgeable_share: float
    unpledgeable_expected_value: float
    secured_upfront_payment: float
    royalty_share: float
    bilateral_benchmark_payment: float
    competitive_benchmark_payment: float
    median_realized_value: float
    p90_realized_value: float
    p99_realized_value: float


@dataclass(frozen=True)
class PledgeableHiddenReuseOutcome:
    """Hidden-reuse governance after replacing the exogenous payment cap."""

    pricing: PledgeabilityOutcome
    governance: HiddenReuseOutcome
    applied_context_payment_cap: float


class PostedPricePolicy(str, Enum):
    """Pricing policies when the provider privately observes a value signal."""

    POOL = "pool_both_types"
    SCREEN_HIGH = "screen_high_type"
    NO_TRADE = "no_trade"


@dataclass(frozen=True)
class PrivateSignalPrimitives:
    """Two-type adverse-selection benchmark for capability pricing.

    Before the context contract, the provider privately observes whether its
    expected net capability value is low or high. The owner can post only one
    fixed access fee, and each type can finance that fee only up to its
    pledgeability ceiling. Both types face the same verifiability and collateral
    constraints.
    """

    low_expected_value: float = 0.15
    high_expected_value: float = 0.45
    high_type_probability: float = 0.30
    verifiable_share: float = 0.10
    collateral: float = 0.02
    owner_access_cost: float = 0.00
    value_log_sigma: float = 0.80

    def validate(self) -> None:
        if self.low_expected_value < 0:
            raise ValueError("low_expected_value cannot be negative")
        if self.high_expected_value < self.low_expected_value:
            raise ValueError("high_expected_value must be at least low_expected_value")
        if not 0 <= self.high_type_probability <= 1:
            raise ValueError("high_type_probability must lie in [0, 1]")
        if not 0 <= self.verifiable_share <= 1:
            raise ValueError("verifiable_share must lie in [0, 1]")
        if self.collateral < 0:
            raise ValueError("collateral cannot be negative")
        if self.owner_access_cost < 0:
            raise ValueError("owner_access_cost cannot be negative")
        if self.value_log_sigma < 0:
            raise ValueError("value_log_sigma cannot be negative")


@dataclass(frozen=True)
class PrivateSignalOutcome:
    """Optimal single posted price under a private high/low value signal."""

    policy: PostedPricePolicy
    low_type_pricing: PledgeabilityOutcome
    high_type_pricing: PledgeabilityOutcome
    pooling_price: float
    screening_price: float
    pooling_expected_profit: float
    screening_expected_profit: float
    offered_price: float
    trade_probability: float
    expected_owner_payment: float
    expected_owner_profit: float
    expected_provider_surplus: float
    low_type_accepts: bool
    high_type_accepts: bool
    high_type_rent_if_served: float


def _lognormal_quantile(mean: float, log_sigma: float, probability: float) -> float:
    """Quantile of a lognormal distribution parameterized by its mean."""

    if mean <= 0:
        return 0.0
    if log_sigma == 0:
        return mean
    z = NormalDist().inv_cdf(probability)
    return mean * exp(log_sigma * z - 0.5 * log_sigma * log_sigma)


def solve_pledgeability(
    primitives: PledgeabilityPrimitives,
    *,
    fallback_expected_value: Optional[float] = None,
) -> PledgeabilityOutcome:
    """Solve the maximum pledgeable-payment problem.

    The provider is risk neutral and both parties share the same prior.  Value
    uncertainty changes ex-post outcomes but, conditional on the mean, does not
    change the ex-ante ceiling.  This cleanly separates uncertainty from
    unverifiability.
    """

    primitives.validate()
    expected_value = primitives.expected_net_capability_value
    if expected_value is None:
        expected_value = fallback_expected_value
    if expected_value is None:
        raise ValueError(
            "expected_net_capability_value or fallback_expected_value is required"
        )
    if expected_value < 0:
        raise ValueError("fallback_expected_value cannot be negative")

    mu = float(expected_value)
    phi = primitives.verifiable_share
    participation_ceiling = mu
    enforceability_ceiling = primitives.collateral + phi * mu
    maximum_payment = min(participation_ceiling, enforceability_ceiling)

    # Maximize the verifiable state-contingent claim first, then use secured
    # value to cover the remaining expected payment.  These terms implement P*.
    royalty_share = phi if mu > 0 else 0.0
    secured_upfront = min(primitives.collateral, max(0.0, mu - phi * mu))
    pledgeable_share = maximum_payment / mu if mu > 0 else 0.0

    return PledgeabilityOutcome(
        expected_net_capability_value=mu,
        participation_ceiling=participation_ceiling,
        enforceability_ceiling=enforceability_ceiling,
        maximum_pledgeable_payment=maximum_payment,
        pledgeable_share=pledgeable_share,
        unpledgeable_expected_value=max(0.0, mu - maximum_payment),
        secured_upfront_payment=secured_upfront,
        royalty_share=royalty_share,
        bilateral_benchmark_payment=(
            primitives.bilateral_owner_capture * maximum_payment
        ),
        competitive_benchmark_payment=maximum_payment,
        median_realized_value=_lognormal_quantile(mu, primitives.value_log_sigma, 0.50),
        p90_realized_value=_lognormal_quantile(mu, primitives.value_log_sigma, 0.90),
        p99_realized_value=_lognormal_quantile(mu, primitives.value_log_sigma, 0.99),
    )


def realized_payment(
    realized_capability_value: float, outcome: PledgeabilityOutcome
) -> float:
    """Payment under the maximum-pledgeability secured-plus-royalty contract."""

    if realized_capability_value < 0:
        raise ValueError("realized_capability_value cannot be negative")
    return (
        outcome.secured_upfront_payment
        + outcome.royalty_share * realized_capability_value
    )


def solve_private_signal_pricing(
    primitives: PrivateSignalPrimitives,
    *,
    tolerance: float = 1e-12,
) -> PrivateSignalOutcome:
    """Solve a two-type posted-price problem under adverse selection.

    A pooling price equal to the low type's pledgeability ceiling is accepted by
    both types. A screening price equal to the high type's ceiling is accepted
    only by the high type. The owner compares expected profit from those offers
    with no trade.
    """

    primitives.validate()
    common = {
        "verifiable_share": primitives.verifiable_share,
        "collateral": primitives.collateral,
        "value_log_sigma": primitives.value_log_sigma,
    }
    low = solve_pledgeability(
        PledgeabilityPrimitives(
            expected_net_capability_value=primitives.low_expected_value,
            **common,
        )
    )
    high = solve_pledgeability(
        PledgeabilityPrimitives(
            expected_net_capability_value=primitives.high_expected_value,
            **common,
        )
    )
    probability_high = primitives.high_type_probability
    pooling_price = low.maximum_pledgeable_payment
    screening_price = high.maximum_pledgeable_payment
    pooling_profit = pooling_price - primitives.owner_access_cost
    screening_profit = probability_high * (
        screening_price - primitives.owner_access_cost
    )

    if max(pooling_profit, screening_profit) <= tolerance:
        policy = PostedPricePolicy.NO_TRADE
        offered_price = 0.0
        trade_probability = 0.0
        expected_payment = 0.0
        expected_profit = 0.0
        expected_provider_surplus = 0.0
        low_accepts = False
        high_accepts = False
        high_rent = 0.0
    elif screening_profit > pooling_profit + tolerance:
        policy = PostedPricePolicy.SCREEN_HIGH
        offered_price = screening_price
        trade_probability = probability_high
        expected_payment = probability_high * offered_price
        expected_profit = screening_profit
        expected_provider_surplus = probability_high * (
            primitives.high_expected_value - offered_price
        )
        low_accepts = False
        high_accepts = True
        high_rent = primitives.high_expected_value - offered_price
    else:
        policy = PostedPricePolicy.POOL
        offered_price = pooling_price
        trade_probability = 1.0
        expected_payment = offered_price
        expected_profit = pooling_profit
        expected_provider_surplus = (1.0 - probability_high) * (
            primitives.low_expected_value - offered_price
        ) + probability_high * (primitives.high_expected_value - offered_price)
        low_accepts = True
        high_accepts = True
        high_rent = primitives.high_expected_value - offered_price

    return PrivateSignalOutcome(
        policy=policy,
        low_type_pricing=low,
        high_type_pricing=high,
        pooling_price=pooling_price,
        screening_price=screening_price,
        pooling_expected_profit=pooling_profit,
        screening_expected_profit=screening_profit,
        offered_price=offered_price,
        trade_probability=trade_probability,
        expected_owner_payment=expected_payment,
        expected_owner_profit=expected_profit,
        expected_provider_surplus=expected_provider_surplus,
        low_type_accepts=low_accepts,
        high_type_accepts=high_accepts,
        high_type_rent_if_served=high_rent,
    )


def solve_with_pledgeability(
    hidden_primitives: HiddenReusePrimitives,
    pricing_primitives: PledgeabilityPrimitives,
    *,
    disclosure_grid_size: int = 201,
    tolerance: float = 1e-10,
) -> PledgeableHiddenReuseOutcome:
    """Solve governance with the payment cap derived from pledgeability.

    When no separate expected capability value is supplied, the pricing mean is
    the provider's full-disclosure private reuse gain in the hidden-reuse game.
    The resulting maximum pledgeable payment is normalized per unit of full
    disclosure and replaces ``context_payment_cap``. The wrapper treats the
    resulting expected claim as a period-one payment capacity; it does not
    separately subtract an avoidable royalty from the later reuse incentive.
    """

    hidden_primitives.validate()
    fallback = max(0.0, provider_reuse_gain(1.0, hidden_primitives))
    pricing = solve_pledgeability(pricing_primitives, fallback_expected_value=fallback)
    applied_cap = pricing.maximum_pledgeable_payment
    governance = solve_hidden_reuse(
        replace(hidden_primitives, context_payment_cap=applied_cap),
        disclosure_grid_size=disclosure_grid_size,
        tolerance=tolerance,
    )
    return PledgeableHiddenReuseOutcome(
        pricing=pricing,
        governance=governance,
        applied_context_payment_cap=applied_cap,
    )
