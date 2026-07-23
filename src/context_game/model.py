"""Analytical baseline for the context disclosure and ownership decision.

The context owner chooses external disclosure ``s`` in [0, 1]. Current joint
benefit is concave. Disclosure also dissipates an exclusive context rent. An
integrated owner can apply the full context without external leakage, but must
pay a fixed integration cost.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Union


class Regime(str, Enum):
    """Market structures selected by the baseline game."""

    MODULAR = "modular_sharing"
    WITHHOLDING = "strategic_withholding"
    OWNERSHIP = "ownership"


@dataclass(frozen=True)
class Primitives:
    """Primitive parameters of one context transaction.

    ``marginal_value_at_full`` is the marginal current benefit of the final
    unit of disclosure in the absence of Arrow friction. ``curvature`` governs
    diminishing returns. This parameterization guarantees that full disclosure
    is efficient when leakage is zero.
    """

    marginal_value_at_full: float = 0.55
    curvature: float = 0.45
    context_rent: float = 1.0
    leakage: float = 0.5
    protection: float = 0.2
    integration_cost: float = 0.5

    def validate(self) -> None:
        if self.marginal_value_at_full <= 0:
            raise ValueError("marginal_value_at_full must be positive")
        if self.curvature <= 0:
            raise ValueError("curvature must be positive")
        if self.context_rent < 0:
            raise ValueError("context_rent cannot be negative")
        if not 0 <= self.leakage <= 1:
            raise ValueError("leakage must lie in [0, 1]")
        if not 0 <= self.protection <= 1:
            raise ValueError("protection must lie in [0, 1]")
        if self.integration_cost < 0:
            raise ValueError("integration_cost cannot be negative")


@dataclass(frozen=True)
class Outcome:
    """Equilibrium outcome for one set of primitives."""

    regime: Regime
    disclosure: float
    effective_friction: float
    separate_value: float
    integrated_value: float
    integration_threshold: float


def gross_benefit(
    disclosure: Union[float, int], marginal_value_at_full: float, curvature: float
) -> float:
    """Current benefit from applying disclosed context.

    B(s) = (m + c)s - (c/2)s^2, so B'(1) = m > 0.
    """

    s = float(disclosure)
    return (marginal_value_at_full + curvature) * s - 0.5 * curvature * s * s


def effective_friction(primitives: Primitives) -> float:
    """Private rent dissipated by one unit of external disclosure."""

    return (
        primitives.context_rent
        * primitives.leakage
        * (1.0 - primitives.protection)
    )


def separate_disclosure(primitives: Primitives) -> float:
    """Optimal disclosure under arm's-length contracting."""

    friction = effective_friction(primitives)
    unconstrained = (
        primitives.marginal_value_at_full + primitives.curvature - friction
    ) / primitives.curvature
    return min(1.0, max(0.0, unconstrained))


def separate_value(primitives: Primitives) -> float:
    """Net value under the optimal separate-contracting policy."""

    s = separate_disclosure(primitives)
    value = gross_benefit(
        s, primitives.marginal_value_at_full, primitives.curvature
    ) - effective_friction(primitives) * s
    return max(0.0, value)


def integrated_value(primitives: Primitives) -> float:
    """Net value when ownership permits full internal context use."""

    return gross_benefit(
        1.0, primitives.marginal_value_at_full, primitives.curvature
    ) - primitives.integration_cost


def integration_threshold(primitives: Primitives) -> float:
    """Largest fixed integration cost for which ownership strictly dominates."""

    full_internal_value = gross_benefit(
        1.0, primitives.marginal_value_at_full, primitives.curvature
    )
    return max(0.0, full_internal_value - separate_value(primitives))


def solve(primitives: Primitives, tolerance: float = 1e-10) -> Outcome:
    """Solve the baseline disclosure/ownership game.

    Ties preserve modular organization: ownership must strictly improve on the
    best arm's-length arrangement by more than ``tolerance``.
    """

    primitives.validate()
    disclosure = separate_disclosure(primitives)
    arm_length = separate_value(primitives)
    integrated = integrated_value(primitives)
    threshold = integration_threshold(primitives)

    if integrated > arm_length + tolerance and integrated > tolerance:
        regime = Regime.OWNERSHIP
    elif disclosure >= 1.0 - tolerance:
        regime = Regime.MODULAR
    else:
        regime = Regime.WITHHOLDING

    return Outcome(
        regime=regime,
        disclosure=disclosure,
        effective_friction=effective_friction(primitives),
        separate_value=arm_length,
        integrated_value=integrated,
        integration_threshold=threshold,
    )

