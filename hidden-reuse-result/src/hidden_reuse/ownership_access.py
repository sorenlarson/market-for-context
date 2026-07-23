"""Ownership versus customer access in heterogeneous learning networks.

The homogeneous firm-size model asks how many interchangeable assets an
integrated firm should own.  This module lets assets differ and admits a second
way to aggregate their learning: keep them independent and serve them through
a common intermediary.

The intermediary begins as a neutral platform serving every node.  It can buy
any subset ``S`` of the context-generating assets.  Relative to remaining a
platform, the value of that choice is

    Delta(S) = sum(a_i for i in S)
             + (1 - q) sum(gamma_ij for i, j in S)
             - C(S)
             - chi sum(d_ij for ownership boundaries crossed by i -> j).

``a_i`` is the direct internalization advantage inherited from the bilateral
hidden-reuse problem. ``q`` is the fraction of cross-node learning that can be
realized through contracts and customer access without ownership. ``gamma`` is
a directed learning matrix. ``d`` is a directed customer-dependence matrix:
partial ownership can make the intermediary less neutral and put relationships
that cross its ownership boundary at risk. ``C`` contains a fixed ownership
cost, convex organization cost, and pair-specific coordination burdens.
An optional fringe-customer term opens the network: it charges the same
neutrality penalty on outside-customer value per owned asset, so even the
full rollup of modeled nodes bears conflict cost when it is switched on.

The game is deliberately a single-intermediary acquisition benchmark.  Offers
are assumed to compensate each acquired node for its fallback, so ``a_i`` is
net of that payment.  Exhaustive subset search therefore gives the
intermediary's reduced-form acquisition equilibrium.  It is not a general
equilibrium of competing platforms or a welfare calculation.
"""

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from typing import Iterable, Optional


class OwnershipAccessRegime(str, Enum):
    """Organizational forms selected by the ownership-access game."""

    PLATFORM = "neutral_platform"
    SINGLE_ASSET = "single_asset_ownership"
    SPECIALIZED_ROLLUP = "specialized_partial_rollup"
    CROSS_TYPE_ROLLUP = "cross_type_partial_rollup"
    FULL_ROLLUP = "full_network_rollup"


@dataclass(frozen=True)
class NetworkNode:
    """One heterogeneous context-generating asset or operating business."""

    name: str
    kind: str
    internalization_advantage: float

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError("node name cannot be empty")
        if not self.kind.strip():
            raise ValueError("node kind cannot be empty")
        if not isfinite(self.internalization_advantage):
            raise ValueError("internalization_advantage must be finite")


Matrix = tuple[tuple[float, ...], ...]


def _zero_matrix(size: int) -> Matrix:
    return tuple(tuple(0.0 for _ in range(size)) for _ in range(size))


def _validate_matrix(
    matrix: Matrix,
    size: int,
    name: str,
    *,
    symmetric: bool = False,
    tolerance: float = 1e-12,
) -> None:
    if len(matrix) != size or any(len(row) != size for row in matrix):
        raise ValueError(f"{name} must be a square matrix matching the nodes")
    for row, values in enumerate(matrix):
        for column, value in enumerate(values):
            if not isfinite(value) or value < 0:
                raise ValueError(f"{name} entries must be finite and nonnegative")
            if row == column and abs(value) > tolerance:
                raise ValueError(f"{name} diagonal must be zero")
            if symmetric and abs(value - matrix[column][row]) > tolerance:
                raise ValueError(f"{name} must be symmetric")


