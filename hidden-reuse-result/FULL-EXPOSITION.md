# The Market for Context

## How AI learning reshapes contracts, firm size, platforms, and value capture

> **A self-contained exposition.** This article introduces the actors,
> vocabulary, models, results, and computations from the beginning. No earlier
> essay or repository context is required.

An AI provider does not merely sell an answer. By receiving the information
needed to produce that answer, it may also learn how to produce better answers
in the future.

That creates two economic flows in every context-rich AI relationship:

1. **Learning travels:** private operating context enters an AI system and may
   improve what the system can do elsewhere.
2. **Value travels:** some of the operating value created by the system returns
   to the AI provider through a price.

Neither flow is automatic. A clinic may be willing to use an outside diagnostic
system but unwilling to let the provider learn from its patient outcomes. Or it
may permit the learning while retaining most of the resulting savings because
the provider cannot observe or verify them. Common ownership changes both
flows: it can keep learning inside one organization, and it can turn an
uncollectible service benefit into operating cash flow.

The models in this article ask what organization follows. Does the owner share
all of its context, sell the right to learn from it, withhold part of it, or
bring the capability inside the firm? If ownership wins, should one firm own
one operating asset or many? Could an AI platform obtain the same learning by
serving independent customers? And can that platform charge for enough of the
value it creates to remain independent?

The combined answer is:

> AI context is governed by two incomplete markets: one for future learning
> and one for the operating value that learning creates. Gaps in the first
> market can produce secrecy or ownership; gaps in the second can produce
> ownership even when learning travels perfectly. Whether that ownership grows
> into a large rollup then depends on cross-asset learning, shared costs,
> organizational burden, and the customer relationships cut by the new firm
> boundary.

**Status: calibrated theoretical computation.** The result is supported by
analytical derivations and reproducible computations. The parameters in the
figures are transparent normalizations, not estimates of present AI markets.

## Four results at a glance

The organizational vocabulary is scaffolding, not the result. Within the
models' stated assumptions, the analysis establishes four propositions.

### Result I — hidden learning supports modularity through control or exchange

For disclosure $s>0$ and a positive provider gain from reuse $G(s)$, a
non-reuse promise is implementable if and only if enforcement capacity
satisfies

\[
E\ge\frac{G(s)}{s}.
\]

If reuse is permitted instead, the largest expected payment the provider can
credibly promise for the learning right is

\[
P^*=\min\{\mu,\;W+\phi\mu\},
\]

where $\mu$ is expected capability value, $W$ is secured collateral, and
$\phi$ is the fraction of future value that can be verified and collected.
When enforceability binds,

\[
\frac{\partial P^*}{\partial\mu}=\phi.
\]

An additional dollar of expected learning then supports only $\phi$ dollars of
additional compensation and creates $1-\phi$ dollars of additional hidden
value. More valuable learning can therefore support independent exchange when
it is contractible but intensify withholding or integration when it is not.

### Result II — the force that causes integration need not determine firm size

With homogeneous assets, surplus per asset can be written as

\[
g(n;A)=A+h(n),
\]

where $A$ is the same per-asset gain from internalizing the hidden-reuse
problem and $h(n)$ contains the scale forces. Consequently,

\[
\arg\max_n g(n;A)=\arg\max_n h(n).
\]

Changing $A$ can move the economy across the integration threshold, but it
cannot change the preferred size conditional on integration. Shared fixed
costs, transferable cross-asset learning, and organizational costs determine
that size. Thus an information-contracting reason for ownership is not, by
itself, a theory of concentration.

### Result III — customer access substitutes for ownership, while customer conflict can remove partial firms

Let $q$ be the fraction of cross-business learning available through
independent customer relationships, and let $\Gamma_I(S)$ be learning between
operations in a candidate ownership set $S$. In the learning-only model,

\[
\frac{\partial\Delta(S)}{\partial q}=-\Gamma_I(S)\le0.
\]

Better legitimate customer access weakly reduces every ownership candidate's
learning advantage. Once a neutral platform is optimal, it remains optimal as
$q$ rises. But partial ownership can jeopardize the intermediary's remaining
customer relationships. Above an exact customer-conflict threshold, every
partial structure is dominated; the equilibrium then jumps between a full
rollup and a neutral platform at the derived access threshold.

The heterogeneous-network calculation adds a constructive result: holding
total learning fixed while changing only which operations learn from which
others changes the exact equilibrium from a neutral platform to a specialized
clinic rollup. Aggregate data or aggregate learning is therefore not sufficient
to determine a firm boundary.

### Result IV — customer access can increase selective ownership once value capture is separated from learning

Let $p$ be the share of customer value captured through platform prices, $o$
the share retained at an owned operation, and $\Gamma_X(S)$ learning imported
from independent customers into owned operations. The value of a fixed partial
ownership set changes with customer access according to

\[
\frac{\partial\Delta(S)}{\partial q}
=(o-p)\Gamma_X(S)-p\Gamma_I(S).
\]

Customer access increases the value of selective ownership exactly when

\[
(o-p)\Gamma_X(S)>p\Gamma_I(S).
\]

