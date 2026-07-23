# First result: when context moves from contract to secrecy to ownership

## 1. Environment

A context owner can disclose a fraction \(s\in[0,1]\) to an external model or
application provider. Current benefit is

\[
B(s)=(m+c)s-\frac{c}{2}s^2,
\qquad m>0,\;c>0.
\]

The parameterization makes \(B'(1)=m>0\), so full context use is optimal absent
Arrow friction.

Let

\[
a=R\omega(1-\kappa)
\]

be effective Arrow friction, where:

- \(R\) is the private rent attached to exclusive context;
- \(\omega\in[0,1]\) is the technological leakage/reuse rate; and
- \(\kappa\in[0,1]\) is contractual protection.

Under separation, the context owner chooses

\[
\max_{s\in[0,1]} B(s)-as.
\]

Ownership permits full internal context use without external leakage but costs
\(F\). Its value is

\[
W_I=B(1)-F=m+\frac{c}{2}-F.
\]

This is a reduced-form private-surplus model. Transfers between the parties are
suppressed; \(a\) represents value that escapes the potential coalition through
imitation, rival learning, or future price discrimination.

## 2. Arm's-length disclosure

Concavity gives

\[
s_S^*(a)=
\begin{cases}
1, & a\le m,\\[4pt]
\dfrac{m+c-a}{c}, & m<a<m+c,\\[8pt]
0, & a\ge m+c.
\end{cases}
\]

The corresponding value is

\[
W_S(a)=
\begin{cases}
m+\dfrac{c}{2}-a, & a\le m,\\[8pt]
\dfrac{(m+c-a)^2}{2c}, & m<a<m+c,\\[8pt]
0, & a\ge m+c.
\end{cases}
\]

This produces full modular sharing at low effective leakage, partial strategic
withholding at intermediate leakage, and complete withholding at sufficiently
high leakage—unless ownership dominates.

## 3. Ownership boundary

Define

\[
F^*(a)=B(1)-W_S(a).
\]

Then ownership is strictly preferred exactly when

\[
F<F^*(a).
\]

Expanding the threshold:

\[
F^*(a)=
\begin{cases}
a, & a\le m,\\[6pt]
m+\dfrac{c}{2}-\dfrac{(m+c-a)^2}{2c}, & m<a<m+c,\\[10pt]
m+\dfrac{c}{2}, & a\ge m+c.
\end{cases}
\]

### Proposition

Holding the value of context use fixed:

1. greater leakage \(\omega\) weakly reduces arm's-length disclosure and
   weakly raises the maximum integration cost consistent with ownership;
2. stronger contractual protection \(\kappa\) has the opposite effects;
3. higher integration cost \(F\) never increases ownership; and
4. high Arrow friction plus high integration cost creates a no-trade region in
   which valuable context is unused.

The fourth region is important: the alternative to vertical integration is not
always a healthy modular market. It can be missing trade.

## 4. Baseline regime classification

For each \((\omega,\kappa,F)\):

1. compute \(a=R\omega(1-\kappa)\);
2. compute the best separated disclosure \(s_S^*(a)\) and value \(W_S(a)\);
3. select ownership if \(B(1)-F>W_S(a)\);
4. otherwise call the outcome modular sharing if \(s_S^*=1\), and strategic
   withholding if \(s_S^*<1\).

Ties preserve separation, so ownership must generate a strict gain.

## 5. Identification and falsifiability

In the baseline, leakage and protection enter only through
\(\omega(1-\kappa)\). They are not separately identifiable from observed
disclosure and ownership alone. Distinguishing them empirically requires an
additional margin such as:

- direct compliance cost of stronger protection;
- detection probability and penalties for unauthorized reuse;
- protection that blocks socially valuable learning as well as appropriation;
- variation in legal enforceability holding technical leakage fixed; or
- variation in confidential-compute technology holding contracts fixed.

The result is not established by defining low disclosure as withholding and low
cost as ownership. It is falsified if, after measuring current context value,
ownership does not rise with the private leakage rent, or if stronger credible
non-use protections fail to support arm's-length disclosure and reduce
integration pressure.

Several assumptions are intentionally stark in this first pass:

- integration eliminates external leakage and has no separate residual-control
  synergy; internal reuse, employee mobility, and cross-business learning can
  be added as residual internal leakage;
- protection is costless and does not reduce model performance or add latency;
- the leakage term is a private coalition loss, although some leakage may be a
  transfer to suppliers or a social gain from diffusion;
- integration cost includes bureaucracy, liability, financing, and lost
  multi-homing; and
- licenses, joint ventures, clean rooms, staged disclosure, and relational
  contracts are represented only through the protection parameter.

These restrictions make the baseline comparative statics auditable. They should
be relaxed one at a time rather than hidden inside fitted residuals.

For empirical work, the primitives should be measured before the governance
choice wherever possible. Useful designs include vendor retention-policy
changes, confidential-compute rollouts, jurisdictional enforcement changes,
and financing shocks. Calibrating leakage or integration cost solely to explain
an observed acquisition would make the result tautological.

## 6. Monte Carlo extension

The initial simulation draws mean-one lognormal heterogeneity in:

- current application value;
- private context rent; and
- integration capability/cost.

The analytical choice is solved for every draw. The resulting phase diagram
reports the probability of each regime across heterogeneous initial conditions,
not merely the regime of an average firm.