@dataclass(frozen=True)
class OwnershipAccessPrimitives:
    """Primitives for one heterogeneous ownership-access network.

    Learning and customer relationships may be directed.  Coordination costs
    are symmetric because they are paid once for each owned pair.  Matrices
    default to zero only when a caller constructs the class programmatically;
    most useful scenarios should supply all three explicitly.

    ``fringe_customer_value_per_owned_asset`` opens the otherwise closed
    network: it is the value of relationships with never-acquirable outside
    customers put at risk for each asset the intermediary owns.  Every owned
    asset adds that amount to boundary customer exposure, so a full rollup of
    the modeled nodes is no longer automatically conflict-free.  The default of
    zero reproduces the original closed-network model exactly.
    """

    nodes: tuple[NetworkNode, ...]
    learning: Matrix
    customer_dependence: Matrix
    coordination_cost: Matrix
    external_learning_efficiency: float = 0.55
    neutrality_penalty: float = 0.25
    fixed_ownership_cost: float = 0.20
    organization_cost_scale: float = 0.025
    organization_cost_elasticity: float = 1.50
    fringe_customer_value_per_owned_asset: float = 0.0

    def validate(self) -> None:
        if not self.nodes:
            raise ValueError("at least one node is required")
        if len(self.nodes) > 20:
            raise ValueError("exact subset search is limited to 20 nodes")
        for node in self.nodes:
            node.validate()
        names = [node.name for node in self.nodes]
        if len(set(names)) != len(names):
            raise ValueError("node names must be unique")
        size = len(self.nodes)
        _validate_matrix(self.learning, size, "learning")
        _validate_matrix(self.customer_dependence, size, "customer_dependence")
        _validate_matrix(
            self.coordination_cost,
            size,
            "coordination_cost",
            symmetric=True,
        )
        bounded = {
            "external_learning_efficiency": self.external_learning_efficiency,
        }
        for name, value in bounded.items():
            if not isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"{name} must lie in [0, 1]")
        nonnegative = {
            "neutrality_penalty": self.neutrality_penalty,
            "fixed_ownership_cost": self.fixed_ownership_cost,
            "organization_cost_scale": self.organization_cost_scale,
            "fringe_customer_value_per_owned_asset": (
                self.fringe_customer_value_per_owned_asset
            ),
        }
        for name, value in nonnegative.items():
            if not isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if (
            not isfinite(self.organization_cost_elasticity)
            or self.organization_cost_elasticity < 1
        ):
            raise ValueError("organization_cost_elasticity must be at least one")


@dataclass(frozen=True)
class OwnershipCandidate:
    """Value decomposition for one possible ownership subset."""

    owned_indices: tuple[int, ...]
    owned_names: tuple[str, ...]
    regime: OwnershipAccessRegime
    internalization_value: float
    learning_upgrade: float
    fixed_cost: float
    organization_cost: float
    coordination_cost: float
    boundary_customer_exposure: float
    neutrality_loss: float
    incremental_value: float
    total_private_value: float

    @property
    def size(self) -> int:
        return len(self.owned_indices)


@dataclass(frozen=True)
class OwnershipAccessOutcome:
    """Exact ownership equilibrium and exhaustive deviation evidence."""

    regime: OwnershipAccessRegime
    owned_indices: tuple[int, ...]
    owned_names: tuple[str, ...]
    ownership_size: int
    platform_learning_value: float
    incremental_value: float
    total_private_value: float
    best_alternative_value: float
    selection_margin: float
    maximum_deviation_gain: float
    co_maximizing_subsets: tuple[tuple[int, ...], ...]
    chosen: OwnershipCandidate
    candidates: tuple[OwnershipCandidate, ...]


def _regime_for_subset(
    owned: tuple[int, ...], nodes: tuple[NetworkNode, ...]
) -> OwnershipAccessRegime:
    if not owned:
        return OwnershipAccessRegime.PLATFORM
    if len(owned) == len(nodes):
        return OwnershipAccessRegime.FULL_ROLLUP
    if len(owned) == 1:
        return OwnershipAccessRegime.SINGLE_ASSET
    kinds = {nodes[index].kind for index in owned}
    if len(kinds) == 1:
        return OwnershipAccessRegime.SPECIALIZED_ROLLUP
    return OwnershipAccessRegime.CROSS_TYPE_ROLLUP


