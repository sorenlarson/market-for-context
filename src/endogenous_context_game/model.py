"""Two-party bargaining with endogenous context protection.

The context owner and model provider bargain over disclosure, protection, and a
transfer.  Ownership is the context owner's disagreement option.  With
transferable utility, the contract maximizes joint arm's-length surplus; Nash
bargaining then divides the gain over disagreement.
"""

from dataclasses import dataclass
from enum import Enum


class Regime(str, Enum):
    """Governance regimes, matching the analytical baseline's stable names."""

    MODULAR = "modular_sharing"
    WITHHOLDING = "strategic_withholding"
    OWNERSHIP = "ownership"


def gross_benefit(
    disclosure: float, marginal_value_at_full: float, curvature: float
) -> float:
    """Current benefit from applying context to the task."""

    s = float(disclosure)
    return (marginal_value_at_full + curvature) * s - 0.5 * curvature * s * s


@dataclass(frozen=True)
class ContractPrimitives:
    """Primitives of the endogenous-protection bargaining game.

    ``provider_learning_value`` is the part of the owner's leakage loss captured
    by the provider as reusable learning.  The difference between
    ``context_rent`` and ``provider_learning_value`` is genuine joint
    dissipation rather than a transfer between the two bargaining parties.

    ``protectability`` is the largest share of technological leakage that a
    fully protected contract can prevent.  ``protection_cost`` is the quadratic
    cost coefficient per unit of disclosed context.
    """

    marginal_value_at_full: float = 0.55
    curvature: float = 0.45
    context_rent: float = 1.0
    provider_learning_value: float = 0.25
    leakage: float = 0.5
    protectability: float = 0.8
    protection_cost: float = 0.4
    integration_cost: float = 0.5
    owner_bargaining_weight: float = 0.5
    provider_outside_option: float = 0.0

    def validate(self) -> None:
        if self.marginal_value_at_full <= 0:
            raise ValueError("marginal_value_at_full must be positive")
        if self.curvature <= 0:
            raise ValueError("curvature must be positive")
        if self.context_rent < 0:
            raise ValueError("context_rent cannot be negative")
        if not 0 <= self.provider_learning_value <= self.context_rent:
            raise ValueError(
                "provider_learning_value must lie between zero and context_rent"
            )
        if not 0 <= self.leakage <= 1:
            raise ValueError("leakage must lie in [0, 1]")
        if not 0 <= self.protectability <= 1:
            raise ValueError("protectability must lie in [0, 1]")
        if self.protection_cost < 0:
            raise ValueError("protection_cost cannot be negative")
        if self.integration_cost < 0:
            raise ValueError("integration_cost cannot be negative")
        if not 0 <= self.owner_bargaining_weight <= 1:
            raise ValueError("owner_bargaining_weight must lie in [0, 1]")
        if self.provider_outside_option < 0:
            raise ValueError("provider_outside_option cannot be negative")


@dataclass(frozen=True)
class ContractOutcome:
    """Subgame-perfect governance outcome with a generalized Nash contract."""

    regime: Regime
    agreement: bool
    disclosure: float
    context_use: float
    protection: float
    residual_leakage: float
    effective_joint_friction: float
    separate_value: float
    integrated_value: float
    owner_outside_option: float
    provider_outside_option: float
    bargaining_surplus: float
    transfer_to_provider: float
    owner_payoff: float
    provider_payoff: float
    integration_threshold: float


def joint_dissipation(primitives: ContractPrimitives) -> float:
    """Leakage loss not recaptured by either bargaining party."""

    return primitives.context_rent - primitives.provider_learning_value


def optimal_protection(primitives: ContractPrimitives) -> float:
    """Joint-surplus-maximizing protection intensity in [0, 1]."""

    primitives.validate()
    incentive = (
        joint_dissipation(primitives) * primitives.leakage * primitives.protectability
    )
    if incentive <= 0:
        return 0.0
    if primitives.protection_cost == 0:
        return 1.0
    return min(1.0, incentive / primitives.protection_cost)


def residual_leakage(primitives: ContractPrimitives, protection: float) -> float:
    """Technological leakage left after enforceable protection."""

    return primitives.leakage * (1.0 - primitives.protectability * protection)


def protection_cost_per_unit(
    primitives: ContractPrimitives, protection: float
) -> float:
    """Protection cost per unit of disclosed context."""

    return 0.5 * primitives.protection_cost * protection * protection


