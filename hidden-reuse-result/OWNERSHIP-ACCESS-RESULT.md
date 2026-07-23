# Result III: When a Learning Network Becomes a Platform or a Firm

## Abstract

The earlier models in this package establish why an AI-context relationship may
move inside a firm and, under homogeneous assets, how many assets an integrated
firm should own. They leave open a fundamental alternative: a common AI
intermediary may learn across independent customers without owning them.

This note makes ownership and customer access substitutes in one heterogeneous,
directed learning network. It establishes three results. First, ownership gains
only the part of cross-node learning that arm's-length access cannot deliver.
Second, customer relationships that are endangered by partial ownership suppress
hybrid structures and can create a discontinuous switch between a neutral
platform and a full rollup. Third, total learning opportunity is insufficient to
predict firm boundaries: holding aggregate learning fixed, changing which types
learn from which other types can change both the assets acquired and whether any
acquisition occurs.

The implementation exactly enumerates all ownership subsets in two six-node
benchmarks and verifies that the selected subset has no profitable acquisition
deviation. The phase maps and robustness draws are calibrated theoretical
computations, not empirical evidence.

## 1. Why customer access is a distinct governance technology

The homogeneous size model assumes useful learning transfers only among assets
under common ownership. That is one polar case. At the other extreme, an AI
intermediary may serve independent firms, obtain permission to learn from their
interactions, and apply the result across its customer network.

Call this second arrangement a **platform**: the intermediary coordinates
learning while the operating assets remain independently owned. The distinction
is not where the server sits. It is whether useful cross-node learning requires a
common owner.