Outside customers then become learning sources while owned operations become
the places where the intermediary captures the resulting value. This reversal
cannot strengthen a full rollup: a full rollup has no outside customers, so
$\Gamma_X=0$ and its ownership advantage weakly falls with $q$. Ownership can
nevertheless beat a platform even at $q=1$, when ownership creates no
additional learning, if the value-capture and direct internalization gains
exceed ownership costs.

The sharpest combined result is:

> Better external learning access weakens the case for a full rollup but can
> strengthen selective ownership by feeding learning from independent
> customers into owned operations. If those customers reject the conflict, the
> hybrid disappears and the organization polarizes between a neutral platform
> and a full rollup.

The evidentiary status of these claims differs:

| Object | What the package establishes |
|---|---|
| Analytical results | Incentive thresholds, maximum pledgeable payment, integration-entry/size separation, access and capture derivatives, and customer-conflict cutoffs |
| Exact constructions | A topology counterexample and a two-operation example in which better customer access induces selective ownership |
| Calibrated computations | Which regime wins at each displayed parameter cell and whether selected anchor cases survive nearby synthetic perturbations |
| Not established | The current empirical structure of AI markets, welfare optimality, or general equilibrium among competing AI firms |

## Model setup and organizational vocabulary

Imagine an AI intermediary serving several operating businesses: clinics,
laboratories, insurers, warehouses, or factories. Each business continually
generates **context**—local histories, exceptions, evaluations, outcomes, and
constraints that improve decisions when combined with an AI capability.

The AI activity is present in every organization. “Provider” and
“intermediary” are not different kinds of firm here: **provider** is the term
used when looking at one customer relationship, while **intermediary** is the
same AI-side role viewed across several customers.

The organizational labels then operate at two different zoom levels.

At the **relationship level**, ask about one operating business:

- The relationship is **modular** when the AI activity and that business remain
  under separate owners.
- The relationship is **integrated** when the AI activity and that business
  share an owner.

Consider one clinic building an AI diagnostic workflow:

- In the **modular** version, the clinic buys the context-bearing diagnostic
  service from an outside vendor. The vendor receives the clinic's histories
  and outcomes and controls the application, evaluations, retention, and
  learning process.
- In the **integrated** version, the clinic or its corporate parent owns and
  controls that diagnostic application, its context store, evaluations, and
  learning decisions. It can still purchase a foundation-model API—such as one
  supplied by OpenAI or Anthropic—or rent cloud infrastructure. That
  arrangement counts as integrated at this layer only insofar as those
  suppliers do not control or retain the strategically relevant context and
  learning loop.

The same stack can therefore be integrated at the application-and-operator
layer while remaining modular at the model and infrastructure layers. The
classification must always identify the particular AI activity whose access to
context and ability to learn are at issue. Integration can also occur in the
other direction: instead of the clinic bringing the application inside, the AI
vendor can acquire the clinic.

At the **network level**, ask how many operating businesses share the AI
activity's owner. Let $m$ be the number of relevant operating businesses and
$n$ the number owned by the firm controlling the AI activity:

| Owned businesses | Network-level description | Relationship-level description |
|---:|---|---|
| $n=0$ | **Neutral platform** | Every operating business has a modular relationship with the AI firm |
| $n=1<m$ | **Single-asset integration**; also a **platform-owner hybrid** if the AI firm continues serving the others | One relationship is integrated; the rest remain modular |
| $1<n<m$ | **Partial rollup**; also a **platform-owner hybrid** if the AI firm continues serving the others | Several relationships are integrated; the rest remain modular |
| $n=m=1$ | **Single-asset integrated firm** | The only relationship is integrated |
| $n=m>1$ | **Full rollup** | Every operating business is integrated with the AI activity |

For example, imagine one AI company serving six clinics. If it owns no clinics,
it is a neutral platform, and each clinic has a modular relationship with it.
If it buys one clinic but keeps serving the other five, the purchased clinic is
integrated and the overall company is a platform-owner hybrid. If it owns three
clinics and continues serving the other three, it is both a partial rollup and
a hybrid. If it owns all six, it is a full rollup.

A rollup therefore does have the AI activity inside the common firm. A rollup
is not an alternative to integration; it is integration applied to several
operating businesses. **Integration** answers “does this particular business
share the AI firm's boundary?” **Rollup** answers “how many businesses share
it?” A rollup can still buy models, compute, and infrastructure from outside
suppliers.

The word **equilibrium** has a deliberately concrete meaning here. Given the
model's prices, costs, learning opportunities, and customer relationships, the
selected organization is the one no modeled alternative can profitably replace.
The network computations check every possible acquisition set for one
intermediary. They do not claim to solve competition among all possible AI
firms.

The argument proceeds through four decisions:

| Decision | Economic question | Central force |
|---|---|---|
| Contract or own? | Can an independent provider be prevented from, or paid for, learning after the sale? | Enforcement and pledgeable payment |
| How large? | If ownership is worthwhile, how many operating assets should share one owner? | Shared fixed cost, transferable learning, and organization cost |
| Platform, hybrid, or rollup? | Can useful learning cross independent customer relationships, and will customers tolerate partial ownership? | External learning access and customer neutrality |
| Who captures value? | Can the platform charge for the operating value its learning creates? | Price-based capture versus owner-retained cash flow |

