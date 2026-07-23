# Result: when hidden learning changes firm boundaries

## Central claim

An AI context market can remain modular in two distinct ways:

1. **control:** hidden reuse is deterred because monitoring and enforceable
   sanctions outweigh the provider's future payoff gain; or
2. **exchange:** reuse occurs, but the provider can compensate the context owner
   for permission to retain and benefit from what it learns.

If neither control nor exchange is available, the owner does not simply accept
the same modular contract. It reduces disclosure or integrates.

The mechanism has close published precursors: Anton and Yao (2002) derive
partial disclosure as the equilibrium sale of an expropriable idea, and
Baccara (2007) shows that hidden leakage by an outside contractor can drive
the in-house versus outsourcing choice. What is claimed as new here is the
joint role of the enforcement margin \(E\ge G(s)/s\) and the pledgeability of
the learning right in selecting among the four governance regimes. See
[REFERENCES.md](REFERENCES.md) for positioning.

## Proposition 1: credibility of non-reuse

Fix disclosure \(s>0\). Let

\[
G(s)=\delta[V_P^2(s)-V_P^2(0)]-c_rs
\]

be the provider's private future payoff gain from reusing the disclosed context.
Let \(E\) be the maximum expected sanction per reused unit under full
monitoring, and let monitoring intensity satisfy \(k\in[0,1]\).

Then:

1. if \(G(s)\le0\), the provider prefers non-reuse without monitoring;
2. if \(G(s)>0\), non-reuse is implementable if and only if

   \[
   E\ge E_D(s)\equiv\frac{G(s)}{s};
   \]

3. whenever deterrence is implementable, the least-cost monitoring intensity is

   \[
   k_D(s)=\frac{G(s)}{Es},
   \]

   with cost

   \[
   C_D(s)=\frac{pG(s)^2}{2E^2s};
   \]

4. if \(E<E_D(s)\), the provider reuses under every feasible monitoring
   intensity; and
5. if, at full disclosure, neither a deterred contract nor a tolerated-reuse
   contract satisfies participation and the payment cap, full modularity cannot
   be the period-one equilibrium. The remaining candidates are partial
   disclosure and no agreement; immediate integration is selected when it is
   the owner's best no-contract alternative.

### Proof

The provider reuses exactly when \(G(s)>Eks\). If \(G(s)\le0\), this inequality
never holds at \(k=0\). For \(G(s)>0\), a deterring \(k\le1\) exists exactly
when \(G(s)/(Es)\le1\), which gives the threshold. Monitoring cost is increasing
in \(k\), so the least-cost implementation uses equality. If the threshold
fails, all feasible \(k\) leave reuse privately profitable. The final statement
then follows from exhaustive comparison of the incentive-compatible
period-one candidates and the owner's no-contract alternatives. ∎

The first four claims are analytical. The fifth maps the incentive condition
into governance using the model's constrained Nash bargain.

## Baseline corollary

At the baseline calibration and default integration cost \(F=0.70\),

\[
G(1)=0.295.
\]

Full-disclosure non-reuse is therefore technologically and legally feasible
only when

\[
E\ge0.295.
\]

This is a feasibility result, not a sufficient condition for secure
modularity. Near the boundary, the necessary monitoring can be expensive enough
that another governance arrangement has the larger Nash product.

The threshold also varies with \(F\) whenever integration changes what either
party can earn if renewal fails or changes the chosen route. The figure
correctly plots \(E_D(1;F)\) as a curve rather than treating 0.295 as a
universal vertical boundary.

## Proposition 2: how much unknown future capability can be priced

Let \(V\ge0\) be the provider's *net* future value from the capability created
by reuse. Its realization is unknown when the period-one contract is signed
and privately observed by the provider later. The parties share a prior with
\(\mu=\mathbb E[V]\).

The contract can claim:

- a secured payment \(b\) before realization, with \(0\le b\le W\); and
- a royalty \(\rho V\), where \(0\le\rho\le\phi\) and \(\phi\) is the largest
  share of realized value that can be verified and collected.

Under risk neutrality, the maximum expected payment the provider can credibly
promise is

\[
P^*(\mu,W,\phi)=\min\{\mu,\;W+\phi\mu\}.
\]

The first ceiling is participation: the provider will not promise more than
its expected net gain. The second is enforceability: the owner can collect only
secured value plus the verifiable share of future value. The formula is an
application of Holmström and Tirole's (1997) pledgeable-income cap to the
value of a learning right, and the comparative static
\(\partial P^*/\partial\mu=\phi\) below is the standard pledgeability
observation.

An implementing contract sets

\[
\rho^*=\phi,
\qquad
b^*=\min\{W,(1-\phi)\mu\}.
\]

The expected value that remains unpledgeable is

\[
\mu-P^*=\max\{0,(1-\phi)\mu-W\}.
\]

### Proof

Every feasible contract satisfies

\[
b+\rho\mu\le\mu
\]

by provider participation and

\[
b+\rho\mu\le W+\phi\mu
\]

by the collateral and verifiability constraints. Expected payment is therefore
bounded above by \(P^*\). The proposed \((b^*,\rho^*)\) attains the smaller of
the two bounds, so the bound is tight. ∎

