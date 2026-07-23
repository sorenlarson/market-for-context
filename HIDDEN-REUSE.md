# Hidden reuse and the Arrow–Coase ratchet

> **Canonical package:** The self-contained publication version now lives in
> [`hidden-reuse-result/`](hidden-reuse-result/README.md). This document is
> retained as the exploratory technical note.

## 1. The economic problem

An organization owns context that makes an AI system more valuable: customer
history, workflow data, operating experience, private evaluations, or knowledge
of a local environment. Call this organization the **context owner**. It would
like to use an outside **AI provider**, because the provider has capabilities
that would be costly to reproduce internally.

Sharing context with the provider creates two outputs at once. It improves the
current service, but it can also teach the provider something. The provider may
retain patterns, improve its general capability, or become better able to earn
money from other customers if this relationship ends. Economists call that
fallback a better **outside option**: what the provider can earn without
renewing this particular contract. The owner receives the current benefit but
may lose some of the scarcity and future bargaining power attached to its
context.

This is an Arrowian problem because the owner cannot obtain the full value of
the service without revealing information. It becomes a Coasian problem because
the information cannot simply be taken back after revelation. If reuse cannot
be reliably prohibited or compensated, the owner may disclose less context or
bring the activity inside the firm.

The model asks:

> When can independent firms contract for full use of valuable context, and
> when does anticipated provider learning instead produce strategic
> withholding or ownership?

Its basic answer is:

- credible enforcement can support **secure modularity**;
- weak enforcement can still support **priced reuse** if the provider can pay
  for permission to retain and benefit from what it learns;
- if reuse can be neither deterred nor adequately priced, the owner withholds
  context when integration is expensive and integrates when it is cheap.

The central friction is therefore not merely whether privacy technology exists.
It is whether the maximum credible consequence of reuse is large enough to
offset the provider's future gain from learning.

## 2. Actors and timing

The model deliberately reduces the larger AI stack to one bilateral
relationship:

- the context owner \(O\) controls valuable private context and can ultimately
  use more than one provider (multi-home), build or acquire the capability
  itself (integrate), or stop the activity (exit);
- the AI provider \(P\) supplies external capability and may learn from the
  context it receives.

The game has two periods:

1. The parties anticipate what each could earn without an agreement—their
   outside options—and negotiate a market contract while remaining independent.
   The contract specifies disclosure \(s\in[0,1]\), monitoring intensity
   \(k\in[0,1]\), and a transfer \(\tau\) from the owner to the provider.
2. The owner discloses \(s\), generating a current operating benefit.
3. After seeing the context, the provider privately chooses whether to reuse
   it. For transparency, the baseline choice is binary: reuse all disclosed
   context or reuse none of it.
4. In period two, reuse affects the provider's capability and what it can earn
   if renewal fails, while eroding the owner's exclusive context rent.
5. The owner chooses whether to renew with the incumbent, use more than one
   provider, build or acquire the capability itself, or stop. If the parties
   renew, they bargain again over the value created by continuing together.

The period-one contract is chosen with all of these continuation incentives in
view. If no market contract makes both parties better off than their
initial alternatives, the owner integrates immediately or waits.

## 3. Current value from disclosure

Let \(s\in[0,1]\) be the fraction of context disclosed. Its current benefit is

\[
B(s)=(m+c)s-\frac{c}{2}s^2,
\qquad m>0,\;c>0.
\]