Each decision adds a missing margin without discarding the result before it.

## Result I in detail: controlling or pricing learning after the sale

Start with one context owner and one AI provider.

In the first period, they negotiate how much context will be disclosed, how
reuse will be monitored, and what the provider will pay or charge. The owner
then receives the current AI service. After seeing the context, the provider
privately decides whether to retain or reuse what it learned.

In the second period, that reuse may improve the provider's capability, reduce
the owner's exclusive advantage, and change the terms of renewal. The provider
may also be able to earn more from other customers if renewal fails. That
fallback—what it can earn without another agreement with this owner—is its
**outside option**.

Both parties anticipate the second period when negotiating the first. The
problem is therefore not merely unauthorized data retention. It is a hidden
investment in future capability and bargaining power.

### When a zero-retention promise changes behavior

Let $s\in[0,1]$ be the fraction of useful context disclosed, and let $G(s)$
be the provider's discounted private gain from reusing it.

Let $E$ be the maximum enforceable consequence per reused unit under full
monitoring. It combines three practical limits: the probability that reuse is
detected, the probability that a prohibition is enforced, and the largest
penalty that can actually be collected. If monitoring intensity is
$k\in[0,1]$, the expected consequence is $E k s$.

The provider complies with a non-reuse promise exactly when

\[
G(s)\le E k s.
\]

Even the strongest available monitoring cannot deter reuse unless

\[
E\ge \frac{G(s)}{s}.
\]

This is an incentive condition, not a drafting condition. A contract may say
“zero retention,” and a confidential-computing product may be available, yet
neither sustains independent trade if the provider's gain from learning still
exceeds the expected consequence of reuse. Deterrence can also be technically
feasible but too expensive to be the preferred arrangement.

### Learning can be sold instead of prohibited

Weak enforcement need not eliminate exchange. If provider learning creates
more value than it destroys for the context owner, the parties can permit reuse
and attach a payment to the learning right. The result is **priced reuse**:
full context is shared, the provider may learn, and the owner is compensated.

The difficult part is deciding how much compensation can be promised. The
future capability may not exist when the contract is signed. Once it exists,
its value may appear inside the provider as lower costs, better routing,
stronger renewal terms, or sales to other customers. The context owner cannot
collect a percentage of a value that it cannot verify.

Let

- $\mu$ be the provider's expected net value from the future capability;
- $W$ be cash, collateral, or another claim secured before that value is
  realized; and
- $\phi$ be the share of future value that an auditor, court, or payment
  system can verify and collect later.

The largest credible payment is

\[
P^*=\min\{\mu,\;W+\phi\mu\}.
\]