Three implications matter.

First, uncertainty by itself does not prevent an ex-ante price when the parties
are risk neutral and share a prior. Conditional on \(\mu\), the dispersion of
\(V\) changes realized gains but not \(P^*\). The market fails because value is
unverifiable or cannot be secured, not simply because the future is uncertain.

Second, competition can move the owner's payment toward \(P^*\), but not above
it. Competition improves rent capture inside the feasible set; it does not make
the privately realized remainder collectible.

Third, when enforceability binds,

\[
P^*=W+\phi\mu,
\qquad
\frac{\partial P^*}{\partial\mu}=\phi.
\]

An additional unit of expected capability value produces only \(\phi\) units
of additional pledgeable payment. The remaining \(1-\phi\) enlarges the hidden
value wedge. Better learning can therefore increase the provider's reuse
incentive faster than it increases compensation available to the owner.

The computational extension uses the hidden-reuse model's full-disclosure
private reuse gain as \(\mu\) unless a separate expected value is supplied. It
normalizes \(P^*\) per unit of full disclosure and replaces the reduced-form
payment cap \(\bar T\). The expected claim is treated as committed in period
one. If a provider can avoid a royalty by declining to reuse, the royalty would
also reduce \(G(s)\); that joint incentive effect is not included in the
present wrapper.

## Proposition 3: a private signal prevents true-value extraction

Suppose the provider privately learns before contracting whether its expected
net capability value is \(\mu_L\) or \(\mu_H>\mu_L\). The high signal occurs
with probability \(\pi\). Define each type's maximum financeable access fee as

\[
P_t^*=\min\{\mu_t,\;W+\phi\mu_t\},
\qquad t\in\{L,H\}.
\]

The context owner cannot observe the signal and posts one fee. Let \(C\) be its
cost of granting access. Among positive-trade offers, it need compare only:

\[
\Pi_{\mathrm{pool}}=P_L^*-C,
\]

which both types accept, and

\[
\Pi_{\mathrm{screen}}=\pi(P_H^*-C),
\]

which only the high type can finance. The owner pools when the first is weakly
larger, screens when the second is strictly larger, and makes no offer when
both are non-positive.

### Proof

A fee at or below \(P_L^*\) is accepted by both types and is dominated by
charging \(P_L^*\). A fee between \(P_L^*\) and \(P_H^*\) is accepted only by
the high type and is dominated by charging \(P_H^*\). A fee above \(P_H^*\) is
accepted by neither. Comparing the two undominated offers with no trade gives
the result. ∎

Even successful screening does not extract the high type's eventual “true
value.” It leaves expected rent of at least

\[
\mu_H-P_H^*.
\]

If the owner instead pools, the high type keeps
\(\mu_H-P_L^*\). The private signal therefore adds a second wedge: the owner
must choose between leaving information rent and excluding low-signal trade.
This is a two-type posted-price benchmark, not a general optimal mechanism.

## Computed governance map

![Hidden-reuse phase map](outputs/hidden-reuse-regime-map.svg)

The phase map varies:

- maximum enforcement capacity \(E\) on the horizontal axis;
- integration cost \(F\) on the vertical axis; and
- the context-payment cap \(\bar T\) across panels.

