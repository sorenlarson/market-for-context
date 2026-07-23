# Result IV: Access Is Not Appropriation

## Abstract

The ownership-access model asks whether an AI intermediary can learn across
independent customers as effectively as it can learn across owned operations.
That model implicitly assumes that learning value is equally monetizable under
both organizations. This note relaxes that assumption.

An independent AI provider may create operating value that its customer
privately observes but cannot credibly promise to share. The provider earns a
service price; an owner receives the operating cash flow left after costs. We
separate those two claims with a platform capture share and an owner retained
share. The resulting private acquisition value has an exact decomposition into
a **capture upgrade** on value already producible through customer access and a
**productive learning upgrade** available only inside the ownership boundary.

Three results follow. First, ownership can dominate even when independent
customer relationships transmit all useful learning. Second, customer access
and partial ownership can become complements: outside customers supply learning
while owned businesses become the places where its value is monetized. Third,
customer conflict can eliminate this hybrid and restore the platform-versus-full
rollup polarization derived in the earlier model.

The implementation exactly enumerates every ownership subset and supplies a
Pareto single-price benchmark connecting task-value dispersion to provider
capture. Figures and sensitivity draws are calibrated theoretical computations,
not empirical evidence.

## 1. The missing assumption in the ownership-access result

The previous result defined \(q\in[0,1]\) as the fraction of cross-business
learning achievable while operating assets remain independent customers. It
showed that ownership has a productive learning advantage only over the fraction
\(1-q\).

That conclusion was conditional on a strong monetization assumption. The
intermediary was treated as if one unit of learning generated one unit of
private value regardless of whether the learning improved a customer's
operation or an operation the intermediary owned.

The distinction matters whenever:

1. the customer observes the realized operating benefit more accurately than
   the provider;
2. that benefit is difficult to verify in a contract;
3. a common service price is constrained by the customer's ability to switch,
   self-provide, or conceal its surplus; and
4. ownership gives the acquirer a claim on operating cash flow without requiring
   an ex-post invoice for the value caused by AI.

This is a private-value mechanism. In a frictionless transferable-utility world,
the seller or customer could collect the entire expected gain through the
service or acquisition price, and value capture alone would not determine the
firm boundary. The result below therefore concerns incomplete pricing and
contracting, not a claim that changing ownership mechanically creates social
surplus.

## 2. A Pareto task-pricing benchmark

