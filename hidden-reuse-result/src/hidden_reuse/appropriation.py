"""Value creation versus value capture in an AI learning network.

The ownership-access model asks whether useful learning can travel through
independent customer relationships.  This extension asks a separate question:
if the learning travels, can the intermediary charge for the operating value it
creates?

For an ownership subset ``S``, the incremental private value relative to a
neutral platform is

    direct internalization
    + capture upgrade on value landing at owned nodes
    + productive learning unlocked inside the ownership boundary
    - ownership, organization, coordination, and neutrality costs.

The decomposition is exact.  It nests the earlier ownership-access model when
both capture shares equal one (``o = p = 1``); equal shares below one scale the
productive-learning term and do not reproduce it.  It also exposes a new
force: external customer access can complement selective ownership when outside
customers supply learning that is monetized inside owned operating assets.

The module additionally supplies a Pareto task-pricing benchmark.  It maps the
task-value tail parameter used in ``A Complexity Theory of AI Value Accrual``
to a provider capture share under single-price monopoly.  That mapping is a
calibration device, not an assertion that real AI markets are monopolies or
that all value has a Pareto distribution.
"""

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, Optional

from .ownership_access import (
    HomogeneousOwnershipAccessPrimitives,
    OwnershipAccessPrimitives,
    OwnershipAccessRegime,
    evaluate_ownership_subset,
    homogeneous_network,
    vertical_customer_network,
)


@dataclass(frozen=True)
class ParetoTaskPrimitives:
    """Primitives for a single-price Pareto task-value benchmark.

    Task value ``v`` has support ``[minimum_task_value, infinity)`` and tail
    probability ``Pr(v >= z) = (minimum_task_value / z) ** tail_index``.
    ``tail_index`` must exceed one so expected task value is finite.
    """

    tail_index: float = 1.5
    minimum_task_value: float = 1.0
    marginal_cost: float = 1.0
    task_mass: float = 1.0

    def validate(self) -> None:
        finite = {
            "tail_index": self.tail_index,
            "minimum_task_value": self.minimum_task_value,
            "marginal_cost": self.marginal_cost,
            "task_mass": self.task_mass,
        }
        if any(not isfinite(value) for value in finite.values()):
            raise ValueError("Pareto pricing primitives must be finite")
        if self.tail_index <= 1:
            raise ValueError("tail_index must exceed one")
        if self.minimum_task_value <= 0:
            raise ValueError("minimum_task_value must be positive")
        if self.marginal_cost < 0:
            raise ValueError("marginal_cost cannot be negative")
        if self.task_mass <= 0:
            raise ValueError("task_mass must be positive")


@dataclass(frozen=True)
class ParetoPricingOutcome:
    """Exact single-price solution and its surplus allocation."""

    monopoly_price: float
    quantity: float
    provider_profit: float
    customer_surplus: float
    platform_total_surplus: float
    integrated_operating_surplus: float
    provider_capture_share: float
    pricing_deadweight_loss: float


def pareto_demand_fraction(price: float, primitives: ParetoTaskPrimitives) -> float:
    """Fraction of tasks whose value weakly exceeds ``price``."""

    primitives.validate()
    if not isfinite(price) or price < 0:
        raise ValueError("price must be finite and nonnegative")
    if price <= primitives.minimum_task_value:
        return 1.0
    return (primitives.minimum_task_value / price) ** primitives.tail_index