def evaluate_ownership_subset(
    primitives: OwnershipAccessPrimitives,
    owned_indices: Iterable[int],
) -> OwnershipCandidate:
    """Evaluate one acquisition choice relative to a neutral platform."""

    primitives.validate()
    size = len(primitives.nodes)
    owned = tuple(sorted(set(owned_indices)))
    if any(isinstance(index, bool) or not isinstance(index, int) for index in owned):
        raise ValueError("owned indices must be integers")
    if any(index < 0 or index >= size for index in owned):
        raise ValueError("owned index outside the network")
    owned_set = set(owned)

    direct = sum(primitives.nodes[index].internalization_advantage for index in owned)
    internal_learning = sum(
        primitives.learning[source][target]
        for source in owned
        for target in owned
        if source != target
    )
    learning_upgrade = (
        1.0 - primitives.external_learning_efficiency
    ) * internal_learning
    fixed = primitives.fixed_ownership_cost if owned else 0.0
    organization = (
        primitives.organization_cost_scale
        * len(owned) ** primitives.organization_cost_elasticity
        if owned
        else 0.0
    )
    coordination = sum(
        primitives.coordination_cost[left][right]
        for position, left in enumerate(owned)
        for right in owned[position + 1 :]
    )
    exposure = sum(
        primitives.customer_dependence[source][target]
        for source in range(size)
        for target in range(size)
        if (source in owned_set) != (target in owned_set)
    ) + primitives.fringe_customer_value_per_owned_asset * len(owned)
    neutrality_loss = primitives.neutrality_penalty * exposure
    incremental = (
        direct
        + learning_upgrade
        - fixed
        - organization
        - coordination
        - neutrality_loss
    )
    platform_learning = primitives.external_learning_efficiency * sum(
        sum(row) for row in primitives.learning
    )
    return OwnershipCandidate(
        owned_indices=owned,
        owned_names=tuple(primitives.nodes[index].name for index in owned),
        regime=_regime_for_subset(owned, primitives.nodes),
        internalization_value=direct,
        learning_upgrade=learning_upgrade,
        fixed_cost=fixed,
        organization_cost=organization,
        coordination_cost=coordination,
        boundary_customer_exposure=exposure,
        neutrality_loss=neutrality_loss,
        incremental_value=incremental,
        total_private_value=platform_learning + incremental,
    )


def solve_ownership_access(
    primitives: OwnershipAccessPrimitives, *, tolerance: float = 1e-10
) -> OwnershipAccessOutcome:
    """Enumerate every ownership subset and select the private optimum.

    Ties are exposed and resolved toward fewer acquisitions, then toward the
    lexicographically first tuple of node indices.  The reported deviation gain
    compares the selected subset with every other feasible subset.
    """

    primitives.validate()
    size = len(primitives.nodes)
    candidates = tuple(
        evaluate_ownership_subset(
            primitives,
            (index for index in range(size) if mask & (1 << index)),
        )
        for mask in range(1 << size)
    )
    best_value = max(candidate.incremental_value for candidate in candidates)
    co_maximizers = tuple(
        candidate.owned_indices
        for candidate in candidates
        if abs(candidate.incremental_value - best_value) <= tolerance
    )
    chosen_subset = min(co_maximizers, key=lambda subset: (len(subset), subset))
    chosen = next(
        candidate
        for candidate in candidates
        if candidate.owned_indices == chosen_subset
    )
    alternatives = [
        candidate.incremental_value
        for candidate in candidates
        if candidate.owned_indices != chosen_subset
    ]
    best_alternative = max(alternatives) if alternatives else chosen.incremental_value
    deviation_gain = max(
        candidate.incremental_value - chosen.incremental_value
        for candidate in candidates
    )
    return OwnershipAccessOutcome(
        regime=chosen.regime,
        owned_indices=chosen.owned_indices,
        owned_names=chosen.owned_names,
        ownership_size=chosen.size,
        platform_learning_value=(
            primitives.external_learning_efficiency
            * sum(sum(row) for row in primitives.learning)
        ),
        incremental_value=chosen.incremental_value,
        total_private_value=chosen.total_private_value,
        best_alternative_value=best_alternative,
        selection_margin=chosen.incremental_value - best_alternative,
        maximum_deviation_gain=max(0.0, deviation_gain),
        co_maximizing_subsets=co_maximizers,
        chosen=chosen,
        candidates=candidates,
    )