The pricing input is motivated by Soren Larson's
[“A Complexity Theory of AI Value Accrual”](https://hypersoren.xyz/posts/price-elasticity/).
Let task value \(v\) have a Pareto distribution:

\[
\Pr(v\ge z)=\left(\frac{x_m}{z}\right)^\alpha,
\qquad z\ge x_m,\quad \alpha>1.
\]

A provider with marginal cost \(c\) posts one price \(r\) before seeing task
value. When the interior solution is above the minimum task value, the optimal
price is

\[
r^*=\frac{\alpha}{\alpha-1}c.
\]

Under the normalization \(x_m=c\), provider profit and customer surplus imply
the provider capture share

\[
\boxed{
p(\alpha)=
\frac{\text{provider profit}}
     {\text{provider profit}+\text{customer surplus}}
=\frac{\alpha-1}{2\alpha-1}.
}
\tag{1}
\]

At \(\alpha=1.5\), the provider captures 25 percent of the net surplus produced
on served tasks. Customers retain 75 percent. The exact implementation also
calculates tasks excluded by the common markup: with \(x_m=c=1\), integrated
operation produces normalized surplus 2.000, while monopoly pricing produces
1.540 across provider and served customers, leaving a deadweight loss of 0.460.

Equation (1) is a benchmark, not a universal law. Competition, nonlinear
contracts, task-specific prices, observability, and bargaining can all change
the provider share. The network result therefore treats the capture share as a
primitive and uses (1) only to translate selected values into a task-tail
interpretation.

## 3. A directed learning-and-value network

There are \(N\) context-generating operating assets. One AI intermediary begins
as a neutral provider serving every asset and may acquire a subset
\(S\subseteq N\).

The learning and customer primitives are inherited from the ownership-access
model:

- \(\gamma_{ij}\ge0\) is the value of learning generated at node \(i\) when
  applied at node \(j\);
- \(q\in[0,1]\) is the fraction of that learning available through lawful,
  contractible customer access;
- \(a_j\) is node \(j\)'s direct internalization advantage, net of its
  independent fallback;
- \(C(S)\) includes fixed ownership, organization, and pair-specific
  coordination costs; and
- \(\chi D(\partial S)\) is customer value placed at risk when partial ownership
  cuts buyer-supplier relationships.

The new primitives are:

- \(b_j\ge0\): AI-enabled operating surplus generated at node \(j\), before it
  is divided between provider and operator;
- \(p\in[0,1]\): the share of customer-side value captured by the platform
  through service prices; and
- \(o\in[0,1]\): the share of operating value retained by the acquirer under
  ownership, after acquisition-price capitalization, seller bargaining, and
  product-market pass-through.

The owner share \(o\) need not equal one. That restriction prevents the result
from assuming away the acquisition-price question.

The direct term \(a_j\) and the operating-surplus term \(b_j\) must be
calibrated to distinct gains. In this package, \(a_j\) carries the bilateral
hidden-reuse contracting advantage, while \(b_j\) carries ordinary operating
value whose private recipient changes with governance. Loading the same gain
into both would double count the case for ownership.

### Deriving both shares from one pledgeability friction

The wedge \(o-p\) drives every capture result below, so it should not enter as
a free calibration. The package derives both shares from the same
pledgeable-payment logic used in the bilateral extension, where a party
charging for value realized later collects only what its counterparty commits
before realization plus the share a court, auditor, or payment system can
verify afterward.

The two capture markets place that friction on opposite sides.

In the **service market**, the intermediary is the charging party. A customer
observes its own avoided mistakes better than the provider does, so the
provider collects an ex-ante commitment \(w_s\) plus the ex-post verifiable
share \(\phi_s\) of realized value:

\[
p=\min\{1,\;w_s+\phi_s\}.
\]

In the **market for corporate control**, the seller is the charging party. It
capitalizes into the acquisition price only the pledgeable share of
prospective AI gains, weighted by its bargaining position
\(\beta_a\in[0,1]\); downstream competition then passes through a further
share \(\lambda\in[0,1]\) of what remains:

\[
o=\bigl(1-\beta_a\min\{1,\;w_a+\phi_a\}\bigr)(1-\lambda).
\]

Weak verifiability therefore *lowers* \(p\) and *raises* \(o\): the same
friction that stops a provider from billing realized customer value also stops
a seller from charging for gains the buyer will realize later.

Under fully symmetric frictions—\(w_a=w_s=w\), \(\phi_a=\phi_s=\phi\),
\(\beta_a=1\), \(\lambda=0\)—the wedge is

\[
o-p=1-2(w+\phi),
\]

which is positive exactly when the pledgeable share of AI-created value is
below one half. This mirrors the bilateral comparative static in which
capability improvements enlarge the unpledgeable remainder faster than the
enforceable payment whenever \(\phi<1/2\). The assumption \(o>p\) used in the
displayed calibrations is thereby restated as a falsifiable claim: the market
for corporate control verifies prospective AI gains no better than the service
market verifies realized ones. If diligence, earn-outs, and seller bargaining
capitalize most expected gains—or if metering and outcome-contingent service
contracts improve—the wedge shrinks or reverses, and the capture case for
ownership disappears with it.

The baseline calibration is reproduced exactly by \(w_s=0.10\),
\(\phi_s=0.15\) (so \(p=0.25\)) and \(\beta_a=1\), \(w_a=0.15\),
\(\phi_a=0.40\), \(\lambda=0\) (so \(o=0.45\)). The derivation is implemented
by `CaptureShareFrictions` and `derive_capture_shares` in
[`src/hidden_reuse/appropriation.py`](src/hidden_reuse/appropriation.py);
`with_derived_capture_shares` feeds the derived shares into the subset solver.

For a candidate subset, define:

\[
B(S)=\sum_{j\in S}b_j,
\]

\[
\Gamma_I(S)=
\sum_{i\in S}\sum_{j\in S,\,j\ne i}\gamma_{ij},
\]

and

\[
\Gamma_X(S)=
\sum_{i\notin S}\sum_{j\in S}\gamma_{ij}.
\]

\(\Gamma_I\) is learning whose source and destination are both owned.
\(\Gamma_X\) is learning imported from outside customers into owned operations.
Direction is essential: learning that lands at an owned node affects the
acquirer's operating return; learning delivered to an independent customer
remains subject to the platform pricing constraint.

## 4. Exact private-value decomposition

As a neutral platform, the intermediary captures

\[
V_P=p\left[
\sum_j b_j+q\sum_{i\ne j}\gamma_{ij}
\right].
\tag{2}
\]

If it owns \(S\), it receives owner-side returns on value landing at nodes in
\(S\). Internal learning rises from \(q\Gamma_I(S)\) to \(\Gamma_I(S)\), while
learning imported from outside customers remains \(q\Gamma_X(S)\). Subtracting
(2) gives:

\[
\boxed{
\begin{aligned}
\Delta(S)=
&\sum_{j\in S}a_j \\
&+(o-p)\left[B(S)+q\bigl(\Gamma_I(S)+\Gamma_X(S)\bigr)\right] \\
&+o(1-q)\Gamma_I(S) \\
&-C(S)-\chi D(\partial S).
\end{aligned}
}
\tag{3}
\]

The second line is the **capture upgrade**. It applies to value that customer
access could already produce but the service price could not fully appropriate.
The third line is the **productive learning upgrade**. It applies only to
learning that common ownership makes newly available.

The intermediary chooses

\[
S^*\in\arg\max_{S\subseteq N}\Delta(S).
\tag{4}
\]

The computation reports all ties and tests every ownership subset. As in the
earlier network result, this is an exact single-intermediary acquisition
equilibrium after reduced-form compensation of acquired owners. It is not a
general equilibrium of competing acquirers.

### Proposition 1: the previous model is nested

If \(o=p=1\), equation (3) becomes

\[
\Delta(S)=
\sum_{j\in S}a_j
+(1-q)\Gamma_I(S)
-C(S)-\chi D(\partial S),
\]

which is exactly the earlier ownership-access model. Thus the new mechanism is
an extension rather than a replacement.

### Proposition 2: stronger platform appropriation discourages ownership

For every nonempty candidate subset,

\[
\frac{\partial\Delta(S)}{\partial p}
=-\left[B(S)+q\bigl(\Gamma_I(S)+\Gamma_X(S)\bigr)\right]\le0.
\tag{5}
\]

Consequently, if the neutral platform is optimal at capture share \(p_0\), it
remains optimal for every \(p\ge p_0\), holding other primitives fixed.

This is the appropriation counterpart to the earlier access result: providers
that can charge for more of the value they create need less ownership.

## 5. Customer access can complement selective ownership

Differentiating a fixed candidate with respect to external learning efficiency
gives

\[
\boxed{
\frac{\partial\Delta(S)}{\partial q}
=(o-p)\Gamma_X(S)-p\Gamma_I(S).
}
\tag{6}
\]

### Proposition 3

Customer access increases the value of owning \(S\) exactly when

\[
(o-p)\Gamma_X(S)>p\Gamma_I(S).
\tag{7}
\]

The left side is the capture improvement on learning imported from independent
customers and monetized at owned destinations. The right side is the platform's
improved ability to monetize learning on edges that ownership would otherwise
internalize.

For a full rollup, \(\Gamma_X(N)=0\), so (6) becomes
\(-p\Gamma_I(N)\le0\): customer access and full ownership remain substitutes.
For a single destination node, \(\Gamma_I=0\). If \(o>p\) and incoming learning
is valuable, customer access strictly increases the case for selective
ownership.

This reverses the global monotonicity of the earlier model. Better external
learning no longer implies weakly less ownership in every network. It can
produce a hybrid organization that serves outside customers as learning sources
and owns the operations where the resulting value is realized.

### Exact two-node counterexample

Let one independent customer generate learning of value one for one operating
target. Set \(o=0.8\), \(p=0.2\), fixed ownership cost \(0.05\), and no direct
operating surplus. Owning only the target has value

\[
\Delta(\{\text{target}\})=0.6q-0.05.
\]

At \(q=0\), the platform is optimal. At \(q=1\), owning the target produces
incremental private value \(0.55\). A coordination cost of \(0.8\) on owning
both nodes rules out the full rollup in both cases. Greater independent-customer
access therefore changes the exact equilibrium from a platform to selective
ownership even though selective ownership unlocks no extra learning.

## 6. Pure platform-versus-rollup boundary

For \(m\) symmetric assets, let each node have operating surplus \(b\), direct
advantage \(a\), and each directed pair learning value \(\gamma\). Define

\[
B=mb,
\qquad
\Gamma=\gamma m(m-1),
\]

and full-rollup cost

\[
C_m=K+cm^\rho+\frac h2m(m-1).
\]

The pure organizations have private values

\[
V_P=p(B+q\Gamma)
\tag{8}
\]

and

\[
V_R=ma+o(B+\Gamma)-C_m.
\tag{9}
\]

They are indifferent at

\[
\boxed{
p^*(q)=
\frac{ma+o(B+\Gamma)-C_m}{B+q\Gamma}.
}
\tag{10}
\]

Below \(p^*(q)\), the full rollup beats the platform; above it, the platform
beats the full rollup. Higher \(q\) lowers the capture share the platform needs
to compete because it raises the productive value available without ownership.

At complete external learning, \(q=1\), ownership still wins precisely when

\[
\boxed{
(o-p)(B+\Gamma)+ma>C_m.
}
\tag{11}
\]

Equation (11) is the clean extension of the prior result. Productive learning is
identical across organizations; only direct internalization, capture, and
ownership cost remain.

## 7. Customer conflict and the hybrid organization

For a homogeneous candidate size \(n\), let \(R_n(q,p)=\Delta_n(q,p,0)\) be its
value before customer conflict. The conflict penalty is

\[
\chi b_D n(m-n),
\]

where \(b_D\) is customer value per cross-boundary pair. As in the previous
model, define the better endpoint

\[
M(q,p)=\max\{0,R_m(q,p)\}.
\]

Every partial structure is dominated by an endpoint once

\[
\chi\ge
\max_{1\le n<m}
\frac{[R_n(q,p)-M(q,p)]_+}{b_Dn(m-n)}.
\tag{12}
\]

Thus the new capture mechanism does not remove the neutrality problem. It makes
the hybrid economically attractive, while customer distrust can make it
organizationally infeasible. The combined prediction is polarization between a
neutral platform and a full rollup when customer conflict is high, but a
platform-owner hybrid when outside customers continue supplying learning.

## 8. Computed evidence

The symmetric figure uses six assets, direct advantage \(a=0.215\), operating
surplus \(b=0.80\), directed pair learning \(\gamma=0.105\), and owner retained
share \(o=0.45\). The shares and costs are transparent normalizations, not
estimates.

![Access and value appropriation phase map](outputs/value-appropriation-regime-map.svg)

The horizontal axis is external learning efficiency \(q\). The vertical axis is
platform capture \(p\). The secondary labels translate selected capture shares
into the Pareto tail parameter from equation (1).

The left panel sets customer conflict high enough to eliminate partial
ownership. Its dashed curve is equation (10). Three cells illustrate the
mechanisms:

- At \(q=0.05,p=0.40\), a full rollup wins primarily because ownership unlocks
  productive learning.
- At \(q=1,p=0.25\), a full rollup still wins by 0.222 even though its productive
  learning upgrade is exactly zero. The capture upgrade is 1.590 before direct
  gains and ownership costs.
- At \(q=0.90,p=0.40\), the neutral platform wins: learning travels and the
  provider captures enough of its value.

The right panel removes customer conflict. Partial platform-owner structures
occupy much of the middle. At \(q=0.97,p=0.17\), the exact solution owns four of
six symmetric assets. Its external-access slope from equation (6) is positive,
so a marginal increase in customer learning access raises—not lowers—the value
of that selected ownership subset.

Every grid cell compares all seven homogeneous ownership sizes. The general
network solver enumerates all \(2^N\) subsets and reports the gain from every
unchosen deviation. Tests verify the analytical boundary, the nesting result,
the Pareto capture formula, capture monotonicity, the two-node complementarity
counterexample, and zero profitable subset deviations.

The fixed-seed sensitivity exercise perturbs operating value, learning, direct
internalization, owner retention, and ownership costs. Across 600 draws, the
illustrative learning-rollup, full-access capture-rollup, neutral-platform, and
partial-owner anchors retain their displayed broad organizational form in
65.5, 67.5, 98.2, and 83.7 percent of draws. The first two anchors lie relatively
close to the pure boundary; their lower frequencies correctly show that the
normalization is not a quantitative forecast. The exact comparative statics do
not depend on those frequencies.

## 9. What the result contributes

The generic distinction between creating value and capturing it is established
economics. The narrower contribution of this package is the exact connection to
an AI learning network:

1. it decomposes every acquisition subset into productive-learning and
   appropriation wedges;
2. it shows that ownership can arise at \(q=1\), where the earlier learning-only
   mechanism is absent;
3. it identifies condition (7), under which customer access and selective
   ownership become complements rather than substitutes; and
4. it combines that complementarity with customer neutrality to explain why a
   platform-owner hybrid may either emerge or collapse into an endpoint.

The concise result is:

> A scalable AI platform requires two forms of portability: learning must travel
> through customer relationships, and the value created by that learning must
> travel back through prices. If only the first travels, the intermediary may
> own the operations where value lands while retaining customers as learning
> sources; if those customers reject the conflict, market structure polarizes
> between a neutral platform and a full rollup.

## 10. Empirical objects and falsifiers

The model points to measurements that distinguish learning from capture.

- **Platform capture:** provider gross profit or contribution margin divided by
  provider profit plus measured customer operating surplus attributable to the
  service.
- **Owner retention:** the acquirer's realized share of operating improvement
  after the acquisition premium, seller earn-outs, output-price pass-through,
  liability, and financing costs.
- **Incoming learning:** whether experience generated at independent customer
  \(i\) improves decisions at owned operation \(j\).
- **Target direction:** whether acquisitions select businesses where learning
  produces valuable outcomes, rather than only businesses that generate large
  datasets.
- **Neutrality response:** customer usage, disclosure, and renewal after the
  provider acquires an operation that competes with or buys from the customer.

The capture mechanism is weakened if service providers can reliably charge for
realized customer value, if acquisition prices capitalize nearly all expected
AI gains, or if output-market competition passes owned efficiency gains fully
to consumers. The platform-fed-ownership mechanism is falsified if acquisitions
do not follow high-value incoming learning edges after controlling for ordinary
operating synergies.

## 11. Limits

- \(p\) and \(o\) are summary shares. Both now receive a shared pledgeability
  derivation (Section 3), and \(p\) additionally has the Pareto single-price
  benchmark, but the commitment, verifiability, and bargaining primitives
  behind the derivation are themselves supplied rather than solved; a full
  acquisition-bargaining game remains open.
- The task benchmark uses one posted price, a Pareto distribution, common
  marginal cost, and no nonlinear or outcome-contingent contract.
- Operating surplus and learning value are known in expectation. Asset owners
  may have private information about both.
- Direct internalization and operating surplus must be measured separately;
  otherwise the capture extension can double count the bilateral ownership
  gain.
- There is one potential intermediary. Competing labs, platforms, and acquirers
  could bid away capture rents or split the network.
- The solution maximizes the intermediary's private value. Capture changes the
  distribution of surplus and can move ownership without increasing welfare.
- Customer conflict remains reduced form. Exit, foreclosure, exclusivity, and
  endogenous disclosure are not separately solved.
- The model is static. It does not yet feed captured profit into future capital,
  acquisition capacity, or model investment.

Those limits locate the next general-equilibrium exercise. They do not affect
the decomposition or the stated single-intermediary comparative statics.

## 12. Reproducible artifacts

- Source: [`src/hidden_reuse/appropriation.py`](src/hidden_reuse/appropriation.py)
- Tests: [`tests/test_appropriation.py`](tests/test_appropriation.py)
- Generator: [`scripts/generate_appropriation.py`](scripts/generate_appropriation.py)
- Scenario solver: [`scripts/solve_appropriation.py`](scripts/solve_appropriation.py)
- Phase map: [`outputs/value-appropriation-regime-map.svg`](outputs/value-appropriation-regime-map.svg)
- Solved grid: [`outputs/value-appropriation-grid.csv`](outputs/value-appropriation-grid.csv)
- Pareto benchmark: [`outputs/pareto-capture-benchmark.csv`](outputs/pareto-capture-benchmark.csv)
- Worked examples: [`outputs/value-appropriation-examples.json`](outputs/value-appropriation-examples.json)
- Sensitivity evidence: [`outputs/value-appropriation-robustness.csv`](outputs/value-appropriation-robustness.csv)
- Run metadata: [`outputs/value-appropriation-run-summary.json`](outputs/value-appropriation-run-summary.json)
- Optional explorer: [`outputs/value-appropriation-explorer.html`](outputs/value-appropriation-explorer.html)