def solve_pareto_pricing(primitives: ParetoTaskPrimitives) -> ParetoPricingOutcome:
    """Solve the monopoly benchmark and compare it with residual ownership.

    The provider posts one price before observing task value.  An integrated
    operator instead applies AI whenever task value covers marginal cost.  The
    latter comparison isolates both the surplus left with served customers and
    the tasks excluded by a common markup.
    """

    primitives.validate()
    alpha = primitives.tail_index
    minimum = primitives.minimum_task_value
    cost = primitives.marginal_cost
    mass = primitives.task_mass

    interior_price = alpha * cost / (alpha - 1.0)
    price = max(minimum, interior_price)
    demand = pareto_demand_fraction(price, primitives)
    quantity = mass * demand
    profit = quantity * (price - cost)

    if price <= minimum:
        expected_value = alpha * minimum / (alpha - 1.0)
        customer_surplus = mass * (expected_value - price)
    else:
        customer_surplus = quantity * price / (alpha - 1.0)
    platform_surplus = profit + customer_surplus

    if cost <= minimum:
        expected_value = alpha * minimum / (alpha - 1.0)
        integrated_surplus = mass * (expected_value - cost)
    else:
        efficient_quantity = mass * (minimum / cost) ** alpha
        integrated_surplus = efficient_quantity * cost / (alpha - 1.0)

    capture_share = profit / platform_surplus
    return ParetoPricingOutcome(
        monopoly_price=price,
        quantity=quantity,
        provider_profit=profit,
        customer_surplus=customer_surplus,
        platform_total_surplus=platform_surplus,
        integrated_operating_surplus=integrated_surplus,
        provider_capture_share=capture_share,
        pricing_deadweight_loss=max(0.0, integrated_surplus - platform_surplus),
    )


@dataclass(frozen=True)
class CaptureShareFrictions:
    """One pledgeability friction applied symmetrically to both capture markets.

    The bilateral extension prices a learning right with the pledgeable-payment
    logic ``P* = min(mu, W + phi * mu)``: a party charging for value realized
    later collects only what its counterparty commits before realization plus
    the share an auditor, court, or payment system can verify afterward.

    The same logic disciplines both capture shares here, on opposite sides:

    - In the service market the AI intermediary is the charging party.  It
      collects the customer's ex-ante commitment ``service_commitment_share``
      plus the ex-post verifiable share ``service_verifiable_share`` of the
      operating value its system creates, so weak verifiability *lowers* the
      platform share ``p``.
    - In the market for corporate control the seller is the charging party.  It
      capitalizes into the acquisition price only the pledgeable share of
      prospective AI gains, weighted by its bargaining position, so weak
      verifiability *raises* the acquirer's retained share ``o``.

    Under fully symmetric frictions (equal commitment and verifiable shares,
    full seller bargaining weight, no pass-through), ``o > p`` if and only if
    the pledgeable share of AI-created value is below one half.  The sign of
    the capture wedge is then a statement about which market can verify
    realized AI value, not a free calibration.
    """

    service_verifiable_share: float = 0.15
    service_commitment_share: float = 0.10
    acquisition_verifiable_share: float = 0.40
    acquisition_commitment_share: float = 0.15
    seller_bargaining_weight: float = 1.0
    downstream_passthrough_share: float = 0.0

    def validate(self) -> None:
        for name, value in {
            "service_verifiable_share": self.service_verifiable_share,
            "service_commitment_share": self.service_commitment_share,
            "acquisition_verifiable_share": self.acquisition_verifiable_share,
            "acquisition_commitment_share": self.acquisition_commitment_share,
            "seller_bargaining_weight": self.seller_bargaining_weight,
            "downstream_passthrough_share": self.downstream_passthrough_share,
        }.items():
            if not isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"{name} must lie in [0, 1]")


@dataclass(frozen=True)
class DerivedCaptureShares:
    """Both capture shares expressed as pledgeability outcomes."""

    platform_capture_share: float
    owner_capture_share: float
    capture_wedge: float
    service_pledgeable_share: float
    acquisition_pledgeable_share: float
    seller_capitalized_share: float