This collectible amount is the capability's **pledgeable value**: the part the
provider can credibly place behind a promise before the eventual value is
fully known. The concept is
[Holmström and Tirole's](https://doi.org/10.1162/003355397555316) pledgeable
income, applied here to the value of a learning right rather than to a
project's return.

The first ceiling is willingness to pay: the provider will not voluntarily
promise more than its expected gain. The second is enforceability: the owner
can collect only what is secured now plus the verifiable share later.

This clarifies the role of uncertainty. Unknown future capability can be priced
in expectation if both parties share a forecast. The sharper contracting
problem is value that becomes known only later and remains unverifiable after
it arrives.

For example, suppose expected learning value is 0.295, only 10 percent will be
verifiable, and the provider can secure 0.02 today. The most it can credibly
promise is

\[
0.02+0.10(0.295)=0.0495.
\]

More than four-fifths of expected value remains outside the contract. Rival
providers can compete the payment up toward 0.0495; competition cannot make the
hidden remainder collectible.

If the provider privately knows whether the opportunity is low- or high-value,
the owner faces an additional tradeoff. A low access fee serves both provider
types but leaves the high type a large gain. A high fee extracts more from the
high type but excludes the low type. The package solves this as a transparent
two-type posted-price benchmark, not as a general optimal auction or mechanism.

### Four governance regimes

The bilateral model produces four outcomes:

- **Secure modularity:** independent firms use all relevant context, and reuse
  is either unprofitable or credibly deterred.
- **Priced reuse:** independent firms use all context, reuse is permitted, and
  the provider pays for the learning right.
- **Strategic withholding:** the owner sacrifices current performance by
  revealing only some context—or none—to preserve future scarcity.
- **Ownership:** no independent contract beats building or acquiring the
  capability and using context internally.

![Governance regimes under hidden reuse](outputs/hidden-reuse-regime-map.svg)

**Figure 1. Governance under hidden reuse.** The horizontal axis is maximum
enforcement capacity and the vertical axis is integration cost. Across the
panels, the provider becomes increasingly able to pay for learning rights. The
dotted curve marks where full-disclosure deterrence becomes feasible; it is not
by itself an equilibrium boundary. Weak enforcement and cheap integration
support ownership. Weak enforcement and expensive integration support
withholding when learning cannot be priced. Greater payment capacity replaces
much of that withholding with priced reuse.

The next calculation derives payment capacity rather than assuming it.

![Pledgeable future capability and context governance](outputs/capability-pledgeability-map.svg)

**Figure 2. Pricing uncertain capability.** The left panel shows how much
expected future value is collectible as verifiability and collateral change.
The right panel feeds that payment limit into the hidden-reuse game. Under the
displayed weak-enforcement scenario, low pledgeability produces withholding;
enough collateral or verifiable value restores full disclosure with priced
reuse.

The first conclusion is therefore:

> Independent AI contracting survives when learning after the sale can be
> deterred or exchanged. When it can be neither, the owner chooses between
> revealing less context and owning the capability, according to the cost of
> integration.

This links three familiar ideas.
[Hayek](https://www.aeaweb.org/aer/top20/35.4.519-530.pdf) explains why
valuable knowledge begins locally.
[Arrow](https://www.nber.org/books-and-chapters/rate-and-direction-inventive-activity-economic-and-social-factors/economic-welfare-and-allocation-resources-invention)
explains why information can be difficult to sell without revealing it.
[Coase](https://doi.org/10.1111/j.1468-0335.1937.tb00002.x) explains why a
failed market can move an activity inside a firm. The model adds the dynamic
hinge: today's disclosure can change tomorrow's capability and bargaining
position. It formalizes the organizational mechanism behind
[“Hayek's Revenge”](https://hypersoren.xyz/posts/hayeks-revenge/) and
[“Cybernetic Arbitrage”](https://hypersoren.xyz/posts/cybernetic-arbitrage/).

The closest formal precursors deserve separate credit.
[Anton and Yao (2002)](https://doi.org/10.1111/1467-937X.t01-1-00020) derive
partial disclosure as the equilibrium way to sell an expropriable idea.
[Baccara (2007)](https://www.jstor.org/stable/25046303) shows that hidden
information leakage by an outside contractor can drive the choice between
outsourcing and in-house production.
[Holmström and Tirole (1997)](https://doi.org/10.1162/003355397555316) supply
the pledgeable-income logic behind the payment ceiling. What is added here is
the joint condition: the enforcement margin $E\ge G(s)/s$ and the
pledgeability of the learning right interact to select among the four
governance regimes, so the same learning hazard can end in secure contracting,
priced reuse, withholding, or ownership depending on which margin fails.

## Result II in detail: integration entry and firm size separate

The bilateral result explains why one operating activity may cross a firm
boundary. It does not explain why the resulting owner should acquire two
assets, twenty, or an entire industry.

Call each clinic, factory, laboratory, warehouse, or similar operation a
**context-generating asset**. It continually produces local observations and
feedback from real decisions. Let $A$ be the per-asset **internalization
advantage**: the private gain from owning that asset rather than using its best
independent AI contract. The hidden-reuse model can supply $A$, but scale
requires three additional forces:

- a shared AI platform or evaluation system has a fixed cost $K$;
- learning at one owned asset may improve other owned assets, with maximum
  strength $L$ and saturation rate $\kappa$; and
- financing, integration, liability, and bureaucracy have cost scale $c$ and
  become increasingly burdensome at rate $\eta$ as the firm grows.

For a firm owning $n$ otherwise similar assets, incremental value is

\[
V(n)=nA-K+nL\frac{n-1}{\kappa+n-1}-cn^{1+\eta}.
\]

The learning term grows and then saturates; the organization term is convex.
When potential owners compete for assets, the relevant value per asset is

\[
g(n)=A-\frac Kn+L\frac{n-1}{\kappa+n-1}-cn^\eta.
\]

An integrated firm chooses the integer size that maximizes $g(n)$, provided
that maximum beats the independent alternative.

The important feature is that $A$ enters as the same additive amount at every
size. Raising it moves the entire curve up. It can make integration profitable,
but it cannot change the location of the curve's maximum.

That separation is a characterization, not a free result: it holds if and only
if the advantage is size-independent. If owning more assets changes the
per-asset advantage itself—the solver exposes a diluted form $An^{-\zeta}$—the
entry and size margins interact, and a stronger contracting problem can buy
entry while shrinking the firm.
[FIRM-SIZE-RESULT.md](FIRM-SIZE-RESULT.md) reports a worked example.

Within the additive case, the model separates two margins:

> Hidden reuse determines whether integrated firms form. Shared fixed costs,
> transferable cross-asset learning, and convex organization costs determine
> their size after they form.

In the illustrative calibration, the scale terms make four assets the best
integrated size. Strong enforcement generates an internalization advantage of
0.430, too little for integration. Weak enforcement with unpriced reuse raises
it to 0.778, so four-asset firms form. The contracting shock changes entry from
no integrated firm to a four-asset firm; it does not itself select four.

![A phase map separating integration entry from conditional firm size](outputs/firm-size-separation-map.svg)

**Figure 3. Integration entry and conditional size.** The left panel varies
the internalization advantage and transferable learning. Moving horizontally
can cross the black integration boundary without changing firm size within a
row. The right panel isolates scale: stronger cross-asset learning supports
larger firms, while greater organization cost supports smaller ones.

This is also a negative result for simple concentration stories. An Arrowian
problem can create many small integrated operators if learning at one asset is
useless at the others. A rollup requires some scalable complementarity beyond
the contracting failure itself.

## Result III in detail: when a learning network becomes a platform or a rollup

The size model uses a polar assumption: transferable learning is available only
among commonly owned assets. But an intermediary might obtain permission to
learn across independent customers. A platform and a rollup can therefore
assemble the same knowledge network through different firm boundaries. The
question echoes
[Rajan and Zingales (1998)](https://doi.org/10.1162/003355398555630), who
treat regulated access to a critical resource as an alternative to ownership;
here the critical resource is the learning that independent customers can
legitimately transmit.

Let $q\in[0,1]$ be **external learning efficiency**: the fraction of useful
cross-business learning the intermediary can lawfully, technically, and
commercially realize while the businesses remain independent customers.

- $q=1$: customer access transmits learning as effectively as ownership.
- $q=0$: cross-business learning is usable only inside a common firm.

This permissioned learning is different from the hidden reuse in the first
model. Hidden reuse lowers the value of an independent contract. External
learning efficiency measures what an independent relationship can legitimately
deliver.

### Heterogeneous assets and directed learning

Operating assets need not be interchangeable. A laboratory result may improve
a clinic's decision; a clinical outcome may improve a diagnostic system; an
insurer may supply long-run outcome labels. The reverse effects may differ.

Let $\gamma_{ij}$ be the value of learning generated at operation $i$ when
applied at operation $j$. Learning is directed, so $\gamma_{ij}$ need not
equal $\gamma_{ji}$.

Suppose one intermediary initially serves every operation and may acquire a set
$S$. Relative to remaining a neutral platform, the private value of that
acquisition is

\[
\Delta(S)=
\sum_{i\in S}a_i
+(1-q)\Gamma_I(S)
-C(S)
-\chi D(\partial S).
\]

Here:

- $a_i$ is the direct internalization advantage of owning operation $i$;
- $\Gamma_I(S)$ is the sum of directed learning opportunities whose source
  and destination are both inside $S$;
- $C(S)$ includes fixed ownership, organization, and pair-specific
  coordination costs;
- $D(\partial S)$ is the value of customer or supplier relationships that
  cross the new ownership boundary; and
- $\chi$ measures how much of that relationship value partial ownership puts
  at risk.

The productive learning advantage of ownership is only
$(1-q)\Gamma_I(S)$. A large learning opportunity supports a large integrated
firm only to the extent that independent customer access cannot reproduce it.

### Why customer conflict can eliminate the middle

An intermediary that buys a clinic is no longer neutral when it sells AI
services to competing clinics. Those customers may reveal less, reduce usage,
or leave. The same conflict can arise when it buys a laboratory or insurer that
trades with its remaining customers.

The customer-conflict term is zero when the intermediary owns nothing: it is a
neutral platform. It is also zero when it owns the entire relevant network:
there is no outside customer relationship crossing the boundary. The term is
largest for partial ownership.

As a result, strong customer conflict does not necessarily make the firm
gradually smaller. It can eliminate intermediate structures altogether:

- when $q$ is low, a full rollup captures otherwise inaccessible learning;
- when $q$ is high, a neutral platform obtains the learning without
  ownership; and
- partial ownership survives only when its targeted benefits exceed both its
  organization costs and the customer relationships it jeopardizes.

![Customer access, customer conflict, and ownership regimes](outputs/ownership-access-regime-map.svg)

**Figure 4. Platform, partial rollup, or full rollup.** The horizontal axis is
learning available through independent customer relationships; the vertical
axis is customer value at risk from partial ownership. At the top, customer
conflict removes intermediate structures, leaving a full rollup on the left and
a neutral platform on the right. At the bottom, partial structures survive.
Heterogeneous assets create a wider middle because particular combinations are
more valuable than others.

Two specification choices favor this polarization, and the package stress-tests
both. The full rollup bears zero conflict only because the model's network is
closed; adding never-acquirable fringe customers taxes the rollup as well, yet
the all-or-nothing switch survives. The quadratic internal learning term is
convex in firm size and independently favors corners; replacing it with the
firm-size chapter's saturating learning form overturns the result at the
displayed conflict levels—high conflict then compresses partial ownership
rather than eliminating it. Polarization is therefore a prediction about
markets where cross-asset learning keeps compounding with scale, not a general
consequence of customer conflict. The computations are reported in
[OWNERSHIP-ACCESS-RESULT.md](OWNERSHIP-ACCESS-RESULT.md).

### Total learning does not determine the boundary

The location of learning opportunities matters as much as their sum. The next
calculation holds fixed the six businesses, direct ownership values, customer
relationships, organization costs, and total directed learning. It changes only
which operations learn from which others.

![The topology of learning changes firm boundaries](outputs/ownership-access-topology.svg)

**Figure 5. Equal aggregate learning, different firms.** When learning is
spread across complementary vertical links, independent access is sufficient
and the intermediary remains a platform. When the same total learning is
concentrated between the two clinics, the intermediary acquires those clinics.
Filled nodes are owned.

The third conclusion is:

> Learning economies support integrated AI firms only for learning that cannot
> travel through independent customer relationships. The pattern of learning
> determines which assets belong together, while customer distrust can
> polarize the market between a neutral platform and a full rollup.

## Result IV in detail: learning access is not value capture

An intermediary can solve the learning-access problem and still have a weak
business model.

Suppose its system creates one hundred dollars of operating value at a customer
but can collect only twenty-five dollars through the service price. The
customer observes its own avoided mistakes, savings, or additional revenue more
clearly than the provider does. It may switch providers, use a cheaper model,
or simply be unable to verify how much value the AI caused.

If the intermediary buys an operating business, an improvement no longer needs
to be converted into a service invoice. Some of it appears in the acquired
business's operating cash flow. The acquirer still pays the seller, finances
the transaction, bears liability, and may pass efficiency gains to the
business's customers. Ownership changes the claim on value; it does not make
the value free.

Define:

- $p$ as the share of AI-created operating value the intermediary captures
  through service prices; and
- $o$ as the share it retains at an owned operation after the acquisition
  price, seller bargaining, financing, liability, and output-price pass-through.

Neither share is a welfare weight, and $o$ need not equal one.

Neither share is a free calibration, either. Both are derived from the same
pledgeability logic that priced the learning right in Result I, applied to
opposite sides of two markets. In the service market the AI firm is the
charging party, so it collects only the committed and verifiable share of the
value it creates: $p=\min\{1,w_s+\phi_s\}$. In the market for corporate
control the *seller* is the charging party, so it capitalizes into the
acquisition price only the pledgeable share of prospective gains, leaving the
acquirer the remainder. Under symmetric frictions, $o$ exceeds $p$ exactly
when the pledgeable share of AI-created value is below one half—the same
one-half threshold that governed the bilateral pricing result. The capture
case for ownership is therefore a falsifiable claim about relative
verifiability across the two markets, not an assumption: if diligence and
earn-outs capitalize most expected AI gains, or outcome-contingent service
pricing improves, the wedge shrinks or reverses.

### A task-pricing benchmark

To discipline $p$, the package turns the task-value distribution in
[“A Complexity Theory of AI Value Accrual”](https://hypersoren.xyz/posts/price-elasticity/)
into a simple benchmark in which one provider posts one price. If task values
follow a Pareto distribution with tail parameter $\alpha>1$, the provider's
share of net value on served tasks is

\[
p(\alpha)=\frac{\alpha-1}{2\alpha-1}.
\]

The parameter $\alpha$ describes how concentrated value is in unusually
valuable tasks; lower values imply a heavier right tail.

At $\alpha=1.5$, the provider captures 25 percent and customers retain 75
percent. This is a single-price monopoly benchmark, not a universal prediction
or a claim that real AI providers capture exactly one quarter of value.

### Separating a capture upgrade from a learning upgrade

For a candidate acquisition set $S$, let

- $B(S)$ be baseline AI-created operating value at owned operations;
- $\Gamma_I(S)$ be learning between two owned operations; and
- $\Gamma_X(S)$ be learning imported from independent customers into owned
  operations.

The exact private acquisition value becomes

\[
\begin{aligned}
\Delta(S)=
&\sum_{j\in S}a_j \\
&+(o-p)\left[B(S)+q\bigl(\Gamma_I(S)+\Gamma_X(S)\bigr)\right] \\
&+o(1-q)\Gamma_I(S) \\
&-C(S)-\chi D(\partial S).
\end{aligned}
\]

The second line is the **capture upgrade**: value that independent customer
access could already produce but that ownership lets the intermediary retain
more readily. The third line is the **productive learning upgrade**: learning
that common ownership actually makes possible.

This decomposition yields two results that a learning-only account misses.

First, ownership can win even when $q=1$. In that case independent customer
relationships transmit all useful learning, so the productive learning upgrade
is zero. Ownership can still be privately attractive when the capture upgrade
and direct internalization gains exceed acquisition and organization costs.

Second, independent customers and selective ownership can become complements.
An outside customer supplies experience; that experience improves an owned
operation; and the intermediary receives the owner-side return where the value
lands. For a fixed partial acquisition set,

\[
\frac{\partial\Delta(S)}{\partial q}
=(o-p)\Gamma_X(S)-p\Gamma_I(S).
\]

Better customer access strengthens selective ownership exactly when the
capture gain on imported learning exceeds the platform revenue it would have
earned from internally sourced learning. Customers can be learning sources
while owned operations become value-capture destinations.

This complementarity does not apply to a full rollup, which has no outside
customers supplying incoming learning. And the hybrid can collapse if those
customers distrust a supplier that owns their competitor.

![Access and value appropriation phase map](outputs/value-appropriation-regime-map.svg)

**Figure 6. A platform requires learning access and value capture.** The
horizontal axis is the fraction of cross-business learning available without
ownership. The vertical axis is the provider's capture share through prices.
With high customer conflict in the left panel, partial ownership disappears.
The full-rollup region reaches the right edge: ownership can win even when
customer relationships transmit all useful learning. With low conflict in the
right panel, partial platform-owner hybrids occupy the middle. The dotted line
marks the 25-percent Pareto pricing benchmark.

The fourth conclusion is:

> A scalable AI platform requires two kinds of portability: useful learning
> must travel through customer relationships, and some of the value created by
> that learning must travel back through prices. If only learning travels, the
> intermediary may own the operations where value lands while retaining
> independent customers as learning sources—unless those customers reject the
> conflict.

## The complete decision logic

The four models now fit into one sequence.

| Question | If yes | If no |
|---|---|---|
| Can provider reuse be credibly deterred? | Full context can support secure modularity. | Ask whether the learning right can be priced. |
| Can the provider make a collectible payment for learning? | Full context can support priced reuse. | The owner withholds if integration is costly and owns if it is cheap enough. |
| Once ownership is viable, do shared costs and learning outweigh organization costs at additional assets? | A multi-asset firm or rollup forms. | Ownership remains local or does not form. |
| Can the same learning travel through legitimate customer access? | The productive case for ownership shrinks. | Common ownership has a learning advantage. |
| Can the platform charge for the value its learning creates? | A neutral platform becomes more viable. | Ownership can remain privately attractive even with perfect learning access. |
| Will remaining customers tolerate partial ownership? | A platform-owner hybrid can use customers as learning sources and owned assets as value destinations. | The market tends toward a neutral platform or full rollup. |

This sequence explains why “more AI learning” has no single implication for
market structure. Learning supports independent exchange when its rights and
value can be contracted. It supports ownership when disclosure creates hidden
future capability, when useful transfer requires common control, or when value
cannot return through a service price. It supports a neutral platform when both
learning and value cross independent relationships well.

It also separates three questions that are often conflated:

1. **Why does an activity cross a firm boundary?** Because the market cannot
   adequately govern future learning or distribute its value.
2. **Which assets share that boundary?** Those connected by valuable directed
   learning and tolerable coordination costs.
3. **How large is the firm?** Large enough to spread fixed costs and learning,
   but not so large that organization and customer conflict dominate.

## What the code solves—and what it produces

The package does not ask language-model agents to improvise strategies, and it
does not estimate the parameters from market data. It solves each stated model
directly.

| Computation | What is solved | Main outputs |
|---|---|---|
| Hidden reuse | For each disclosure level, second-period payoffs, the incentive to reuse, monitoring required for compliance, feasible transfers, and the preferred contract or ownership alternative | Governance phase map, complete solved grid, worked examples, interactive supplement |
| Capability pricing | Maximum collectible payment from expected value, verifiability, and collateral; plus a two-type posted-price comparison | Pledgeability map, solved grid, pricing examples |
| Homogeneous firm size | Total and per-asset surplus at every feasible integer size, integration entry, and the maximizing size conditional on entry | Entry/size phase map, two solved grids, bridge examples |
| Ownership access | Private value of every acquisition subset for one intermediary; with six nodes, all $2^6=64$ sets are checked | Platform/rollup phase map, topology counterexample, complete grid, exact deviation evidence |
| Value appropriation | Every acquisition subset with capture and productive-learning gains recorded separately, plus the Pareto pricing benchmark | Appropriation phase map, solved grid, Pareto table, worked examples |

The numerical records behind the figures are the
[bilateral regime grid](outputs/hidden-reuse-regime-grid.csv),
[pledgeability grid](outputs/capability-pledgeability-grid.csv),
[firm-entry](outputs/firm-size-entry-grid.csv) and
[firm-scale](outputs/firm-size-scale-grid.csv) grids,
[ownership-access grid](outputs/ownership-access-grid.csv), and
[value-appropriation grid](outputs/value-appropriation-grid.csv). The
[Pareto table](outputs/pareto-capture-benchmark.csv) exposes the task-pricing
calculation directly. JSON worked examples and run summaries record selected
scenarios, full calibrations, software versions, and seeds; the complete file
index is in [README.md](README.md#generated-outputs).

The phase maps repeat these solutions over transparent parameter grids. The
ownership-access and value-appropriation exercises also perturb the stated
calibrations with fixed random seeds and resolve every candidate organization.
Those frequencies are synthetic sensitivity checks—evidence that an
illustrative result survives nearby assumptions—not estimated probabilities of
real market structures.

In 600 nearby synthetic networks, the ownership-access model's full-rollup,
partial-rollup, and platform anchors retained their broad organizational forms
in 98.8, 97.3, and 100 percent of draws. In the value-capture extension, the
learning-rollup, full-access capture-rollup, neutral-platform, and partial-owner
anchors did so in 65.5, 67.5, 98.2, and 83.7 percent. The lower frequencies for
the two capture-rollup anchors correctly reveal that they lie nearer a regime
boundary; none of these percentages is an estimate of a real-world
probability.

The authoritative artifacts are static SVG figures and CSV files containing
the solved cells. The
[bilateral](outputs/hidden-reuse-explorer.html),
[ownership-access](outputs/ownership-access-explorer.html), and
[value-appropriation](outputs/value-appropriation-explorer.html) HTML explorers
use coarser grids and are optional aids, not standalone explanations or sources
for quoted numbers.

To regenerate and audit every result from the package root:

```bash
make audit
```

The technical statements, derivations, and source code are linked at the end of
this article.

## What evidence would distinguish the mechanisms

The theory becomes empirically useful only if its margins are measured
separately.

For the bilateral contract, measure whether retention rules actually change
provider behavior; what sanctions are detectable and collectible; how much
future capability revenue can be audited; and how much collateral a provider
can commit before learning occurs. Credible improvements in enforcement should
increase disclosure. Better pledgeability should replace withholding with
explicit learning-right payments.

For firm size, measure whether an outcome at operation $i$ improves accepted
decisions at operation $j$. A pure contracting shock should mainly change
whether integration occurs. A change in cross-asset transfer should change the
size and composition of already integrated firms.

For platform boundaries, map directed learning rather than total data volume.
Then measure whether customers reduce usage, disclosure, or renewal after their
AI provider buys a competitor, supplier, or buyer. High external learning
efficiency should favor platforms only when independent access is credible and
durable.

For value capture, compare the provider's contribution profit with operating
surplus customers attribute to the service. Separately estimate how much of an
acquired operation's improvement remains with the acquirer after the purchase
premium, financing, liability, and downstream price competition. If providers
can reliably charge for realized customer value, or sellers capitalize nearly
all expected AI gains into acquisition prices, ownership should not arise
merely to improve appropriation.

Several observations would falsify or redirect the theory:

- enforcement improves without increasing context disclosure or reducing
  ownership pressure;
- acquisitions expand even though learning does not transfer across the owned
  operations;
- independent customers transmit essentially all useful learning, yet
  ownership follows no value-capture or control advantage;
- partial ownership creates no measurable customer response in settings where
  neutrality is supposed to matter; or
- acquisition targets are unrelated to the destinations where outside learning
  creates valuable outcomes.

## Contribution and limits

Most of the building blocks here are established. Partial disclosure of an
expropriable idea is the equilibrium of
[Anton and Yao (2002)](https://doi.org/10.1111/1467-937X.t01-1-00020); hidden
leakage driving the make-or-buy choice is
[Baccara (2007)](https://www.jstor.org/stable/25046303); the payment ceiling
is [Holmström and Tirole's (1997)](https://doi.org/10.1162/003355397555316)
pledgeable income; access as an alternative to ownership is
[Rajan and Zingales (1998)](https://doi.org/10.1162/003355398555630); and the
data-markets literature—[Jones and Tonetti
(2020)](https://doi.org/10.1257/aer.20191330) on data hoarding,
[Bergemann and Bonatti
(2019)](https://doi.org/10.1146/annurev-economics-080315-015439) on priced
information, [Acemoglu, Makhdoumi, Malekian, and Ozdaglar
(2022)](https://doi.org/10.1257/mic.20200200) on leakage externalities—already
studies why firms withhold data and why its price understates its value. The
contribution here is not any single ingredient. It is connecting them in one
computable theory of AI context governance, from which four distinctions are
claimed as new:

1. future learning can be technically possible yet ungovernable because its
   gain exceeds deterrence and its value is not pledgeable;
2. the force that makes ownership worthwhile need not determine equilibrium
   firm size;
3. customer access substitutes for ownership only for the learning it can
   legitimately reproduce, and the topology of that learning selects the
   boundary; and
4. customer access can instead complement selective ownership when outside
   learning is monetized at owned destinations, because access and
   appropriation are separate margins.

In one sentence:

> This work derives when AI's use of private operating context produces secure
> contracting, paid learning rights, strategic secrecy, a neutral platform,
> selective ownership, or a full rollup—and separately shows which forces
> determine how large the resulting firm becomes.

The discipline matters as much as the claim. These models do not establish
that real providers secretly reuse customer data, that ownership maximizes
social welfare, or that AI rollups are inevitable. The bilateral game treats
reuse as binary and supplies rather than derives the parties' broader market
alternatives. The size theorem assumes many divisible copies of the same asset
and lets gains be transferred through prices. The network models contain one
potential intermediary, not competing acquirers or an equilibrium of the entire
model, application, and infrastructure stack. Customer conflict, platform
capture, and owner retention are supplied summaries rather than outcomes of
separate bargaining games. The models are static and do not yet let captured
profit finance the next round of model investment or acquisitions.

Those are boundaries on the present result, not hidden assumptions. They also
identify the next research program: acquisition bargaining, competing
intermediaries, endogenous customer prices and exit, and a dynamic capital loop
linking captured value to future capability and firm growth.

## Technical record and reproducibility

For readers who want proofs or implementation details:

- bilateral model and results: [RESULT.md](RESULT.md) and [MODEL.md](MODEL.md);
- homogeneous firm-size theorem: [FIRM-SIZE-RESULT.md](FIRM-SIZE-RESULT.md);
- heterogeneous platform-versus-rollup model:
  [OWNERSHIP-ACCESS-RESULT.md](OWNERSHIP-ACCESS-RESULT.md);
- value-appropriation extension: [APPROPRIATION-RESULT.md](APPROPRIATION-RESULT.md);
- computational sources: [src/hidden_reuse](src/hidden_reuse);
- figure captions and alt text: [FIGURE.md](FIGURE.md); and
- reproduction and package guide: [README.md](README.md).

The four narrower drafts—[WEBSITE-DRAFT.md](WEBSITE-DRAFT.md),
[FIRM-SIZE-DRAFT.md](FIRM-SIZE-DRAFT.md),
[OWNERSHIP-ACCESS-DRAFT.md](OWNERSHIP-ACCESS-DRAFT.md), and
[APPROPRIATION-DRAFT.md](APPROPRIATION-DRAFT.md)—are retained as chapter
extracts. They are no longer the reading path a new reader must assemble.