All other primitives remain at the baseline values in
[`MODEL.md`](MODEL.md#3-parameter-glossary).

The map shows four robust regions:

- **Secure modularity** dominates where enforcement can deter reuse at an
  acceptable monitoring cost.
- **Ownership** dominates when enforcement is weak and integration is cheap.
- **Strategic withholding** appears when enforcement is weak, integration is
  expensive, and the provider cannot make a sufficient payment for learning
  rights.
- **Priced reuse** expands as \(\bar T\) rises, converting some withholding and
  ownership outcomes into full disclosure with compensated learning.

The generated CSV contains the contract, payoffs, incentive measures, and
continuation route at every cell. The JSON summary records the full baseline,
software versions, grid dimensions, and regime counts.

## Endogenous pricing map

![Capability pledgeability and governance](outputs/capability-pledgeability-map.svg)

The left panel varies the verifiable share \(\phi\) horizontally and collateral
as a share of expected value, \(W/\mu\), vertically. The color is

\[
\frac{P^*}{\mu}=\min\left\{1,\frac{W}{\mu}+\phi\right\}.
\]

The dashed diagonal marks full pledgeability. Below it, some expected
capability value cannot be promised to the owner even under a perfectly
competitive price benchmark.

The right panel feeds that endogenous payment ceiling into the hidden-reuse
game at weak enforcement \(E=0.20\) and costly integration \(F=0.80\). At the
lower left, little future value is verifiable or secured, so the owner
strategically withholds. Moving northeast eventually supports full disclosure
with priced reuse.

This second boundary is a contracting result, not an estimate of how verifiable
or collateralized real AI capability is.

## The sign reversal

Provider learning does not have one universal effect on modular trade.

When future learning value can be credibly committed as a payment today, a
provider can pay for the right to learn. A larger learning benefit can then
help finance context exchange and preserve full disclosure.

When the same learning is hidden, weakly enforceable, and cannot be committed
as payment, it raises the incentive to reuse and increases what the provider can
earn if renewal fails. The owner responds by withholding or internalizing the
relationship.

Thus the relevant question is not simply whether provider learning is socially
productive. It is whether its value can be governed before disclosure changes
what each party can demand in the next negotiation.

## Comparative statics

Holding other primitives fixed:

- larger gains \(g\) in what the provider can earn elsewhere after reuse
  weakly raise the private reuse gain and required enforcement;
- a higher discount factor \(\delta\) places more weight on future learning and
  usually raises the reuse incentive;
- higher enforcement capacity \(E\) makes deterrence feasible over a larger
  set and reduces its monitoring cost as \(1/E^2\);
- higher monitoring cost \(p\) does not change technical feasibility but makes
  secure modularity less attractive;
- a larger payment cap \(\bar T\) lets the provider pay more for permission to
  retain and benefit from what it learns;
- a higher verifiable share \(\phi\) or more collateral \(W\) weakly increases
  \(P^*\), while neither can raise it above the provider's expected net value;
- when enforceability binds, expected capability value \(\mu\) raises
  pledgeable payment only at rate \(\phi\) and raises the unpledgeable remainder
  at rate \(1-\phi\);
- greater competition can increase the owner's share of \(P^*\), but cannot
  increase \(P^*\) itself;
- a more likely high private signal makes screening more attractive, while a
  larger low-type ceiling makes pooling more attractive;
- a larger owner reuse loss \(R\) reduces the owner's payoff from tolerated
  reuse;
- a lower integration cost \(F\) makes ownership a stronger no-contract
  alternative and expands ownership; and
- greater value \(V_M\) from using multiple providers can protect the owner in
  period-two bargaining, although it can also make an initial contract harder
  to reach by giving the owner a better fallback.

Some effects are piecewise because reuse can change the period-two route. The
solver evaluates those route changes rather than imposing global derivatives
through a discontinuity.

## Empirical predictions

The model motivates—but does not yet test—the following predictions:

1. Context owners should demand stronger non-retention, audit, confidential
   execution, or on-premise terms when provider learning is more transferable
   to rivals.
2. Credible improvements in enforcement should increase disclosure and reduce
   integration pressure, especially where monitoring costs are low.
3. Explicit data-licensing or learning-right payments should preserve modular
   exchange in settings where reuse is difficult to prevent.
4. When provider payments are legally, organizationally, or financially
   constrained, greater provider learning value should instead predict
   withholding or ownership.
5. Revenue-share contracts should be more common where downstream capability
   value is auditable; upfront access fees or bonds should matter more where
   future value is hard to observe but providers have collateral.
6. Provider competition should raise payments only where learning value is
   already pledgeable. It should have weaker effects when future value remains
   private and unsecured.
7. Integration should be most likely where context rents are high, learning is
   difficult to govern, and acquisition or internal deployment is relatively
   cheap.
8. When providers privately differ in learning value, higher access fees should
   be associated with exclusion of low-value providers rather than full
   extraction of high providers' realized gains.

Useful empirical variation could come from retention-policy changes,
confidential-compute rollouts, enforcement differences across jurisdictions,
changes in auditability, and financing shocks. Parameters should be measured or
bounded before observing the governance choice; fitting them solely to explain
an acquisition would make the exercise tautological.

## What is not a result

The phase diagram does not show:

- an estimated probability that any real firm will integrate;
- a Monte Carlo distribution over stochastic histories;
- a welfare ranking of the four regimes;
- proof that hidden reuse currently occurs;
- a full auction or endogenous entry game among multiple AI providers; or
- equilibrium concentration across model, application, and infrastructure
  layers.

Calling the output "empirical equilibrium" would be incorrect at this stage.
It is a calibrated equilibrium computation whose comparative statics generate
empirical hypotheses.

## Limitations and next tests

The most important bilateral robustness exercises are:

1. replace binary reuse with continuous reuse;
2. replace the two-type posted price with continuous private signals and an
   optimal dynamic mechanism;
3. endogenize provider competition, auctions, and the owner's use of multiple
   providers instead of treating competition only as a price benchmark;
4. permit risk aversion, financing costs, and state-dependent limited
   liability in the pledgeability contract;
5. jointly solve reuse incentives when a future royalty is avoidable rather
   than committed at signing;
6. allow internal leakage and bureaucracy under ownership;
7. distinguish private exclusivity loss from social diffusion gains;
8. relax the homogeneous firm-size benchmark into heterogeneous
   context-generating assets and a cross-node learning network; and
9. calibrate or partially identify primitives using external moments.

The first five should precede a large stochastic industry simulation. They test
whether the mechanism survives smoother choices, private information before
contracting, and richer markets for permission to reuse and learn from context.

The homogeneous multi-asset benchmark is now developed separately in
[FIRM-SIZE-RESULT.md](FIRM-SIZE-RESULT.md). It proves that an additive
hidden-reuse advantage changes integration entry but not conditional firm size.
That result narrows the remaining industry question to asset heterogeneity,
cross-node learning networks, financing, and competition among acquirers.
