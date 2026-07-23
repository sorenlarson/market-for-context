# Second result: endogenous protection and bargaining

## 1. Why extend the baseline

The first model treated contractual protection as an exogenous reduction in
leakage. This extension makes protection a choice inside a two-party contract
and makes the context owner's integration option the disagreement point in
Nash bargaining.

The extension separates two consequences of disclosure that the reduced-form
model combined:

1. the context owner's private loss from diminished scarcity; and
2. the part of that loss captured by the model provider as reusable learning.

Only the difference is lost to the bargaining coalition. This distinction is
necessary once transfers are explicit.

## 2. Timing and payoffs

1. The context owner can withhold, integrate at fixed cost \(F\), or bargain
   with a model provider.
2. Under separation, the parties bargain over disclosure \(s\in[0,1]\),
   protection \(k\in[0,1]\), and a transfer \(\tau\) from the owner to the
   provider.
3. The agreed contract is executed and payoffs are realized.

Current benefit from using context remains

\[
B(s)=(m+c)s-\frac{c}{2}s^2.
\]

Let \(R\) be the owner's scarcity rent at risk and \(L\in[0,R]\) the learning
value captured by the provider. Protection can prevent at most fraction
\(\eta\in[0,1]\) of technological leakage \(\omega\), so residual leakage is

\[
\ell(k)=\omega(1-\eta k).
\]

Protection costs \(pk^2/2\) per unit of disclosed context. Individual payoffs
before disagreement options are

\[
u_O=B(s)-R\ell(k)s-\tau,
\]

\[
u_M=L\ell(k)s-\frac{p}{2}k^2s+\tau.
\]

Define genuine joint dissipation as

\[
D=R-L.
\]

The total value of an arm's-length contract is therefore

\[
W_S(s,k)=B(s)-s\left[D\omega(1-\eta k)+\frac{p}{2}k^2\right].
\]

## 3. Endogenous protection

For any positive disclosure, the contract chooses protection to minimize the
joint friction per disclosed unit. When \(p>0\),

\[
k^*=\min\left\{1,\frac{D\omega\eta}{p}\right\}.
\]

The resulting effective friction is

\[
a^*(D,\omega,\eta,p)=
\begin{cases}
D\omega-\dfrac{(D\omega\eta)^2}{2p},
&D\omega\eta\le p,\\[8pt]
D\omega(1-\eta)+\dfrac p2,
&D\omega\eta>p.
\end{cases}
\]

If protection is costless and useful, \(k^*=1\). If protection cannot prevent
leakage, or if all of the owner's loss is captured by the provider, the
joint-surplus-maximizing contract chooses \(k^*=0\).

After substituting \(a^*\), disclosure has the same closed form as in the first
result:

\[
s_S^*(a^*)=
\begin{cases}
1, & a^*\le m,\\[4pt]
\dfrac{m+c-a^*}{c}, & m<a^*<m+c,\\[8pt]
0, & a^*\ge m+c.
\end{cases}
\]

The optimized arm's-length value is

\[
W_S(a^*)=
\begin{cases}
m+\dfrac c2-a^*, & a^*\le m,\\[8pt]
\dfrac{(m+c-a^*)^2}{2c}, & m<a^*<m+c,\\[10pt]
0, & a^*\ge m+c.
\end{cases}
\]

## 4. Bargaining and governance equilibrium

Integration produces

\[
W_I=m+\frac c2-F.
\]

The owner's disagreement payoff is \(d_O=\max\{0,W_I\}\); let \(d_M\ge0\) be
the provider's outside option. An arm's-length agreement exists exactly when

\[
\Delta=W_S(a^*)-d_O-d_M\ge0.
\]

With owner bargaining weight \(\beta\in[0,1]\), generalized Nash bargaining
gives

\[
u_O=d_O+\beta\Delta,
\qquad
u_M=d_M+(1-\beta)\Delta.
\]

The transfer \(\tau\) implements those payoffs. It can be negative: when
provider learning is valuable enough, the provider pays for access to context
rather than charging for inference.

The equilibrium regimes are:

- **Ownership:** \(W_I>0\) and \(W_I+d_M>W_S(a^*)\).
- **Modular sharing:** agreement exists and \(a^*\le m\).
- **Strategic withholding:** agreement exists and \(a^*>m\), or bargaining
  fails while integration is unprofitable. The latter is the no-trade subtype.

With \(d_M=0\), the ownership boundary remains transparent:

\[
F<F^*_{\mathrm{contract}}=m+\frac c2-W_S(a^*).
\]

Protection no longer shifts the boundary mechanically. Its cost and
effectiveness determine an optimal \(k^*\), which determines \(a^*\), which in
turn determines both disclosure and the value of remaining modular.

## 5. Proposition and economic interpretation

Under transferable utility and complete contracting:

1. Lower protection cost \(p\) and greater protectability \(\eta\) weakly lower
   effective friction, weakly increase disclosure, and weakly reduce the set of
   integration costs that support ownership.
2. A larger provider learning value \(L\) reduces genuine joint dissipation.
   It lowers protection effort and can support more sharing because the owner
   can be compensated through the transfer.
3. Bargaining weight \(\beta\) changes prices and layer-level rent capture but
   not disclosure, protection, or governance.
4. A stronger provider outside option raises the surplus required for modular
   agreement and can tip the owner into integration.
5. When protection remains ineffective or expensive and integration is also
   expensive, the equilibrium is missing trade rather than modular exchange.

The third result is an important null prediction. If bargaining power changes
governance or disclosure in the data, some assumption in this benchmark is
failing: transfers may be constrained, future reuse may be unverifiable,
parties may invest before bargaining, or protection may alter capability.

## 6. What the Monte Carlo layer now measures

The simulation draws heterogeneous initial conditions in:

- current application value;
- private context rent;
- integration capability and cost; and
- protection cost.

For each draw and grid cell it solves the protection choice, disclosure choice,
agreement condition, Nash rent split, and governance choice. It records regime
probabilities, no-trade probability, agreement, disclosure, context use,
protection, owner and provider payoffs, and the transfer.

Common random numbers are reused across counterfactual grid cells. Differences
between two contractual environments therefore reflect parameters rather than
independent Monte Carlo noise.

## 7. Empirical implications to target next

- Confidential-compute or zero-retention rollouts should reduce integration
  pressure most where measured leakage risk is high and the technology is
  actually enforceable.
- Context owners should accept lower service prices, or receive payments, when
  providers retain more valuable learning rights.
- Bargaining-power shocks should move transfers but not governance in the
  complete-contract benchmark.
- Governance responses to bargaining-power shocks identify financial or
  contractual incompleteness omitted here.
- Observed protection effort identifies \(D\omega\eta/p\), while disclosure and
  ownership help identify the remaining effective friction. Leakage and
  protectability still require distinct sources of variation for separate
  identification.

## 8. Reproduce the result

Generate the deterministic comparison, Monte Carlo probabilities, CSV grid,
and run metadata with:

```bash
python3 endogenous_scripts/generate_figures.py
```

Run the focused verification suite with:

```bash
python3 -m pytest endogenous_tests/test_model.py
```

The implementation is in `src/endogenous_context_game/`. Generated artifacts
are written to `endogenous_outputs/`.