@dataclass(frozen=True)
class HomogeneousOwnershipAccessPrimitives:
    """Symmetric special case used for analytical platform-rollup boundaries.

    Two optional stress-test features default to the original model.

    ``fringe_customer_value_per_owned_asset`` (default zero) is relationship
    value with unmodeled outside customers put at risk per owned asset, so the
    full rollup is no longer conflict-free.

    ``learning_saturation`` (default ``None``) replaces the quadratic internal
    learning total ``gamma * n * (n - 1)`` with the firm-size chapter's
    saturating form ``n * L * (n - 1) / (kappa_L + n - 1)``, where ``kappa_L``
    is this parameter and ``L = gamma * (kappa_L + 1)`` so the two forms agree
    exactly at ``n = 2`` (both equal ``2 * gamma``) and the saturating total is
    strictly below the quadratic total for ``n >= 3``.
    """

    asset_count: int = 6
    internalization_advantage: float = 0.215
    directed_pair_learning: float = 0.105
    external_learning_efficiency: float = 0.55
    fixed_ownership_cost: float = 0.150
    organization_cost_scale: float = 0.100
    organization_cost_elasticity: float = 1.70
    pair_coordination_cost: float = 0.027
    neutrality_penalty: float = 0.25
    boundary_customer_value_per_unordered_pair: float = 0.020
    fringe_customer_value_per_owned_asset: float = 0.0
    learning_saturation: Optional[float] = None

    def validate(self) -> None:
        if isinstance(self.asset_count, bool) or not isinstance(self.asset_count, int):
            raise ValueError("asset_count must be an integer")
        if not 1 <= self.asset_count <= 20:
            raise ValueError("asset_count must lie between one and 20")
        finite = {
            "internalization_advantage": self.internalization_advantage,
            "directed_pair_learning": self.directed_pair_learning,
            "external_learning_efficiency": self.external_learning_efficiency,
            "fixed_ownership_cost": self.fixed_ownership_cost,
            "organization_cost_scale": self.organization_cost_scale,
            "organization_cost_elasticity": self.organization_cost_elasticity,
            "pair_coordination_cost": self.pair_coordination_cost,
            "neutrality_penalty": self.neutrality_penalty,
            "boundary_customer_value_per_unordered_pair": (
                self.boundary_customer_value_per_unordered_pair
            ),
            "fringe_customer_value_per_owned_asset": (
                self.fringe_customer_value_per_owned_asset
            ),
        }
        if any(not isfinite(value) for value in finite.values()):
            raise ValueError("homogeneous primitives must be finite")
        if self.learning_saturation is not None and (
            not isfinite(self.learning_saturation) or self.learning_saturation <= 0
        ):
            raise ValueError("learning_saturation must be positive when supplied")
        if not 0 <= self.external_learning_efficiency <= 1:
            raise ValueError("external_learning_efficiency must lie in [0, 1]")
        if self.organization_cost_elasticity < 1:
            raise ValueError("organization_cost_elasticity must be at least one")
        nonnegative = [
            self.directed_pair_learning,
            self.fixed_ownership_cost,
            self.organization_cost_scale,
            self.pair_coordination_cost,
            self.neutrality_penalty,
            self.boundary_customer_value_per_unordered_pair,
            self.fringe_customer_value_per_owned_asset,
        ]
        if any(value < 0 for value in nonnegative):
            raise ValueError("cost, learning, and customer terms cannot be negative")


def homogeneous_internal_learning_total(
    owned_size: int, primitives: HomogeneousOwnershipAccessPrimitives
) -> float:
    """Total internal directed learning among ``owned_size`` owned assets.

    With ``learning_saturation`` unset this is the quadratic benchmark total
    ``gamma * n * (n - 1)``.  With ``learning_saturation = kappa_L`` it is the
    firm-size chapter's saturating total ``n * L * (n - 1) / (kappa_L + n - 1)``
    with the calibration ``L = gamma * (kappa_L + 1)``.  Both totals equal
    ``2 * gamma`` at ``n = 2``; for ``n >= 3`` the saturating total is smaller
    by the factor ``(kappa_L + 1) / (kappa_L + n - 1) < 1``.
    """

    primitives.validate()
    if (
        isinstance(owned_size, bool)
        or not isinstance(owned_size, int)
        or not 0 <= owned_size <= primitives.asset_count
    ):
        raise ValueError("owned_size must lie between zero and asset_count")
    if owned_size <= 1:
        return 0.0
    gamma = primitives.directed_pair_learning
    if primitives.learning_saturation is None:
        return gamma * owned_size * (owned_size - 1)
    kappa = primitives.learning_saturation
    per_asset_learning_level = gamma * (kappa + 1.0)
    return (
        owned_size
        * per_asset_learning_level
        * (owned_size - 1)
        / (kappa + owned_size - 1)
    )