def derive_capture_shares(frictions: CaptureShareFrictions) -> DerivedCaptureShares:
    """Derive ``p`` and ``o`` from one symmetric pledgeability friction.

    The platform share is the pledgeable fraction of customer-side value:

        p = min(1, w_s + phi_s).

    The owner share is what the acquirer keeps after the seller capitalizes
    the pledgeable fraction of prospective gains and the product market passes
    through a further share:

        o = (1 - beta * min(1, w_a + phi_a)) * (1 - passthrough).
    """

    frictions.validate()
    service_pledgeable = min(
        1.0,
        frictions.service_commitment_share + frictions.service_verifiable_share,
    )
    acquisition_pledgeable = min(
        1.0,
        frictions.acquisition_commitment_share + frictions.acquisition_verifiable_share,
    )
    seller_capitalized = frictions.seller_bargaining_weight * acquisition_pledgeable
    platform_share = service_pledgeable
    owner_share = (1.0 - seller_capitalized) * (
        1.0 - frictions.downstream_passthrough_share
    )
    return DerivedCaptureShares(
        platform_capture_share=platform_share,
        owner_capture_share=owner_share,
        capture_wedge=owner_share - platform_share,
        service_pledgeable_share=service_pledgeable,
        acquisition_pledgeable_share=acquisition_pledgeable,
        seller_capitalized_share=seller_capitalized,
    )


def with_derived_capture_shares(
    primitives: "ValueAppropriationPrimitives",
    frictions: CaptureShareFrictions,
) -> "ValueAppropriationPrimitives":
    """Replace both reduced-form capture shares with derived pledgeable shares."""

    shares = derive_capture_shares(frictions)
    return ValueAppropriationPrimitives(
        network=primitives.network,
        operating_surplus=primitives.operating_surplus,
        platform_capture_share=shares.platform_capture_share,
        owner_capture_share=shares.owner_capture_share,
    )


@dataclass(frozen=True)
class ValueAppropriationPrimitives:
    """A directed ownership-access network with explicit surplus capture.

    ``operating_surplus[j]`` is AI-enabled value generated at node ``j`` before
    it is divided between the intermediary and the independent operator.
    ``platform_capture_share`` is the intermediary's share while the node is a
    customer. ``owner_capture_share`` is the acquirer's retained share under
    ownership after acquisition-price capitalization, bargaining, and any
    downstream pass-through.  Both are private-value shares, not welfare
    weights.
    """

    network: OwnershipAccessPrimitives
    operating_surplus: tuple[float, ...]
    platform_capture_share: float = 0.25
    owner_capture_share: float = 0.45

    def validate(self) -> None:
        self.network.validate()
        if len(self.operating_surplus) != len(self.network.nodes):
            raise ValueError("operating_surplus must match the network nodes")
        if any(not isfinite(value) or value < 0 for value in self.operating_surplus):
            raise ValueError("operating_surplus entries must be finite and nonnegative")
        shares = {
            "platform_capture_share": self.platform_capture_share,
            "owner_capture_share": self.owner_capture_share,
        }
        for name, value in shares.items():
            if not isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"{name} must lie in [0, 1]")


@dataclass(frozen=True)
class ValueAppropriationCandidate:
    """Private-value decomposition for one possible ownership subset."""

    owned_indices: tuple[int, ...]
    owned_names: tuple[str, ...]
    regime: OwnershipAccessRegime
    owned_operating_surplus: float
    internal_learning: float
    incoming_customer_learning: float
    internalization_value: float
    capture_upgrade: float
    productive_learning_upgrade: float
    external_access_slope: float
    fixed_cost: float
    organization_cost: float
    coordination_cost: float
    boundary_customer_exposure: float
    neutrality_loss: float
    baseline_platform_value: float
    incremental_private_value: float
    total_private_value: float

    @property
    def size(self) -> int:
        return len(self.owned_indices)


