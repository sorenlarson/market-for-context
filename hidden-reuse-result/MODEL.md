# Model: a two-period hidden-reuse game

This document fully specifies the contracting game implemented in
[`src/hidden_reuse/model.py`](src/hidden_reuse/model.py) and the endogenous
capability-pricing extension in
[`src/hidden_reuse/pledgeability.py`](src/hidden_reuse/pledgeability.py). It can
be read without the website essay or any earlier model.

## 1. Economic environment

An organization owns private context that improves an AI service: customer
history, workflow data, operating experience, private evaluations, or knowledge
of a local environment. It can disclose that context to an outside AI provider
or integrate the capability.

An **arm's-length contract** below means an ordinary agreement between
independent firms. **Integration** means the context owner builds or acquires
the relevant capability instead.

Disclosure produces two things:

1. a current service whose value is visible to both parties; and
2. a learning opportunity that can improve the provider's future capability
   and let it demand better terms later.

The provider chooses reuse only after it sees the context. Reuse is therefore a
hidden action, not a contractible input. Monitoring and sanctions can sometimes
make a non-reuse promise credible. Alternatively, the provider may pay for the
right to learn. When neither route works, the owner shares less or integrates.

## 2. Actors and timing

There are two risk-neutral actors:

- \(O\), the context owner; and
- \(P\), the AI provider.

The game proceeds as follows:

1. **Initial alternatives.** The owner can integrate immediately, wait to use a
   different provider or internal system, or exit. The provider also has an
   **outside option**: what it earns if this contract is never signed.
2. **Period-one contract.** The parties bargain over disclosure
   \(s\in[0,1]\), monitoring \(k\in[0,1]\), and transfer \(\tau\). A positive
   \(\tau\) is paid by the owner to the provider; a negative \(\tau\) is paid
   by the provider for access to context.
3. **Current service.** The owner discloses \(s\), generating \(B(s)\).
4. **Hidden reuse.** The provider privately chooses \(r\in\{0,s\}\): reuse all
   disclosed context or none of it.
5. **Period-two routing.** The owner renews with the incumbent, uses more than
   one provider (multi-homes), builds or acquires the capability itself
   (integrates), or stops. If renewal creates enough value, the parties bargain
   over how to divide it.

The period-one contract anticipates every continuation payoff and hidden-action
incentive.

## 3. Parameter glossary

| Symbol | Code name | Baseline | Interpretation |
|---|---|---:|---|
| \(m\) | `current_marginal_value_at_full` | 0.55 | Marginal current value of the final disclosure unit |
| \(c\) | `current_curvature` | 0.45 | Curvature of current context value |
| \(\delta\) | `discount_factor` | 0.90 | Weight on period-two payoffs |
| \(\bar S\) | `future_renewal_surplus` | 0.80 | Period-two renewal output before reuse gains |
| \(V_M\) | `future_multihome_value` | 0.42 | Owner value from using multiple providers |
| \(V_I\) | `future_integration_value` | 0.62 | Owner's gross future integration value |
| \(F\) | `integration_cost` | 0.70 | Fixed cost of integration |
| \(R\) | `owner_reuse_loss` | 0.75 | Owner's exclusivity loss per reused unit |
| \(q\) | `incumbent_capability_gain` | 0.25 | Renewal output gained from provider learning |
| \(\bar d_P\) | `provider_outside_base` | 0.08 | Provider's period-two outside option without reuse |
| \(g\) | `provider_outside_gain` | 0.45 | Provider outside-option gain per reused unit |
| \(c_r\) | `reuse_cost` | 0.02 | Provider's direct reuse cost |
| \(E\) | `enforcement_capacity` | 0.45 | Maximum expected sanction per reused unit at full monitoring |
| \(p\) | `monitoring_cost` | 0.25 | Monitoring-cost coefficient |
| \(\bar T\) | `context_payment_cap` | 0.00 | Reduced-form maximum provider-to-owner payment per disclosed unit |
| \(\beta_1\) | `period_one_owner_bargaining_weight` | 0.50 | Owner's period-one Nash weight |
| \(\beta_2\) | `period_two_owner_bargaining_weight` | 0.50 | Owner's period-two Nash weight |
| \(d_P^1\) | `provider_initial_outside_option` | 0.05 | Provider payoff if no initial contract is signed |