def homogeneous_candidate_increment(
    owned_size: int, primitives: HomogeneousOwnershipAccessPrimitives
) -> float:
    """Incremental value of owning ``owned_size`` symmetric assets."""

    primitives.validate()
    if (
        isinstance(owned_size, bool)
        or not isinstance(owned_size, int)
        or not 0 <= owned_size <= primitives.asset_count
    ):
        raise ValueError("owned_size must lie between zero and asset_count")
    if owned_size == 0:
        return 0.0
    internal_pairs = owned_size * (owned_size - 1)
    unordered_internal_pairs = internal_pairs / 2.0
    boundary_pairs = owned_size * (primitives.asset_count - owned_size)
    conflict_exposure = (
        primitives.boundary_customer_value_per_unordered_pair * boundary_pairs
        + primitives.fringe_customer_value_per_owned_asset * owned_size
    )
    return (
        owned_size * primitives.internalization_advantage
        + (1.0 - primitives.external_learning_efficiency)
        * homogeneous_internal_learning_total(owned_size, primitives)
        - primitives.fixed_ownership_cost
        - primitives.organization_cost_scale
        * owned_size**primitives.organization_cost_elasticity
        - primitives.pair_coordination_cost * unordered_internal_pairs
        - primitives.neutrality_penalty * conflict_exposure
    )


def homogeneous_optimal_ownership_size(
    primitives: HomogeneousOwnershipAccessPrimitives, *, tolerance: float = 1e-10
) -> int:
    """Exact optimal owned size in the symmetric benchmark.

    Ties resolve toward fewer acquisitions, matching ``solve_ownership_access``.
    This closed-form path is required when ``learning_saturation`` is set,
    because a fixed learning matrix cannot represent size-dependent learning.
    """

    primitives.validate()
    values = [
        homogeneous_candidate_increment(size, primitives)
        for size in range(primitives.asset_count + 1)
    ]
    best = max(values)
    for size, value in enumerate(values):
        if value >= best - tolerance:
            return size
    raise AssertionError("unreachable: maximum must be attained")


def platform_rollup_indifference_efficiency(
    primitives: HomogeneousOwnershipAccessPrimitives,
) -> Optional[float]:
    """Raw external-access efficiency where platform and full rollup tie.

    Values below zero mean the platform beats the full rollup throughout the
    feasible interval. Values above one mean the full rollup beats the platform
    throughout it. ``None`` means there is no cross-node learning, so access
    efficiency does not affect this comparison.

    The formula is exact under both optional stress-test features: with fringe
    customers the full rollup pays ``chi * fringe * m`` in conflict cost, and
    with saturating learning the rollup's learning total is the saturating one.
    """

    primitives.validate()
    size = primitives.asset_count
    total_learning = homogeneous_internal_learning_total(size, primitives)
    if total_learning == 0:
        return None
    full_cost = (
        primitives.fixed_ownership_cost
        + primitives.organization_cost_scale
        * size**primitives.organization_cost_elasticity
        + primitives.pair_coordination_cost * size * (size - 1) / 2.0
        + primitives.neutrality_penalty
        * primitives.fringe_customer_value_per_owned_asset
        * size
    )
    return (
        1.0 - (full_cost - size * primitives.internalization_advantage) / total_learning
    )