@dataclass(frozen=True)
class ValueAppropriationOutcome:
    """Exact subset solution and exhaustive deviation evidence."""

    regime: OwnershipAccessRegime
    owned_indices: tuple[int, ...]
    owned_names: tuple[str, ...]
    ownership_size: int
    baseline_platform_value: float
    incremental_private_value: float
    total_private_value: float
    best_alternative_value: float
    selection_margin: float
    maximum_deviation_gain: float
    co_maximizing_subsets: tuple[tuple[int, ...], ...]
    chosen: ValueAppropriationCandidate
    candidates: tuple[ValueAppropriationCandidate, ...]


def _network_learning_total(network: OwnershipAccessPrimitives) -> float:
    return sum(sum(row) for row in network.learning)


def evaluate_value_appropriation_subset(
    primitives: ValueAppropriationPrimitives,
    owned_indices: Iterable[int],
) -> ValueAppropriationCandidate:
    """Evaluate one ownership choice relative to the all-customer platform."""

    primitives.validate()
    base = evaluate_ownership_subset(primitives.network, owned_indices)
    owned = base.owned_indices
    owned_set = set(owned)
    size = len(primitives.network.nodes)
    q = primitives.network.external_learning_efficiency
    platform_share = primitives.platform_capture_share
    owner_share = primitives.owner_capture_share

    owned_operating = sum(primitives.operating_surplus[index] for index in owned)
    internal_learning = sum(
        primitives.network.learning[source][target]
        for source in owned
        for target in owned
        if source != target
    )
    incoming_learning = sum(
        primitives.network.learning[source][target]
        for source in range(size)
        for target in owned
        if source not in owned_set and source != target
    )
    platform_available_at_owned_nodes = owned_operating + q * (
        internal_learning + incoming_learning
    )
    capture_upgrade = (owner_share - platform_share) * platform_available_at_owned_nodes
    productive_upgrade = owner_share * (1.0 - q) * internal_learning
    access_slope = (
        owner_share - platform_share
    ) * incoming_learning - platform_share * internal_learning
    baseline = platform_share * (
        sum(primitives.operating_surplus)
        + q * _network_learning_total(primitives.network)
    )
    incremental = (
        base.internalization_value
        + capture_upgrade
        + productive_upgrade
        - base.fixed_cost
        - base.organization_cost
        - base.coordination_cost
        - base.neutrality_loss
    )
    return ValueAppropriationCandidate(
        owned_indices=owned,
        owned_names=base.owned_names,
        regime=base.regime,
        owned_operating_surplus=owned_operating,
        internal_learning=internal_learning,
        incoming_customer_learning=incoming_learning,
        internalization_value=base.internalization_value,
        capture_upgrade=capture_upgrade,
        productive_learning_upgrade=productive_upgrade,
        external_access_slope=access_slope,
        fixed_cost=base.fixed_cost,
        organization_cost=base.organization_cost,
        coordination_cost=base.coordination_cost,
        boundary_customer_exposure=base.boundary_customer_exposure,
        neutrality_loss=base.neutrality_loss,
        baseline_platform_value=baseline,
        incremental_private_value=incremental,
        total_private_value=baseline + incremental,
    )


def solve_value_appropriation(
    primitives: ValueAppropriationPrimitives, *, tolerance: float = 1e-10
) -> ValueAppropriationOutcome:
    """Enumerate all ownership subsets and select the private optimum."""

    primitives.validate()
    size = len(primitives.network.nodes)
    candidates = tuple(
        evaluate_value_appropriation_subset(
            primitives,
            (index for index in range(size) if mask & (1 << index)),
        )
        for mask in range(1 << size)
    )
    best_value = max(candidate.incremental_private_value for candidate in candidates)
    co_maximizers = tuple(
        candidate.owned_indices
        for candidate in candidates
        if abs(candidate.incremental_private_value - best_value) <= tolerance
    )
    chosen_subset = min(co_maximizers, key=lambda subset: (len(subset), subset))
    chosen = next(
        candidate
        for candidate in candidates
        if candidate.owned_indices == chosen_subset
    )
    alternatives = [
        candidate.incremental_private_value
        for candidate in candidates
        if candidate.owned_indices != chosen_subset
    ]
    best_alternative = (
        max(alternatives) if alternatives else chosen.incremental_private_value
    )
    deviation_gain = max(
        candidate.incremental_private_value - chosen.incremental_private_value
        for candidate in candidates
    )
    return ValueAppropriationOutcome(
        regime=chosen.regime,
        owned_indices=chosen.owned_indices,
        owned_names=chosen.owned_names,
        ownership_size=chosen.size,
        baseline_platform_value=chosen.baseline_platform_value,
        incremental_private_value=chosen.incremental_private_value,
        total_private_value=chosen.total_private_value,
        best_alternative_value=best_alternative,
        selection_margin=chosen.incremental_private_value - best_alternative,
        maximum_deviation_gain=max(0.0, deviation_gain),
        co_maximizing_subsets=co_maximizers,
        chosen=chosen,
        candidates=candidates,
    )


