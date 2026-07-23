# Learning After the Sale

## Why AI context markets move from contracts to secrecy to ownership

> **Chapter extract:** This focused essay covers the bilateral hidden-reuse
> result. New readers seeking the complete argument should start with
> [The Market for Context](FULL-EXPOSITION.md), which also develops firm
> size, platform boundaries, heterogeneous learning, and value capture.

**Summary:** An AI provider does not only sell a service. After seeing a
customer's context, it may acquire a more valuable future capability. When that
learning cannot be credibly prohibited or priced, customers rationally disclose
less—or own the system that learns.

An AI provider sells an inference and buys an option.

The inference is familiar. A business shares customer history, workflow data,
private evaluations, or operating telemetry. The provider combines that
context with intelligence and returns something useful.

The option is easier to miss. By seeing the context, the provider may learn how
to serve the next customer, improve a model, or discover what makes the first
customer's operations distinctive. Even if that customer walks away, the
provider may now be able to earn more elsewhere. Economists call this fallback
an **outside option**: what a party can earn without renewing the deal.

The invoice prices the inference.

Who prices the option?

This is the hidden-reuse problem. It supplies a game-theoretic mechanism for a
claim I made in [Cybernetic Arbitrage](https://hypersoren.xyz/posts/cybernetic-arbitrage/):
when context cannot be cleanly intermediated, ownership of the assets that
generate it becomes more attractive.

The result is not that vertical integration always wins. It is more useful:

> A contract between independent firms survives when provider learning can
> either be controlled or exchanged. When it can be neither, the market moves
> toward secrecy or the firm.

## Context creates two products

Suppose a context owner hires an outside AI provider.

More disclosure improves the current service. The provider can route more
accurately, automate more of the workflow, or make a better decision. If this
were the only effect, the parties would share all useful context and divide the
surplus with a price.

But disclosure can also change the next game.

Once the provider has seen the owner's context, it may be able to:

- improve the service it sells to the owner's competitors;
- generalize private evaluations into model capability;
- infer the owner's willingness to pay;
- reduce its dependence on the owner in a renewal negotiation; or
- use the learned capability elsewhere even if the relationship ends.

The owner gets the current output. The provider may get a persistent state
change.

This is [Arrow's disclosure problem](https://www.nber.org/books-and-chapters/rate-and-direction-inventive-activity-economic-and-social-factors/economic-welfare-and-allocation-resources-invention)
with a clock attached. Information must be revealed to be used, but revelation
transfers some of the thing being transacted. It becomes
[Coase's problem](https://doi.org/10.1111/j.1468-0335.1937.tb00002.x) one period
later: after bargaining power has shifted, should the relationship still live
in the market, or should the owner have internalized it?

## A two-period game

The model has one context owner and one AI provider.

In period one:

1. they negotiate disclosure, monitoring, and price;
2. the owner reveals context and receives the current service; and
3. the provider privately decides whether to reuse what it saw.

In period two:

1. reuse may improve the provider's capability and what it can earn if renewal
   fails;
2. reuse may reduce the owner's exclusive context rent; and
3. the owner renews, uses more than one provider, builds or acquires the
   capability itself, or stops the activity.

Both parties understand this future when they sign the first contract.

The important hidden action happens between the two bargains. A contract may
say “zero retention,” but after disclosure the provider compares the future
value of learning with the expected consequence of getting caught.

## What the code actually solves

The code performs a deterministic equilibrium search. It does not simulate
LLM agents, estimate parameters from market data, or run Monte Carlo histories.

For each possible disclosure level, the solver:

1. calculates the second-period payoffs with and without provider reuse;
2. calculates the provider's private gain from reuse;
3. compares tolerated reuse with the minimum monitoring needed to prevent it;
4. solves for a price that makes both parties prefer the contract to their
   alternatives; and
5. selects the contract preferred by the model's bargaining rule—or selects
   withholding or ownership when no contract works.

The first phase diagram repeats that calculation over enforcement,
integration-cost, and payment-cap grids. For the second, the code first derives
the maximum pledgeable payment \(P^*\) from verifiability and collateral, then
feeds that payment limit back into the same contract solver. The private-signal
exercise analytically compares a low fee accepted by both provider types, a
high fee accepted only by the high-value type, and no trade.

The distribution of future capability value is used only to report transparent
value quantiles. Random draws do not determine any displayed governance regime.

## When is zero retention credible?

Let \(s\) be the amount of context disclosed and \(G(s)\) the provider's
discounted private gain from reusing it.

Let \(E\) be maximum enforcement capacity per reused unit. It compresses three
things that legal language often keeps separate:

- the probability that reuse is detected;
- the probability that a prohibition is enforced; and
- the maximum penalty that can actually be collected.

If monitoring intensity is \(k\), with zero meaning no oversight and one the
maximum available, the expected consequence of reuse is \(Eks\). The provider
honors non-reuse exactly when

\[
G(s)\le Eks.
\]

Because \(k\) cannot exceed one, full monitoring can deter reuse only if

\[
E\ge\frac{G(s)}{s}.
\]

That is the first result. Protection does not become credible because a
contract contains the right words or because confidential technology is
technically available. Its enforceable deterrence capacity must exceed the
provider's endogenous gain from learning.

In the illustrative baseline, the provider's gain from reusing full disclosure
is 0.295. Full non-reuse is therefore infeasible below an enforcement capacity
of roughly 0.295 at the default integration cost.

Even above that line, secure modularity is not automatic. Near the boundary,
deterrence requires intense monitoring. Monitoring can be feasible and still
cost more than another governance arrangement.

## Why not simply pay for learning?

Weak enforcement need not destroy the market.

If the provider gains 30 from learning while the owner loses 20, the obvious
contract is not “pretend learning will not happen.” It is “pay for the right to
learn.” Full disclosure with priced reuse can dominate an expensive effort to
prevent a jointly valuable spillover.

But that payment is not always available.

The mistake is to imagine a future “true value” that both parties can observe
and then divide. The capability may not exist when the contract is signed. Once
it does exist, its value may be visible only inside the provider: in lower
costs, better routing, stronger negotiations, or sales to other customers. The
context owner cannot collect a percentage of a number it cannot verify.

So the contract prices an expected claim, not the unknowable realized truth.

Let \(\mu\) be the provider's expected net value from the future capability.
Let \(W\) be cash or collateral it can commit before that value is known. Let
\(\phi\) be the share of future value that an auditor, court, or payment system
can verify and collect through a royalty.

The most the provider can credibly promise is

\[
P^*=\min\{\mu,\;W+\phi\mu\}.
\]

The first ceiling is willingness to pay: the provider will not promise more
than its expected gain. The second is enforceability: the owner can collect
only what is secured now plus the verifiable share later.

This distinction is easy to miss. Uncertainty alone does not make pricing
impossible. If both sides share a reasonable forecast, they can bargain over
the expectation. The harder problem is value that is both uncertain *and*
unverifiable after it arrives.

Suppose expected capability value is 0.295, but only 10 percent will be
verifiable and the provider can post 0.02 of collateral. The maximum credible
claim is only

\[
0.02+0.10(0.295)=0.0495.
\]

Roughly 83 percent of expected value remains outside the contract. The realized
capability could later be much more valuable; the owner still has no way to
enforce participation in the hidden remainder.

There is a sharper consequence. Once collateral is exhausted, each additional
unit of expected capability value adds only \(\phi\) to the enforceable price.
If 10 percent is verifiable, a dollar of extra expected learning supports ten
cents of extra payment and creates ninety cents of extra hidden value. Better
capability can widen the contracting problem instead of solving it.

Competition helps only up to this boundary. Rival providers may bid the price
toward \(P^*\). They cannot bid with value that none of them can credibly
promise.

There is another problem if the provider knows more before the contract is
signed.

Imagine it privately receives either a low or high signal about what the
context will teach it. The owner cannot observe the signal. It can charge a low
access fee that both types can finance, leaving the high type a large gain. Or
it can charge a high fee that screens out the low type and risk losing the deal.

In the model's simple example, the low and high expected values are 0.15 and
0.45, but only 10 percent is verifiable and 0.02 can be secured. Their maximum
financeable fees are 0.035 and 0.065. If the high signal occurs 30 percent of
the time, a fee of 0.035 paid by both types earns more than gambling on the high
fee:

\[
0.035>0.30(0.065).
\]

The owner pools the two types. A high-value provider pays 0.035 and keeps 0.415
in expected value. If the high signal becomes likely enough, the owner switches
to the high fee—but even then it can collect only 0.065, not the provider's
0.45 expectation.

Private information therefore creates a choice between leaving a hidden gain
and excluding trade. It does not create a mechanism for enforcing participation
in eventual true value.

This produces the second result:

> When reuse cannot be deterred, pledgeable value—not eventual true value—
> determines whether learning supports modular trade or destroys it.

## Four governance regimes

The model produces four outcomes.

**Secure modularity.** The owner discloses all context. Reuse is naturally
unprofitable or monitoring makes compliance more attractive than reuse.

**Priced reuse.** The owner discloses all context and permits reuse. The
provider pays for learning rights, directly or through a lower service price.

**Strategic withholding.** The owner reveals only part of its context—or, in
the limiting case, none. The lost current performance is the price of
preserving future scarcity.

**Ownership.** No contract between independent firms beats building or buying
the capability. The owner pays the fixed cost to use context internally rather
than teach a future counterparty.

![Governance regimes under hidden reuse](outputs/hidden-reuse-regime-map.svg)

The horizontal axis is maximum enforcement capacity. The vertical axis is
integration cost. Across the three panels, the provider becomes increasingly
able to pay for learning rights.

The right side is mostly secure modularity: enforcement can support non-reuse.
At the lower left, integration is cheap and enforcement weak, so ownership
wins. At the upper left, integration is too expensive to discipline the
relationship. With no market for learning rights, the owner withholds.

As payment capacity rises from left to right, priced reuse replaces much of the
withholding and some ownership.

The market is not saved by privacy alone. It can also be saved by a price.

The first figure treats payment capacity as a direct input. The next figure
opens that input and derives it from collateral and verifiable future value.

![Pledgeable future capability and context governance](outputs/capability-pledgeability-map.svg)

The left panel shows the fraction of expected capability value that can appear
in an enforceable claim. Below the dashed diagonal, some expected value remains
private and unsecured. The right panel feeds that limit into the hidden-reuse
game under weak enforcement and expensive integration. Low pledgeability
produces strategic withholding. Enough verifiable value or collateral restores
full disclosure with priced reuse.

## The sign reversal

Provider learning is often described as an uncomplicated benefit. Better
models, better service, more surplus.

The model shows why that conclusion depends on contractibility.

When learning can be priced, a larger provider gain can finance more context
exchange. The provider pays for the option it receives. Learning supports
modularity.

When learning is hidden, weakly enforceable, and cannot be committed as a
payment today, the same gain raises the incentive to reuse and increases what
the provider can earn if renewal fails. The owner shares less or integrates.
Learning destroys modularity.

The sign flips according to whether the learning right can be governed.

This is the economic hinge between Hayek and Coase.

[Hayek's Revenge](https://hypersoren.xyz/posts/hayeks-revenge/) argued that
valuable intelligence remains tied to the physics and economics of local
context. The hidden-reuse game adds that local context may also resist market
exchange. The context is useful precisely because it is scarce, but using it
through a foreign provider can train the party that will bargain over its value
tomorrow.

If you cannot contract over that state change, buying the context-generating
asset is not merely a data strategy. It is a response to a missing market.

## What we should observe

The model is theoretical, but it suggests measurable predictions.

Owners should demand stronger zero-retention, audit, on-premise, or
confidential-execution terms when learning transfers readily to competitors.

Credible improvements in enforcement should increase disclosure and reduce
integration pressure.

Explicit data-licensing or learning-right payments should preserve exchange
between independent firms when reuse is difficult to prevent.

Where providers cannot make those payments, greater learning value should have
the opposite effect: more withholding, self-hosting, or ownership.

Royalties should matter where future capability revenue is auditable.
Upfront access fees, bonds, or joint ownership should matter where the future
is hard to audit but providers can commit assets today.

And provider competition should raise owner payments much more when future
value is already verifiable or secured than when it remains private.

When verifiability is low, anticipated improvements in provider capability
should raise payments much less than one-for-one and may coincide with more
withholding.

Acquisitions should be most attractive where context rents are high,
learning is difficult to govern, and internal deployment is relatively cheap.

These are hypotheses, not findings from market data. The parameters in the
figure are normalized rather than estimated. The next empirical task is to
measure or bound them using retention-policy changes, confidential-compute
rollouts, differences in legal enforcement, and financing shocks.

## What the result does not say

The model does not show that every AI provider secretly trains on customer
data.

It does not show that ownership is socially optimal. Provider learning may
create valuable diffusion even while imposing a private loss on the context
owner.

It does not by itself generate industry concentration across applications,
model labs, and infrastructure. The model simply supplies each party with a
predefined fallback if the deal fails rather than deriving those alternatives
from competition. A homogeneous multi-asset sequel asks the narrower next
question—how many context-generating assets belong in one firm—without claiming
to solve the entire AI stack.

And it treats reuse as all-or-nothing. Continuous learning should smooth the
phase boundaries, though the incentive problem should remain.

The pricing extension assumes both parties share the same forecast before
signing. If the provider already knows more about its future value, adverse
selection can reduce the owner's payment further.

Those are important next tests. They do not change the present result:

> A technically available protection cannot sustain a modular market when the
> provider's future learning gain exceeds what can be credibly detected,
> punished, or purchased with verifiable value and secured claims.

The provider sells an inference and buys an option.

If the option cannot appear on the invoice, it may appear in the boundary of
the firm.

The complete argument continues in
[The Market for Context](FULL-EXPOSITION.md). The focused firm-size chapter
extract is
[“How Many Context Factories Should One AI Firm Own?”](FIRM-SIZE-DRAFT.md).