def hybrid_suppression_threshold(
    primitives: HomogeneousOwnershipAccessPrimitives,
) -> Optional[float]:
    """Smallest neutrality penalty that makes both pure modes dominate hybrids.

    The threshold is exact for the symmetric model at the supplied external
    learning efficiency. ``None`` means no finite penalty can work because the
    customer network has zero cross-boundary value and a hybrid strictly beats
    both endpoints.

    Without fringe customers both endpoints are conflict-free, so raising the
    penalty only hurts hybrids and the dominated region is a half-line; the
    closed form below is exact.  With fringe customers the full rollup also
    loses value in the penalty, so hybrids can overtake it again at higher
    penalties.  In that case the function returns the smallest penalty from
    which both pure modes dominate every hybrid for all weakly larger
    penalties, computed exactly from the piecewise-linear value crossings.
    """

    primitives.validate()
    size = primitives.asset_count
    if size <= 1:
        return 0.0
    current = HomogeneousOwnershipAccessPrimitives(
        **{**primitives.__dict__, "neutrality_penalty": 0.0}
    )
    values = [
        homogeneous_candidate_increment(owned_size, current)
        for owned_size in range(size + 1)
    ]
    boundary_value = primitives.boundary_customer_value_per_unordered_pair
    fringe = primitives.fringe_customer_value_per_owned_asset

    if fringe == 0:
        endpoint = max(values[0], values[size])
        required = 0.0
        for owned_size in range(1, size):
            excess = values[owned_size] - endpoint
            if excess <= 0:
                continue
            exposure = boundary_value * owned_size * (size - owned_size)
            if exposure == 0:
                return None
            required = max(required, excess / exposure)
        return required

    rollup_value = values[size]
    rollup_exposure = fringe * size

    def exposure(owned_size: int) -> float:
        return boundary_value * owned_size * (size - owned_size) + fringe * owned_size

    def dominated(chi: float, slack: float = 1e-9) -> bool:
        endpoint = max(0.0, rollup_value - chi * rollup_exposure)
        return all(
            values[owned_size] - chi * exposure(owned_size) <= endpoint + slack
            for owned_size in range(1, size)
        )

    # Every change in the domination indicator happens where a hybrid's value
    # line crosses an endpoint's value line or where the better endpoint
    # switches; collect those breakpoints and scan the constant intervals.
    breakpoints = {0.0}
    if rollup_value > 0:
        breakpoints.add(rollup_value / rollup_exposure)
    for owned_size in range(1, size):
        if values[owned_size] > 0:
            breakpoints.add(values[owned_size] / exposure(owned_size))
        slope = exposure(owned_size) - rollup_exposure
        if slope != 0:
            crossing = (values[owned_size] - rollup_value) / slope
            if crossing > 0:
                breakpoints.add(crossing)
    points = sorted(breakpoints)
    threshold: Optional[float] = 0.0
    probes = [(0.5 * (left + right), right) for left, right in zip(points, points[1:])]
    probes.append((points[-1] + 1.0, None))
    for probe, right in probes:
        if not dominated(probe):
            threshold = right
    return threshold


def homogeneous_network(
    primitives: HomogeneousOwnershipAccessPrimitives,
) -> OwnershipAccessPrimitives:
    """Build the matrix game corresponding exactly to the symmetric formulas.

    ``learning_saturation`` cannot be represented here: a fixed learning
    matrix implies internal learning quadratic in owned size, while the
    saturating benchmark makes it depend nonlinearly on subset size.  Use
    ``homogeneous_candidate_increment`` or ``homogeneous_optimal_ownership_size``
    for the saturating closed form; this function raises to avoid returning a
    silently different game.
    """

    primitives.validate()
    if primitives.learning_saturation is not None:
        raise ValueError(
            "learning_saturation makes internal learning depend on subset "
            "size, which a fixed learning matrix cannot represent; use the "
            "homogeneous closed-form functions instead"
        )
    size = primitives.asset_count
    nodes = tuple(
        NetworkNode(
            name=f"asset_{index + 1}",
            kind="asset",
            internalization_advantage=primitives.internalization_advantage,
        )
        for index in range(size)
    )
    learning = tuple(
        tuple(
            0.0 if row == column else primitives.directed_pair_learning
            for column in range(size)
        )
        for row in range(size)
    )
    customer = tuple(
        tuple(
            0.0
            if row == column
            else primitives.boundary_customer_value_per_unordered_pair / 2.0
            for column in range(size)
        )
        for row in range(size)
    )
    coordination = tuple(
        tuple(
            0.0 if row == column else primitives.pair_coordination_cost
            for column in range(size)
        )
        for row in range(size)
    )
    return OwnershipAccessPrimitives(
        nodes=nodes,
        learning=learning,
        customer_dependence=customer,
        coordination_cost=coordination,
        external_learning_efficiency=primitives.external_learning_efficiency,
        neutrality_penalty=primitives.neutrality_penalty,
        fixed_ownership_cost=primitives.fixed_ownership_cost,
        organization_cost_scale=primitives.organization_cost_scale,
        organization_cost_elasticity=primitives.organization_cost_elasticity,
        fringe_customer_value_per_owned_asset=(
            primitives.fringe_customer_value_per_owned_asset
        ),
    )