@dataclass(frozen=True)
class HomogeneousValueAppropriationPrimitives:
    """Symmetric benchmark with analytical platform-rollup boundaries."""

    asset_count: int = 6
    internalization_advantage: float = 0.215
    directed_pair_learning: float = 0.105
    per_asset_operating_surplus: float = 0.80
    external_learning_efficiency: float = 0.55
    platform_capture_share: float = 0.25
    owner_capture_share: float = 0.45
    fixed_ownership_cost: float = 0.150
    organization_cost_scale: float = 0.100
    organization_cost_elasticity: float = 1.70
    pair_coordination_cost: float = 0.027
    neutrality_penalty: float = 0.60
    boundary_customer_value_per_unordered_pair: float = 0.020

    def ownership_primitives(self) -> HomogeneousOwnershipAccessPrimitives:
        """Return the corresponding learning-and-customer benchmark."""

        return HomogeneousOwnershipAccessPrimitives(
            asset_count=self.asset_count,
            internalization_advantage=self.internalization_advantage,
            directed_pair_learning=self.directed_pair_learning,
            external_learning_efficiency=self.external_learning_efficiency,
            fixed_ownership_cost=self.fixed_ownership_cost,
            organization_cost_scale=self.organization_cost_scale,
            organization_cost_elasticity=self.organization_cost_elasticity,
            pair_coordination_cost=self.pair_coordination_cost,
            neutrality_penalty=self.neutrality_penalty,
            boundary_customer_value_per_unordered_pair=(
                self.boundary_customer_value_per_unordered_pair
            ),
        )

    def validate(self) -> None:
        self.ownership_primitives().validate()
        if (
            not isfinite(self.per_asset_operating_surplus)
            or self.per_asset_operating_surplus < 0
        ):
            raise ValueError(
                "per_asset_operating_surplus must be finite and nonnegative"
            )
        for name, value in {
            "platform_capture_share": self.platform_capture_share,
            "owner_capture_share": self.owner_capture_share,
        }.items():
            if not isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"{name} must lie in [0, 1]")


def homogeneous_value_candidate_increment(
    owned_size: int, primitives: HomogeneousValueAppropriationPrimitives
) -> float:
    """Incremental private value of owning ``owned_size`` symmetric assets."""

    primitives.validate()
    if (
        isinstance(owned_size, bool)
        or not isinstance(owned_size, int)
        or not 0 <= owned_size <= primitives.asset_count
    ):
        raise ValueError("owned_size must lie between zero and asset_count")
    if owned_size == 0:
        return 0.0

    total = primitives.asset_count
    internal_learning = (
        primitives.directed_pair_learning * owned_size * (owned_size - 1)
    )
    incoming_learning = (
        primitives.directed_pair_learning * owned_size * (total - owned_size)
    )
    owned_operating = primitives.per_asset_operating_surplus * owned_size
    capture_upgrade = (
        primitives.owner_capture_share - primitives.platform_capture_share
    ) * (
        owned_operating
        + primitives.external_learning_efficiency
        * (internal_learning + incoming_learning)
    )
    productive_upgrade = (
        primitives.owner_capture_share
        * (1.0 - primitives.external_learning_efficiency)
        * internal_learning
    )
    boundary_pairs = owned_size * (total - owned_size)
    unordered_internal_pairs = owned_size * (owned_size - 1) / 2.0
    return (
        owned_size * primitives.internalization_advantage
        + capture_upgrade
        + productive_upgrade
        - primitives.fixed_ownership_cost
        - primitives.organization_cost_scale
        * owned_size**primitives.organization_cost_elasticity
        - primitives.pair_coordination_cost * unordered_internal_pairs
        - primitives.neutrality_penalty
        * primitives.boundary_customer_value_per_unordered_pair
        * boundary_pairs
    )