All values are normalized utility units. They are illustrative, not estimated.
The generated run metadata records the exact calibration used for each figure.

## 4. Current value from disclosure

The current benefit from disclosure is

\[
B(s)=(m+c)s-\frac{c}{2}s^2,
\qquad s\in[0,1].
\]

This function is concave, but \(B'(1)=m>0\). Full context use is therefore
valuable absent reuse and contracting frictions. Withholding is an equilibrium
response to future appropriation, not an assumption that more context is
unproductive.

## 5. Period-two continuation game

After reuse \(r\), the owner's best operating alternative to renewal is

\[
x_O(F)=\max\{0,V_M,V_I-F\}.
\]

The incumbent provider's outside option—what it can earn if renewal fails—is

\[
x_P(r)=\bar d_P+gr.
\]

Reuse can therefore let the provider serve other customers more effectively or
enter the renewal negotiation from a stronger position. Renewal produces total
operating surplus

\[
S_R(r)=\bar S+qr.
\]

Define the incremental bargaining surplus

\[
\Delta(r,F)=S_R(r)-x_O(F)-x_P(r).
\]

When \(\Delta(r,F)\ge0\), renewal occurs. The model uses generalized Nash
bargaining, a formal rule that divides the gains from agreement according to
the parties' bargaining weights:

\[
V_O^2(r)=x_O(F)+\beta_2\Delta(r,F)-Rr,
\]

\[
V_P^2(r)=x_P(r)+(1-\beta_2)\Delta(r,F).
\]

When \(\Delta(r,F)<0\), the owner takes the maximizing outside route and the
provider receives \(x_P(r)\). The owner still bears the exclusivity loss
\(Rr\), which is sunk by the time routing occurs.

## 6. The hidden-reuse incentive

For disclosure \(s>0\), the provider's private gain from reuse before
enforcement is

\[
G(s)=\delta\left[V_P^2(s)-V_P^2(0)\right]-c_rs.
\]

Monitoring intensity \(k\) creates an expected sanction \(Eks\). The provider
reuses if and only if

\[
G(s)>Eks.
\]

If \(G(s)\le0\), the provider already prefers non-reuse and no monitoring is
required. If \(G(s)>0\), the minimum monitoring that deters reuse is

\[
k_D(s)=\frac{G(s)}{Es}.
\]

Deterrence is feasible exactly when

\[
E\ge E_D(s)\equiv\frac{G(s)}{s}.
\]

Choosing \(k_D\) costs

\[
C_D(s)=\frac{p}{2}k_D(s)^2s
=\frac{pG(s)^2}{2E^2s}.
\]

Sanctions are paid to a third party. Monitoring that remains below \(k_D\)
does not compensate the owner and does not change the provider's binary reuse
choice, so it is strictly wasteful. The solver therefore compares only:

- tolerated reuse with \(k=0\); and
- no reuse with exactly \(k=k_D\), when feasible.

## 7. Period-one alternatives and bargaining

The owner's value from immediate integration is

\[
I=B(1)+\delta V_I-F.
\]

Its value from waiting one period is

\[
W_O=\delta\max\{0,V_M,V_I-F\}.
\]

The owner's initial disagreement payoff—what it receives if no period-one
contract is signed—is

\[
d_O^1=\max\{0,I,W_O\}.
\]

For a candidate contract \((s,k,r)\), pre-transfer payoffs are

\[
\widetilde U_O=B(s)+\delta V_O^2(r),
\]

\[
\widetilde U_P=\delta V_P^2(r)-c_rr-\frac{p}{2}k^2s.
\]

The baseline assigns monitoring cost to the provider before transfers. Final
payoffs are

\[
U_O=\widetilde U_O-\tau,
\qquad
U_P=\widetilde U_P+\tau.
\]

A negative service price would mean that the provider buys access to context.
The payment-cap constraint is

\[
\tau\ge-\bar T s.
\]

This reduced-form constraint captures limited liability, an inability to commit
future learning value as a payment today, uncertainty about that value,
accounting restrictions, or a prohibition on providers explicitly buying
customer data. Section 8 replaces \(\bar T\) with an explicit pledgeability
problem.

The contract must satisfy

\[
U_O>d_O^1,
\qquad
U_P>d_P^1.
\]

Among feasible contracts, the parties maximize the generalized Nash product

\[
(U_O-d_O^1)^{\beta_1}(U_P-d_P^1)^{1-\beta_1}.
\]

When transfers are unrestricted, bargaining weights affect who captures the
value but not the value-maximizing governance arrangement. When the payment cap
binds, the distribution of pre-transfer payoffs can change whether a contract
is feasible.

## 8. Endogenous pricing of uncertain capability

The reduced-form cap is useful for isolating the governance mechanism, but it
does not explain how a capability that does not yet exist receives a price.
The extension supplies that missing contract.

Let \(V\ge0\) be the provider's future *net* value from learning at full
disclosure. Its realization is unknown when the parties contract and privately
observed by the provider later. Both parties initially share a distribution
with

\[
\mu=\mathbb E[V].
\]

The contract has two enforceable instruments:

1. a payment \(b\) made or secured before realization by collateral \(W\), so
   \(0\le b\le W\); and
2. a royalty \(\rho V\), where \(\rho\le\phi\) and \(\phi\) is the largest
   share of realized capability value that an auditor, court, or payment system
   can verify and collect.

The provider's participation constraint is

\[
b+\rho\mu\le\mu.
\]

The maximum expected provider-to-owner payment is therefore

\[
P^*=\min\{\mu,\;W+\phi\mu\}.
\]

It is implemented by

\[
\rho^*=\phi,
\qquad
b^*=\min\{W,(1-\phi)\mu\}.
\]

When \(W<(1-\phi)\mu\), enforceability binds and

\[
\frac{\partial P^*}{\partial\mu}=\phi,
\qquad
\frac{\partial(\mu-P^*)}{\partial\mu}=1-\phi.
\]

Capability improvements then enlarge the unpledgeable remainder faster than
the enforceable payment whenever \(\phi<1/2\).

The extension's parameters are:

| Symbol | Code name | Baseline | Interpretation |
|---|---|---:|---|
| \(\mu\) | `expected_net_capability_value` | endogenous | Shared-prior mean of the provider's net learning value |
| \(\phi\) | `verifiable_share` | 0.00 | Largest collectible royalty share of realized value |
| \(W\) | `collateral` | 0.00 | Payment or bond secured before realization |
| \(\sigma\) | `value_log_sigma` | 0.80 | Lognormal dispersion used for realized-value quantiles |
| \(\alpha\) | `bilateral_owner_capture` | 0.50 | Reporting benchmark for bilateral capture of \(P^*\) |

When \(\mu\) is not supplied, the code sets it equal to
\(\max\{0,G(1)\}\), the provider's endogenous full-disclosure reuse gain. The
maximum pledgeable payment \(P^*\) then replaces \(\bar T\).

The pricing distinction is:

- **unknown but commonly understood value** can be priced in expectation;
- **unverifiable and unsecured value** cannot be credibly shared after it is
  privately realized; and
- **competition** can move the payment from a bilateral benchmark toward
  \(P^*\), but cannot raise the ceiling itself.

### A private signal before contracting

The common-prior benchmark separates uncertainty from unverifiability. The
module also includes a two-type adverse-selection test.

Before the contract, the provider privately learns whether its expected value
is \(\mu_L\) or \(\mu_H>\mu_L\). The high signal has probability \(\pi\). Each
type can finance a fixed access fee only up to

\[
P_t^*=\min\{\mu_t,W+\phi\mu_t\}.
\]

The owner cannot observe the signal and posts one fee. With access cost \(C\),
its undominated choices are:

\[
\Pi_{\mathrm{pool}}=P_L^*-C
\]

from a low fee accepted by both types, or

\[
\Pi_{\mathrm{screen}}=\pi(P_H^*-C)
\]

from a high fee that only the high type can finance. If both profits are
non-positive, there is no trade.

Even the screening fee leaves the high type at least
\(\mu_H-P_H^*\) in expected value. The owner can induce the provider to reveal
that it has a high signal by paying a high fee, but cannot force it to remit an
unverifiable remainder after capability value materializes.

The current wrapper normalizes the full-disclosure \(P^*\) per context unit, so
the payment ceiling scales linearly with partial disclosure. It does not yet
model a provider that privately knows a high or low value type before the
initial bargain.

It also treats the expected secured-plus-royalty claim as committed in period
one. If the provider could avoid a royalty simply by declining to reuse, that
royalty would reduce \(G(s)\) as well as finance a payment. A joint contract
over royalty incentives and reuse is an explicit next extension rather than a
hidden feature of the current solver.

## 9. Computational equilibrium

The model is solved by backward induction:

1. solve the period-two route and Nash bargain for \(r=0\) and every possible
   \(r=s\);
2. compute \(G(s)\), \(E_D(s)\), and the provider's incentive-compatible reuse
   choice;
3. for each disclosure point, evaluate tolerated reuse and feasible
   deterrence;
4. solve the constrained transfer bargain for each candidate;
5. choose the candidate with the highest period-one Nash product; and
6. if no contract between the independent firms makes both parties better off,
   select the owner's best initial alternative.

The baseline uses a deterministic disclosure grid. The primary solver defaults
to 201 points; worked examples use 401. Tests verify grid-refinement stability
at reference calibrations. Near a regime boundary, a coarse grid can place the
winning disclosure one cell away from the fine-grid solution, so regime labels
within one grid cell of a boundary should be checked at a finer grid. Full
disclosure is labeled only when the winning disclosure is the top grid point
\(s=1\), which every grid contains exactly.

The solver does not simulate boundedly rational agents or declare a stable
trajectory an equilibrium. Every reported contract satisfies the modeled
participation, transfer, and hidden-action constraints.

The endogenous-pricing wrapper first solves \(P^*\), substitutes it for
\(\bar T\), and then runs the same backward-induction contracting solver. The
capability-value distribution is not Monte Carlo simulated: the mean determines
the risk-neutral ex-ante ceiling and the lognormal dispersion is used only to
report transparent realized-value quantiles.

## 10. Governance regimes

The canonical regime names are:

1. **Secure modularity:** full disclosure and no reuse, either naturally or
   because monitoring deters it.
2. **Priced reuse:** full disclosure and reuse, supported by a provider payment
   for permission to retain and benefit from what it learns.
3. **Strategic withholding:** the owner discloses less than the full context.
   This normally means a partial contract between independent firms; in the
   limiting case it includes complete withholding when waiting dominates
   immediate integration.
   The output's `agreement` field distinguishes those cases.
4. **Ownership:** no market contract dominates the owner's option to build or
   acquire the capability.

The code retains `LEAKY_MODULAR` as a backward-compatible alias for
`PRICED_REUSE`; generated results use `priced_reuse`.

## 11. Worked examples

All examples use the baseline parameters except for \(E\), \(F\), and
\(\bar T\). Values below are approximate solutions from a 401-point disclosure
grid.

| \(E\) | \(F\) | \(\bar T\) | Outcome | \(s\) | \(k\) | \(r\) | \(\tau\) |
|---:|---:|---:|---|---:|---:|---:|---:|
| 0.20 | 0.80 | 0.00 | Strategic withholding | 0.60 | 0.00 | 0.60 | 0.00 |
| 0.20 | 0.80 | 0.15 | Priced reuse | 1.00 | 0.00 | 1.00 | -0.15 |
| 0.40 | 0.40 | 0.00 | Secure modularity | 1.00 | 0.74 | 0.00 | 0.13 |

The first two rows isolate pricing capacity. With identical enforcement and
integration cost, allowing the provider to pay 0.15 per context unit converts
partial disclosure into full disclosure with compensated reuse. In the third
row, stronger enforcement makes the provider prefer compliance to reuse. A
negative \(\tau\) means the provider pays the owner.

Machine-readable values are generated in
[`outputs/worked-examples.json`](outputs/worked-examples.json).

For the endogenous-pricing extension, weak enforcement \(E=0.20\), costly
integration \(F=0.80\), and the baseline full-disclosure gain imply
\(\mu=0.295\):

| \(\phi\) | \(W\) | \(P^*\) | Pledgeable share | Governance |
|---:|---:|---:|---:|---|
| 0.00 | 0.00 | 0.000 | 0% | Strategic withholding |
| 0.10 | 0.02 | 0.050 | 17% | Strategic withholding |
| 0.50 | 0.00 | 0.148 | 50% | Priced reuse |
| 0.80 | 0.20 | 0.295 | 100% | Priced reuse |

The values are generated in
[`outputs/pledgeability-examples.json`](outputs/pledgeability-examples.json).
Run `python3 scripts/solve_pricing.py --help` to inspect one parameter
combination.

The default private-signal benchmark has
\((\mu_L,\mu_H,\pi)=(0.15,0.45,0.30)\),
\(\phi=0.10\), and \(W=0.02\). The type-specific ceilings are 0.035 and
0.065. Pooling yields 0.035, while screening yields only
\(0.30(0.065)=0.0195\), so the owner posts the pooling fee and the high type
keeps 0.415 in expected value. At \(\pi=0.90\), the owner screens, but the high
type still keeps 0.385.

Run `python3 scripts/solve_private_signal.py --help` to inspect this benchmark.
Machine-readable examples are included in
[`outputs/pledgeability-examples.json`](outputs/pledgeability-examples.json).

## 12. Assumptions

- Reuse is binary: all disclosed context or none.
- Monitoring is contractible, while reuse is privately chosen.
- Enforcement capacity combines detection, legal enforceability, and the
  maximum collectible sanction.
- Sanctions go to a third party.
- Agents are risk neutral and share common knowledge of primitives and the
  capability-value distribution.
- Realized capability value is privately observed after contracting; providers
  may also receive the optional high/low private signal before contracting.
- Collateral is fully collectible and the verifiable royalty share is
  contractible without measurement cost.
- The pricing wrapper treats the expected claim as committed before the hidden
  reuse choice; an avoidable royalty's direct effect on \(G(s)\) is not yet
  modeled.
- Period-two fallbacks are predefined rather than generated by competition
  among providers.
- Integration has a fixed cost and eliminates external reuse; bureaucracy,
  internal leakage, financing constraints, and capability differences are
  compressed into primitives.
- The model has one context owner and one incumbent provider.
- The private-signal extension is a single posted-fee benchmark, not a general
  auction or optimal mechanism.
- The calibration is illustrative and deterministic.

These restrictions isolate the hidden-reuse mechanism. They should be relaxed
one at a time rather than concealed inside a larger agent-based simulation.

## 13. Firm-size extension

The bilateral model determines whether one context relationship is governed by
a contract or ownership. It does not contain multiple assets and therefore
cannot determine firm size.

The sequel introduces homogeneous context-generating assets and lets coalitions
form freely. For a firm of size \(n\), surplus per asset is

\[
g(n)=A-\frac Kn
+L\frac{n-1}{\kappa+n-1}
-dn^{\rho-1}
-cn^\eta.
\]

The bilateral game supplies the private internalization advantage \(A\). The
remaining terms describe shared fixed cost, transferable cross-asset learning,
learning saturation, declining marginal integration-execution cost
\(dn^\rho\) for \(0<\rho<1\), and increasing ongoing coordination cost.
Because \(A\) is additive, it changes whether the best integrated firm has
positive value but not which size maximizes value per asset. That separation
is a characterization, not a free result: it holds if and only if the
advantage is size-independent. The solver exposes an optional dilution
elasticity under which the per-asset advantage becomes \(An^{-\zeta}\); any
\(\zeta>0\) makes the entry and size margins interact, and
[FIRM-SIZE-RESULT.md](FIRM-SIZE-RESULT.md) reports a worked non-additive
example.

The full environment, equilibrium definition, proposition, proof, bridge, and
limitations are in [FIRM-SIZE-RESULT.md](FIRM-SIZE-RESULT.md). The source of
truth is [src/hidden_reuse/firm_size.py](src/hidden_reuse/firm_size.py).

## 14. Ownership-access network extension

The homogeneous sequel assumes transferable learning requires common
ownership. Version 0.4 adds the platform alternative: one intermediary can
realize a fraction \(q\) of directed cross-node learning while the operating
assets remain independent customers.

For a candidate ownership subset \(S\), private incremental value is

\[
\Delta(S)=
\sum_{i\in S}a_i
+(1-q)\sum_{i,j\in S;\ i\ne j}\gamma_{ij}
-C(S)-\chi D(\partial S).
\]

The directed matrix \(\gamma_{ij}\) permits different asset types and
asymmetric learning opportunities. The directed customer network in
\(D(\partial S)\) allows the businesses to buy from or sell to one another;
partial ownership can put relationships crossing the boundary at risk.

The model exactly enumerates every acquisition subset for one intermediary. It
is neither the bilateral game's free-formation replica equilibrium nor a
general equilibrium among competing acquirers. The environment, analytical
thresholds, proof, heterogeneous counterexample, and limits are in
[OWNERSHIP-ACCESS-RESULT.md](OWNERSHIP-ACCESS-RESULT.md). The source of truth is
[src/hidden_reuse/ownership_access.py](src/hidden_reuse/ownership_access.py).

## 15. Value-appropriation extension

Version 0.5 relaxes the assumption that one unit of learning produces the same
private return under a service relationship and ownership. Let (p) be the
platform's share of AI-created operating value and (o) the acquirer's retained
share under ownership. For a subset (S), let (B(S)) be operating surplus at
owned nodes, (Gamma_I(S)) learning between owned nodes, and
(Gamma_X(S)) learning imported from outside customers into owned nodes.

The exact incremental private value becomes

\[
\Delta(S)=
\sum_{j\in S}a_j
+(o-p)\left[B(S)+q(\Gamma_I(S)+\Gamma_X(S))\right]
+o(1-q)\Gamma_I(S)
-C(S)-\chi D(\partial S).
\]

The second term is a capture upgrade on value already producible through
customer access. The third is the productive learning unlocked by ownership.
When (q=1), only the capture, direct internalization, and cost terms remain.

For a fixed partial subset,

\[
\frac{\partial\Delta(S)}{\partial q}
=(o-p)\Gamma_X(S)-p\Gamma_I(S).
\]

Thus the ownership-access model's global monotonicity does not extend to this
environment: customer access can raise selective ownership value when outside
customers feed learning into owned destinations.

The two capture shares are not free parameters. They are derived from the same
pledgeability logic as Section 8, applied to opposite sides of two markets: the
provider charging for realized service value collects
\(p=\min\{1,w_s+\phi_s\}\), while a seller charging for prospective
acquisition gains capitalizes only its pledgeable share, leaving the acquirer
\(o=(1-\beta_a\min\{1,w_a+\phi_a\})(1-\lambda)\). Under symmetric frictions,
\(o>p\) exactly when the pledgeable share of AI-created value is below one
half. See the derivation section of
[APPROPRIATION-RESULT.md](APPROPRIATION-RESULT.md) and
`derive_capture_shares` in the source module.

The complete public exposition is in
[FULL-EXPOSITION.md](FULL-EXPOSITION.md), the focused chapter extract is
[APPROPRIATION-DRAFT.md](APPROPRIATION-DRAFT.md), the derivation and proofs are
in [APPROPRIATION-RESULT.md](APPROPRIATION-RESULT.md), and the computational
source of truth is
[src/hidden_reuse/appropriation.py](src/hidden_reuse/appropriation.py).