The function is concave, but \(B'(1)=m>0\). Thus full disclosure is valuable in
the absence of learning, reuse, or contracting frictions. Any withholding in
the model is a strategic response to the future consequences of revelation,
not an assumption that additional context is useless.

## 4. Period-two continuation game

Let \(r\in\{0,s\}\) be hidden reuse of period-one disclosure \(s\). The owner's
operating outside option in period two is

\[
d_O^2(F)=\max\{0,V_M,V_I-F\},
\]

where \(V_M\) is the value of multi-homing and \(V_I-F\) is the value of
integration. The incumbent provider's outside option is

\[
d_P^2(r)=\bar d_P+gr.
\]

Reuse therefore increases the provider's ability to serve other customers or
to bargain from a stronger capability position. Renewal creates total operating
surplus

\[
S_R(r)=\bar S+qr,
\]

where \(q\) is the quality gain created by learning from context. Renewal occurs
when

\[
S_R(r)\ge d_O^2(F)+d_P^2(r).
\]

If renewal occurs, generalized Nash bargaining splits the surplus over those
outside options. If not, the owner takes its best outside route and the provider
keeps its outside option. In either case, the owner loses exclusive context rent

\[
Rr.
\]

This loss is sunk by the time period-two routing is chosen, but it matters when
the owner evaluates the period-one contract.

## 5. The provider's hidden-reuse incentive

Let \(V_P^2(r)\) be the provider's period-two equilibrium payoff. Its private
gain from reusing disclosure \(s\), before enforcement, is

\[
G(s)=\delta\left[V_P^2(s)-V_P^2(0)\right]-c_rs,
\]

where \(c_r\) is the direct cost of reuse.

Monitoring intensity \(k\in[0,1]\) produces a maximum expected sanction

\[
Eks,
\]

where \(E\) combines detection probability, legal enforceability, and the
maximum collectible penalty. The provider reuses context exactly when

\[
G(s)>Eks.
\]

The minimum monitoring needed to deter reuse is therefore

\[
k_D(s)=\frac{G(s)}{Es}.
\]

A non-retention promise is technologically and legally credible only when

\[
k_D(s)\le1.
\]

Deterrence costs

\[
\frac p2 k_D(s)^2s.
\]

The baseline assumes sanctions are paid to a third party. Positive monitoring
that does not deter reuse therefore destroys surplus without compensating the
owner. The only relevant contractual choices are zero monitoring with tolerated
reuse, or the minimum monitoring that fully deters reuse.

## 6. Why future learning may not be priced

Let \(\tau\) be the period-one transfer from the owner to the provider. Negative
\(\tau\) means the provider pays for access to context. The contract imposes

\[
\tau\ge-\bar T s,
\]

where \(\bar T\) is the provider's maximum pledgeable payment per unit of
context. A low \(\bar T\) represents limited liability, uncertainty about the
value of learning, accounting restrictions, or the absence of a market in which
providers explicitly buy customer context.

For any disclosure and monitoring pair, let \(\widetilde U_O\) and
\(\widetilde U_P\) denote the parties' expected payoffs before the transfer. If
\(d_O^1\) and \(d_P^1\) are their initial outside options, a feasible contract
requires

\[
\max\{d_P^1-\widetilde U_P,-\bar T s\}
\le
\widetilde U_O-d_O^1.
\]

Generalized Nash bargaining selects the feasible transfer and contract with the
largest Nash product. Unlike the complete-contract benchmark, the payment cap
can make governance depend on the distribution of pre-transfer payoffs.

## 7. Governance regimes

The model distinguishes four outcomes:

1. **Secure modularity:** full disclosure and monitoring that deters reuse.
2. **Leaky modularity:** full disclosure, reuse, and enough provider-to-owner
   payment to sustain agreement.
3. **Strategic withholding:** partial disclosure because reuse cannot be fully
   deterred or priced.
4. **Ownership:** arm's-length trade fails and immediate integration dominates
   waiting.

The baseline comparative statics are:

- when enforcement capacity \(E\) exceeds the provider's future learning gain,
  secure modularity is feasible;
- with weak enforcement and cheap integration, the owner integrates;
- with weak enforcement, expensive integration, and little pricing capacity,
  the owner strategically withholds;
- with weak enforcement but enough pricing capacity, the provider can pay for
  learning rights and full but leaky modularity survives; and
- larger capability and provider-outside-option gains increase the monitoring
  required to make non-retention credible.

This produces the central result:

> Technological protection sustains modularity only when its enforceable
> deterrence capacity exceeds the provider's endogenous continuation gain. If
> it does not, modularity requires a credible market for learning rights;
> otherwise the equilibrium moves to withholding or ownership.

## 8. Interpretation

The model converts leakage from a static cost into a bargaining ratchet.
The provider may accept a low period-one price because reuse improves its
period-two capability and outside option. The owner anticipates the resulting
loss of scarcity and future leverage.

The simpler complete-contract benchmark is useful only as a comparison. It
assumes learning can always be priced or prevented. Comparing it with the
hidden-reuse model reveals a sign reversal:

- when learning is pledgeable, a larger provider learning gain can support
  trade through a larger payment for context;
- when learning is neither enforceably constrained nor pledgeable, the same
  learning gain raises the incentive to reuse and pushes the owner toward
  secrecy or integration.

That sign reversal is an empirically falsifiable expression of the
Arrow–Coase mechanism.

## 9. Scope of the result

These regimes describe the governance of one representative relationship, not
the concentration of the entire AI industry. The model takes the owner's and
provider's outside options as primitives rather than deriving them from
competition among many applications, models, or infrastructure providers. Its
purpose is to isolate the contracting mechanism that a larger industry model
would need to preserve.

The binary reuse choice also makes the deterrence boundary especially clear.
A continuous-reuse extension is the natural robustness test; it should smooth
the phase boundaries without removing the underlying incentive problem.

## 10. Reproduce the result

Generate the enforcement, integration-cost, and pricing-capacity phase maps:

~~~bash
python3 endogenous_scripts/generate_hidden_reuse_figures.py
~~~

Run the focused verification suite:

~~~bash
python3 -m pytest endogenous_tests/test_hidden_reuse.py
~~~

The implementation is in src/endogenous_context_game/hidden_reuse.py and the
generated results are written to hidden_reuse_outputs/.