def effective_joint_friction(primitives: ContractPrimitives) -> float:
    """Minimized joint friction per unit of arm's-length disclosure."""

    protection = optimal_protection(primitives)
    return joint_dissipation(primitives) * residual_leakage(
        primitives, protection
    ) + protection_cost_per_unit(primitives, protection)


def optimal_disclosure(primitives: ContractPrimitives) -> float:
    """Joint-surplus-maximizing external disclosure after protection choice."""

    friction = effective_joint_friction(primitives)
    unconstrained = (
        primitives.marginal_value_at_full + primitives.curvature - friction
    ) / primitives.curvature
    return min(1.0, max(0.0, unconstrained))


def arm_length_value(primitives: ContractPrimitives) -> float:
    """Maximum total payoff available under arm's-length contracting."""

    disclosure = optimal_disclosure(primitives)
    value = (
        gross_benefit(
            disclosure,
            primitives.marginal_value_at_full,
            primitives.curvature,
        )
        - effective_joint_friction(primitives) * disclosure
    )
    return max(0.0, value)


def internal_value_before_cost(primitives: ContractPrimitives) -> float:
    """Value of full context use inside an integrated owner."""

    return gross_benefit(
        1.0,
        primitives.marginal_value_at_full,
        primitives.curvature,
    )


def integration_threshold(primitives: ContractPrimitives) -> float:
    """Largest integration cost below which ownership strictly dominates.

    The threshold includes the provider's forgone outside option.  It is capped
    by the gross internal value because an owner never selects negative-value
    integration.
    """

    full_internal = internal_value_before_cost(primitives)
    candidate = (
        full_internal
        + primitives.provider_outside_option
        - arm_length_value(primitives)
    )
    return max(0.0, min(full_internal, candidate))


def solve_contract(
    primitives: ContractPrimitives, tolerance: float = 1e-10
) -> ContractOutcome:
    """Solve the bargaining, disclosure, protection, and ownership game.

    The owner can integrate or withhold at the disagreement node.  When an
    arm's-length agreement creates nonnegative surplus over both parties'
    outside options, generalized Nash bargaining implements the efficient
    disclosure/protection pair and divides the surplus.  Ties preserve
    separation.
    """

    primitives.validate()
    candidate_protection = optimal_protection(primitives)
    candidate_disclosure = optimal_disclosure(primitives)
    friction = effective_joint_friction(primitives)
    separated = arm_length_value(primitives)
    integrated = internal_value_before_cost(primitives) - primitives.integration_cost
    owner_outside = max(0.0, integrated)
    provider_outside = primitives.provider_outside_option
    total_outside = owner_outside + provider_outside
    agreement = separated >= total_outside

    if agreement:
        surplus = max(0.0, separated - total_outside)
        owner_payoff = owner_outside + primitives.owner_bargaining_weight * surplus
        provider_payoff = (
            provider_outside + (1.0 - primitives.owner_bargaining_weight) * surplus
        )
        disclosure = candidate_disclosure
        protection = candidate_protection if disclosure > tolerance else 0.0
        leak = residual_leakage(primitives, protection)
        owner_pretransfer = (
            gross_benefit(
                disclosure,
                primitives.marginal_value_at_full,
                primitives.curvature,
            )
            - primitives.context_rent * leak * disclosure
        )
        transfer = owner_pretransfer - owner_payoff
        regime = Regime.MODULAR if disclosure >= 1.0 - tolerance else Regime.WITHHOLDING
        context_use = disclosure
    elif integrated > tolerance:
        regime = Regime.OWNERSHIP
        surplus = 0.0
        disclosure = 0.0
        context_use = 1.0
        protection = 0.0
        leak = 0.0
        transfer = 0.0
        owner_payoff = integrated
        provider_payoff = provider_outside
    else:
        regime = Regime.WITHHOLDING
        surplus = 0.0
        disclosure = 0.0
        context_use = 0.0
        protection = 0.0
        leak = 0.0
        transfer = 0.0
        owner_payoff = 0.0
        provider_payoff = provider_outside

    return ContractOutcome(
        regime=regime,
        agreement=agreement,
        disclosure=disclosure,
        context_use=context_use,
        protection=protection,
        residual_leakage=leak,
        effective_joint_friction=friction,
        separate_value=separated,
        integrated_value=integrated,
        owner_outside_option=owner_outside,
        provider_outside_option=provider_outside,
        bargaining_surplus=surplus,
        transfer_to_provider=transfer,
        owner_payoff=owner_payoff,
        provider_payoff=provider_payoff,
        integration_threshold=integration_threshold(primitives),
    )