def empty_network(nodes: tuple[NetworkNode, ...]) -> OwnershipAccessPrimitives:
    """Convenience constructor for callers building matrices incrementally."""

    matrix = _zero_matrix(len(nodes))
    return OwnershipAccessPrimitives(
        nodes=nodes,
        learning=matrix,
        customer_dependence=matrix,
        coordination_cost=matrix,
    )


def vertical_customer_network(
    *,
    learning_topology: str = "complementary",
    external_learning_efficiency: float = 0.65,
    neutrality_penalty: float = 0.10,
) -> OwnershipAccessPrimitives:
    """Return a six-node example with reciprocal vertical customer links.

    The nodes are two clinics, two laboratories, and two payers.  In the
    ``complementary`` topology, learning is directed and especially valuable
    across clinic-lab links.  In the ``within_type`` counterfactual, exactly the
    same total learning weight is concentrated within the three node types.
    This holds aggregate learning fixed while changing its topology.
    """

    if learning_topology not in {"complementary", "within_type"}:
        raise ValueError("learning_topology must be complementary or within_type")
    nodes = (
        NetworkNode("clinic_east", "clinic", 0.18),
        NetworkNode("clinic_west", "clinic", 0.16),
        NetworkNode("lab_east", "lab", 0.14),
        NetworkNode("lab_west", "lab", 0.12),
        NetworkNode("payer_east", "payer", -0.03),
        NetworkNode("payer_west", "payer", -0.05),
    )
    size = len(nodes)
    directed_learning = {
        ("clinic", "clinic"): 0.04,
        ("lab", "lab"): 0.05,
        ("payer", "payer"): 0.03,
        ("clinic", "lab"): 0.13,
        ("lab", "clinic"): 0.18,
        ("clinic", "payer"): 0.12,
        ("payer", "clinic"): 0.10,
        ("lab", "payer"): 0.08,
        ("payer", "lab"): 0.06,
    }
    complementary = tuple(
        tuple(
            0.0
            if source == target
            else directed_learning[(nodes[source].kind, nodes[target].kind)]
            * (1.30 if source % 2 == target % 2 else 0.75)
            for target in range(size)
        )
        for source in range(size)
    )
    if learning_topology == "complementary":
        learning = complementary
    else:
        total_learning = sum(sum(row) for row in complementary)
        within_type_edges = sum(
            1
            for source in range(size)
            for target in range(size)
            if source != target and nodes[source].kind == nodes[target].kind
        )
        within_weight = total_learning / within_type_edges
        learning = tuple(
            tuple(
                within_weight
                if source != target and nodes[source].kind == nodes[target].kind
                else 0.0
                for target in range(size)
            )
            for source in range(size)
        )

    directed_customer_value = {
        ("clinic", "lab"): 0.08,
        ("payer", "clinic"): 0.10,
        ("lab", "payer"): 0.06,
    }
    customer = tuple(
        tuple(
            0.0
            if source == target
            else directed_customer_value.get(
                (nodes[source].kind, nodes[target].kind), 0.005
            )
            * (1.0 if source % 2 == target % 2 else 0.35)
            for target in range(size)
        )
        for source in range(size)
    )
    coordination = tuple(
        tuple(
            0.0
            if source == target
            else (0.008 if nodes[source].kind == nodes[target].kind else 0.025)
            for target in range(size)
        )
        for source in range(size)
    )
    return OwnershipAccessPrimitives(
        nodes=nodes,
        learning=learning,
        customer_dependence=customer,
        coordination_cost=coordination,
        external_learning_efficiency=external_learning_efficiency,
        neutrality_penalty=neutrality_penalty,
        fixed_ownership_cost=0.16,
        organization_cost_scale=0.065,
        organization_cost_elasticity=1.65,
    )