def homogeneous_value_network(
    primitives: HomogeneousValueAppropriationPrimitives,
) -> ValueAppropriationPrimitives:
    """Build the exact matrix representation of the symmetric formulas."""

    primitives.validate()
    network = homogeneous_network(primitives.ownership_primitives())
    return ValueAppropriationPrimitives(
        network=network,
        operating_surplus=tuple(
            primitives.per_asset_operating_surplus
            for _ in range(primitives.asset_count)
        ),
        platform_capture_share=primitives.platform_capture_share,
        owner_capture_share=primitives.owner_capture_share,
    )


def _homogeneous_full_cost(
    primitives: HomogeneousValueAppropriationPrimitives,
) -> float:
    size = primitives.asset_count
    return (
        primitives.fixed_ownership_cost
        + primitives.organization_cost_scale
        * size**primitives.organization_cost_elasticity
        + primitives.pair_coordination_cost * size * (size - 1) / 2.0
    )


def platform_rollup_capture_threshold(
    primitives: HomogeneousValueAppropriationPrimitives,
) -> Optional[float]:
    """Raw platform capture share at which the two pure modes tie."""

    primitives.validate()
    size = primitives.asset_count
    operating = primitives.per_asset_operating_surplus * size
    learning = primitives.directed_pair_learning * size * (size - 1)
    platform_value_base = operating + primitives.external_learning_efficiency * learning
    if platform_value_base == 0:
        return None
    rollup_value = (
        size * primitives.internalization_advantage
        + primitives.owner_capture_share * (operating + learning)
        - _homogeneous_full_cost(primitives)
    )
    return rollup_value / platform_value_base


def platform_rollup_access_threshold(
    primitives: HomogeneousValueAppropriationPrimitives,
) -> Optional[float]:
    """Raw external-learning efficiency at which the pure modes tie."""

    primitives.validate()
    size = primitives.asset_count
    operating = primitives.per_asset_operating_surplus * size
    learning = primitives.directed_pair_learning * size * (size - 1)
    if primitives.platform_capture_share * learning == 0:
        return None
    numerator = (
        size * primitives.internalization_advantage
        + primitives.owner_capture_share * (operating + learning)
        - _homogeneous_full_cost(primitives)
        - primitives.platform_capture_share * operating
    )
    return numerator / (primitives.platform_capture_share * learning)


def vertical_value_appropriation_network(
    *,
    external_learning_efficiency: float = 0.65,
    neutrality_penalty: float = 0.10,
    platform_capture_share: float = 0.25,
    owner_capture_share: float = 0.45,
) -> ValueAppropriationPrimitives:
    """Six-node clinic-lab-payer example with unequal operating surplus."""

    network = vertical_customer_network(
        external_learning_efficiency=external_learning_efficiency,
        neutrality_penalty=neutrality_penalty,
    )
    return ValueAppropriationPrimitives(
        network=network,
        operating_surplus=(1.20, 1.05, 0.72, 0.64, 0.48, 0.42),
        platform_capture_share=platform_capture_share,
        owner_capture_share=owner_capture_share,
    )