This framing is related to three established literatures but asks a narrower
question than each. Hagiu and Wright compare multi-sided platforms with vertical
integration as alternative allocations of control rights and coordination
([2015 working paper](https://www.hbs.edu/ris/Publication%20Files/15-037_cb5afe51-6150-4be9-ace2-39c6a8ace6d4.pdf)).
Their later work distinguishes learning across users from learning within a user
([2023](https://onlinelibrary.wiley.com/doi/abs/10.1111/1756-2171.12453)).
Bolton and Whinston show why integration in a multilateral supply setting must be
understood in the entire production and distribution network
([1993](https://academic.oup.com/restud/article-abstract/60/1/121/1575987)).
The model below combines those concerns in a minimal ownership-versus-access
calculation.

## 2. Heterogeneous directed network

There are $N$ context-generating operating assets. One intermediary initially
serves all of them as independent customers and may acquire a subset
$S\subseteq N$.

Each node $i$ has a direct internalization advantage $a_i$. This is the net
private gain from moving that node inside the intermediary after compensating its
owner for remaining independent. It can be derived from the bilateral
hidden-reuse game or supplied directly.

Learning is directed. Let

\[
\gamma_{ij}\ge 0
\]

be the value of learning generated at node $i$ when applied at node $j$.
There is no requirement that $\gamma_{ij}=\gamma_{ji}$, and nodes may have
different types.

Let $q\in[0,1]$ be **external learning efficiency**: the fraction of all
cross-node learning that the intermediary can lawfully, technically, and
commercially realize while the nodes remain independent customers. Thus:

- $q=1$: customer access transmits learning as effectively as ownership;
- $q=0$: cross-node learning is available only inside a common firm.

The parameter rolls together data permissions, contractibility, privacy
technology, interoperability, and the intermediary's ability to apply learning
across customers. It is not covert reuse. Hidden reuse instead contributes to
the direct terms $a_i$ by making market contracting less valuable.

The operating nodes can also buy from, sell to, or otherwise depend on one
another. Let $d_{ij}\ge0$ be the value of the directed customer relationship
from $i$ to $j$. Partial ownership can make a formerly neutral intermediary a
competitor, raise foreclosure concerns, or induce an outside node to withhold
business. Let $\chi\ge0$ be the share or intensity of cross-boundary customer
value thereby placed at risk.

The cost of owning $S$ is

\[
C(S)=K\mathbf 1\{S\ne\varnothing\}
     +c|S|^\rho
     +\sum_{i<j;\ i,j\in S}h_{ij},
\qquad \rho\ge1,
\]

where $K$ is a fixed acquisition/AI-system cost, $c|S|^\rho$ is organization
cost, and $h_{ij}$ is pair-specific coordination difficulty.

## 3. Private acquisition value

As a neutral platform, the intermediary realizes

\[
P(q)=q\sum_{i\ne j}\gamma_{ij}.
\]

Ownership upgrades learning on edges whose endpoints are both owned from $q$
to one. Relative to remaining a platform, acquiring $S$ therefore produces

\[
\boxed{
\Delta(S)=
\sum_{i\in S}a_i
+(1-q)\sum_{i,j\in S;\ i\ne j}\gamma_{ij}
-C(S)
-\chi\sum_{i,j}d_{ij}
  \mathbf 1\{\mathbf 1(i\in S)\ne\mathbf 1(j\in S)\}.
}
\tag{1}
\]

The last term is a directed ownership-boundary cut. It permits vertical chains,
reciprocal trade, and customer cycles. It vanishes for a pure platform
$S=\varnothing$ and a full rollup $S=N$, but can make partial integration
costly.

That the cut vanishes at $S=N$ is a closed-network artifact, not an economic
result: the model contains every customer the intermediary could ever own.  A
real intermediary that rolls up all of its modeled customers still serves
outside customers it can never acquire, and those relationships are put at
risk by ownership just as boundary-crossing internal ones are.  The
implementation therefore takes an optional fringe term
$f\ge0$ (``fringe_customer_value_per_owned_asset``, default zero): each owned
asset adds $f$ to boundary customer exposure, so the conflict cost of any
subset becomes $\chi[\text{cut}(S)+f|S|]$ and the full rollup is no longer
automatically conflict-free.  Section 8 stress-tests the polarization result
against this term.

The intermediary chooses

\[
S^*\in\arg\max_{S\subseteq N}\Delta(S).
\tag{2}
\]

Ties are reported in full and resolved toward fewer acquisitions. Because
offers are assumed to compensate acquired owners for their independent
fallbacks, (2) is a reduced-form, single-intermediary acquisition equilibrium.
It is a private-value benchmark, not a welfare optimum or a general equilibrium
of rival platforms.

## 4. Ownership-access substitution

Define internal learning in a candidate subset as

\[
\Gamma(S)=\sum_{i,j\in S;\ i\ne j}\gamma_{ij}.
\]

### Proposition 1

For every ownership subset $S$,

\[
\frac{\partial\Delta(S)}{\partial q}=-\Gamma(S)\le0.
\]

Consequently, the maximum incremental value of ownership is weakly decreasing
in external learning efficiency. If the neutral platform is optimal at some
$q_0$, it remains optimal for every $q\ge q_0$, holding the other primitives
fixed.

### Proof

Only the learning-upgrade term in (1) depends on $q$, which gives the
derivative. The platform option always has value zero relative to itself. Every
nonempty candidate's value weakly falls as $q$ rises, so none can overtake a
platform that was already optimal. $\square$

The proposition does not claim that selected ownership size is monotone in an
arbitrary heterogeneous network. Different subsets can cross as $q$ changes.
It establishes the sharper object the thesis needs: ownership has a learning
advantage only to the extent that customer access fails to reproduce it.

## 5. Analytical platform-rollup boundary

To expose the boundary, specialize to $m$ symmetric assets. Each node has
direct advantage $a$, every directed pair has learning value $\gamma$, every
owned unordered pair costs $h$ to coordinate, and every unordered customer
relationship crossing the ownership boundary has value $b$. If $n$ assets
are owned, incremental value is

\[
\Delta_n(q,\chi)=
na+(1-q)\gamma n(n-1)
-K-cn^\rho
-\frac h2n(n-1)
-\chi b n(m-n)
\tag{3}
\]

for $n>0$, with $\Delta_0=0$.

The full rollup and platform both have no ownership-boundary customer loss. They
are indifferent at

\[
\boxed{
q^*=1-
\frac{K+cm^\rho+\frac h2m(m-1)-ma}
     {\gamma m(m-1)}.
}
\tag{4}
\]

If $q^*\in(0,1)$, the full rollup beats the platform for $q<q^*$, and the
platform beats it for $q>q^*$. Values outside that interval mean one endpoint
dominates throughout feasible $q$.

A caution about functional form: the internal learning total
$\gamma n(n-1)$ in (3) is convex in $n$, and convex benefits mechanically
favor corner solutions.  The package's own firm-size chapter argues instead
that per-asset learning saturates, using the form $L(n-1)/(\kappa_L+n-1)$.
The implementation therefore accepts an optional ``learning_saturation``
parameter $\kappa_L$ that replaces the quadratic total with the saturating
total $nL(n-1)/(\kappa_L+n-1)$, calibrated by $L=\gamma(\kappa_L+1)$ so the
two forms agree exactly at $n=2$ (both equal $2\gamma$) and the saturating
total is strictly smaller for $n\ge3$ by the factor
$(\kappa_L+1)/(\kappa_L+n-1)$.  The default (no saturation) reproduces (3)
exactly.  Because a fixed learning matrix cannot represent size-dependent
learning, the saturating case is solved through the exact per-size closed
form rather than the matrix game; both thresholds (4) and (5) are computed
under whichever learning total is active, and (4) additionally subtracts the
rollup's fringe conflict cost $\chi f m$ when $f>0$.

## 6. Customer conflict creates organizational polarization

Let $R_n(q)=\Delta_n(q,0)$ and define the better pure-mode value

\[
M(q)=\max\{0,R_m(q)\}.
\]

For $b>0$, define

\[
\boxed{
\chi^*(q)=
\max_{1\le n<m}
\frac{[R_n(q)-M(q)]_+}{b n(m-n)}.
}
\tag{5}
\]

### Proposition 2

If $\chi\ge\chi^*(q)$, a pure mode is a global maximizer. If
$\chi>\chi^*(q)$, no partial ownership structure ties the better pure mode, and
the package's selected equilibrium is therefore:

\[
S^*=
\begin{cases}
N, & q<q^*,\\
\varnothing, & q\ge q^*,
\end{cases}
\]

with the package's smaller-ownership tie rule at $q=q^*$. At
$\chi=\chi^*(q)$, a partial structure can tie an endpoint; the implementation
reports every such co-maximizer.

### Proof

For every $1\le n<m$, equation (5) implies

\[
R_n(q)-\chi b n(m-n)\le M(q).
\]

Thus a partial structure cannot exceed the better endpoint. A strict inequality
in $\chi$ makes every positive-exposure partial structure strictly worse.
Equation (4) ranks the endpoints. $\square$

This is the first new conclusion created by allowing firms to be one another's
customers. Customer links do not mechanically favor separation or integration.
They penalize the boundary of a partially integrated intermediary. Strong
enough conflict removes the middle: as access efficiency crosses $q^*$, the
intermediary can jump from owning the whole learning network to owning none of
it.

Two specification choices do part of this proposition's work, and it is
important to say so plainly.  First, the full rollup escapes conflict cost
only because the network is closed: with unmodeled outside customers
($f>0$), $S=N$ bears $\chi f m$ and the endpoints are no longer both
conflict-free, so (5) no longer applies as written.  The implementation
generalizes the threshold exactly for that case: because raising $\chi$ then
also drags the rollup down, hybrids can overtake it again at higher
penalties, and the reported threshold is the smallest $\chi$ from which both
pure modes dominate every hybrid for all weakly larger penalties, computed
from the piecewise-linear value crossings.  Second, the quadratic learning
total in (3) rewards the corner $n=m$ disproportionately; under the
firm-size chapter's saturating form the middle is much harder to remove.
Section 8 quantifies both effects at the polarization anchor.

This mechanism echoes foreclosure concerns in vertical-integration theory
([Hart and Tirole 1990](https://ceepr.mit.edu/workingpaper/vertical-integration-and-market-foreclosure-2/)),
but the modeled cost is broader: an independent customer may leave or reduce
information sharing because the intermediary now owns a business that competes
with it. Gawer's distinction among platform scope, customer sides, and data
interfaces is especially relevant here
([2020](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3702057)).

## 7. Heterogeneous topology, not aggregate data, sets the boundary

Equation (1) is a weighted-subgraph problem. Node weights $a_i$ reward direct
ownership; internal directed edges $\gamma_{ij}$ reward putting particular
pairs together; coordination edges $h_{ij}$ discourage difficult combinations;
and customer edges $d_{ij}$ penalize a cut through valuable relationships.

It follows immediately that neither the number of records nor

\[
\Gamma(N)=\sum_{i\ne j}\gamma_{ij}
\]

is a sufficient statistic for firm boundaries. The location and direction of
the learning edges matter.

The computed counterexample uses two clinics, two laboratories, and two payers.
It holds all node values, customer links, costs, $q=0.85$, $\chi=0.10$, and
total learning weight (2.927) fixed. It changes only the learning topology:

| Learning topology | Exact ownership equilibrium |
|---|---|
| Learning dispersed across complementary vertical links | Neutral platform |
| Same total learning concentrated within node types | Own both clinics |

![Equal aggregate learning with different firm boundaries](outputs/ownership-access-topology.svg)

The example is not an empirical calibration. Its purpose is constructive: it
disproves the proposition that aggregate transferable learning alone determines
firm scope.

## 8. Computational evidence

The analytical symmetric calibration uses six assets and yields

\[
q^*=0.5657.
\]

At $q=0.55$, a partial rollup is eliminated once $\chi$ exceeds \(0.0800\),
after which the full rollup wins. At $q=0.60$, the corresponding threshold is
(0.1039), after which the platform wins. The heterogeneous vertical network
has a pure-mode indifference point of (0.5853).

![Ownership versus customer access phase maps](outputs/ownership-access-regime-map.svg)

The dashed line is the platform/full-rollup indifference point. At the top of
each panel, customer conflict makes the line an actual all-or-nothing ownership
switch. Near the bottom, partial ownership survives. Heterogeneity makes that
middle region much larger and changes its composition.

For every grid cell, the solver evaluates all (2^6=64) ownership subsets,
reports all maximizers, and calculates the gain from the best unchosen subset.
That gain is zero by construction and is asserted in tests. This is an
equilibrium deviation check, not a claim that stable colors alone prove an
equilibrium.

### Stress test: open networks and saturating learning

The polarization anchor is the symmetric calibration above ($m=6$,
$a=0.215$, $\gamma=0.105$, $K=0.15$, $c=0.1$, $\rho=1.7$, $h=0.027$,
$b=0.02$) at the high-conflict level $\chi=0.8$ used by the robustness
anchors, with $q$ swept over $[0,1]$ (2,001 grid points, switch points then
refined by bisection).  Four cases: baseline; fringe conflict on with
$f=0.02$, the value of one boundary customer link per owned asset;
saturating learning on with $\kappa_L=4$, the firm-size chapter's baseline
(so $L=0.525$ and the rollup's internal learning total falls from $3.15$ to
$1.75$); and both.

| Case | $q^*$ | Optimal size along the $q$ sweep | All-or-nothing? |
|---|---|---|---|
| Baseline | 0.5657 | 6 for $q<q^*$, 0 after | Yes |
| Fringe $f=0.02$ | 0.5352 | 6 for $q<q^*$, 0 after | Yes |
| Saturating $\kappa_L=4$ | 0.2182 | 6, then 5 at 0.0846, 4 at 0.1952, 0 at 0.2938 | No |
| Both | 0.1634 | 6, then 5 at 0.0480, 4 at 0.1564, 0 at 0.2227 | No |

Fringe conflict alone does not break polarization; it just moves and taxes
it.  The rollup now pays $\chi f m=0.096$, shifting the switch from
$q^*=0.5657$ to $0.5352$, but with $f=b$ every partial owner of $n\ge2$
assets still has exposure $bn(m-n)+fn>fm$, so conflict continues to punish
the middle harder than the ends: the best partial structure trails the
better endpoint by at least $0.071$ at every $q$ (baseline: $0.055$), and
the generalized suppression threshold peaks at $\chi^*=0.195$, well below
$0.8$.  The matrix game with the fringe term reproduces the closed form and
the same switch exactly.

Saturating learning breaks polarization at this conflict level.  With
$\kappa_L=4$ the all-or-nothing switch disappears: partial rollups are
strictly optimal for $q\in(0.085,0.294)$, stepping down $6\to5\to4\to0$ as
access improves, and the best partial beats the better endpoint by up to
$0.068$ (at $q=0.218$, the new $q^*$).  Adding the fringe term shrinks but
does not close the interior band ($q\in(0.048,0.223)$, peak advantage
$0.053$).  Restoring all-or-nothing under saturation would require
$\chi\ge1.37$ (or $1.25$ with the fringe term), more than an order of
magnitude above the $0.080$--$0.104$ thresholds reported above for the
quadratic model.

The honest summary: the discontinuous platform/rollup switch of Proposition
2 is genuine but not free.  It survives opening the network to fringe
customers of comparable value to modeled links, because a boundary that
cuts through the modeled network still creates more conflict than one that
surrounds it.  It does not survive replacing the convex learning total with
the saturating form the package itself uses for firm size, except at
implausibly high conflict intensities: with saturating learning, high
customer conflict compresses rather than eliminates partial ownership.
Polarization should therefore be read as conditional on learning economies
that keep compounding at the largest subset sizes.

The robustness exercise perturbs every directed learning edge, every customer
edge, node-level internalization advantages, and organization cost. It then
resolves the exact subset problem under common scenario definitions. The fixed
seed and all probabilities are in
[`outputs/ownership-access-robustness.csv`](outputs/ownership-access-robustness.csv).
Across 600 draws, the low-access/high-conflict anchor selects a full rollup in
98.8 percent of draws; the intermediate-access/low-conflict anchor selects a
cross-type partial rollup in 97.3 percent; and the high-access/high-conflict
anchor selects a neutral platform in 100 percent. These are local robustness
frequencies under stated perturbations, not estimated market probabilities.
These draws show whether the illustrated regimes survive nearby synthetic
heterogeneity; they do not measure uncertainty about the real economy.

## 9. What the result adds to the earlier work

The package now separates four questions:

1. **Can hidden learning be deterred or priced?** The bilateral game determines
   whether one relationship remains modular.
2. **If assets are homogeneous and learning requires ownership, what size is
   viable?** The free-formation game supplies a scale target.
3. **Can customer access transmit the same learning?** If yes, learning economies
   can support a platform rather than a rollup.
4. **Which assets belong together?** The directed learning and customer networks,
   not aggregate context volume, select the boundary.

The concise contribution is:

> Learning economies predict large integrated AI firms only when useful
> learning cannot travel through arm's-length customer relationships; when it
> can, the same economies support a platform, and when partial ownership
> threatens remaining customer ties, equilibrium can jump between those two
> forms.

This statement is conditional on equal private monetization of learning under
customer access and ownership. [Result IV](APPROPRIATION-RESULT.md) introduces
separate platform and owner capture shares. It shows that ownership can remain
privately optimal at (q=1) and that incoming customer learning can complement
selective ownership when its value lands at owned operations.

## 10. Limits and next tests

The result is complete for the stated single-intermediary game, but deliberately
does not claim more.

- There is one potential acquirer. Competing platforms could bid for nodes,
  split the network, or use exclusivity.
- $q$ and $\chi$ are exogenous. A richer model would let the intermediary
  invest in confidential learning infrastructure and let customers choose how
  much context to expose.
- Customer loss is reduced form. Prices, demand substitution, foreclosure, and
  customer exit are not separately modeled.
- Acquisition transfers are summarized in $a_i$; wealth constraints and
  bargaining over acquisition prices are omitted.
- The solution is private-value maximizing and need not be socially efficient.
- Capability accumulates only through the reduced-form learning weights; the
  game is not dynamic.
- Exact enumeration is capped at twenty nodes. Larger empirical networks would
  require mixed-integer optimization or approximation with certified bounds.

The sharp empirical object is not merely whether an acquisition creates “more
data.” It is the task-level transfer matrix: does learning produced at node
$i$ improve decisions at node $j$, can that transfer occur while the firms
remain independent, and do outside customers retreat when the intermediary owns
their competitors? Those three measurements distinguish a rollup mechanism from
a platform mechanism.
