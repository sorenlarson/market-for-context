# When the Same AI Learning Network Becomes a Platform—or a Firm

> **Chapter extract:** This note isolates the heterogeneous
> platform-versus-rollup result. New readers should start with
> [The Market for Context](FULL-EXPOSITION.md), which defines the terms and
> derives all four results in sequence.

A large AI firm and a large AI platform can be built from the same raw material:
learning across many businesses.

The difference is whether the businesses must share an owner for that learning
to travel.

Imagine an AI intermediary serving clinics, laboratories, and insurers. A
laboratory result can improve a clinical decision. A clinical outcome can
improve a diagnostic system. Claims experience can improve both. One way to
combine those lessons is to buy the operating businesses. Another is to keep
them independent and connect them through contracts, shared technical
infrastructure, and permissioned learning.

The first organization is a rollup. The second is a platform.

My earlier notes supplied reasons for the rollup. A market contract can fail if
an outside AI provider secretly learns from a customer's private context, and a
larger owner can spread one AI system and useful operational learning across
several assets. But that argument omitted the platform alternative. If the
provider can obtain the useful learning by serving independent customers, it
does not need to buy the context factories merely to connect them.

This note adds that alternative—and changes the predicted firm boundary.

## The answer in one paragraph

Ownership has a learning advantage only for the part of learning that cannot
travel through an arm's-length customer relationship. Better data permissions,
interoperability, privacy-preserving infrastructure, and credible contracts can
therefore turn the same learning economy from a rollup into a platform. But
partial ownership introduces a second problem: after the intermediary buys one
customer's competitor, its remaining customers may no longer trust it as a
neutral supplier. When that conflict is strong, the middle becomes unstable.
The intermediary stays neutral and owns nothing, or it integrates the whole
learning network.

## Access is an alternative to ownership

Consider a learning opportunity from business $i$ to business $j$. Let its
full value be $\gamma_{ij}$.

Now define $q$ as the fraction of that value the AI intermediary can realize
while the two businesses remain independent customers.

- If $q=1$, contracts and technical access transmit the learning as well as
  ownership would.
- If $q=0$, that learning can be used across the two operations only if they
  share an owner.
- Values between zero and one describe incomplete permissions, lossy
  interfaces, privacy constraints, or learning that is hard to price and
  transfer.

The additional learning created by owning both businesses is not
$\gamma_{ij}$. It is

\[
(1-q)\gamma_{ij}.
\]

That small correction is the first result. A large learning opportunity does
not automatically support a large firm. It supports a large firm only when
access cannot reproduce it.

This is why “data network effects” are not by themselves a theory of firm size.
The same network effect can live inside one company or across a platform's
independent customers.

## Partial ownership can cost customer access

Suppose the intermediary starts as a neutral supplier to every clinic in a
market. It then buys one clinic.

The other clinics now face a different counterparty. Their AI supplier also owns
a competitor. Even with contractual safeguards, they may send less information,
move some work to another provider, or stop buying altogether. Similar conflicts
can arise when an AI intermediary owns a laboratory that sells to its other
customers, or an insurer that pays them.

Call the value of customer relationships put at risk by an ownership boundary
$D(S)$, where $S$ is the set of businesses acquired. Let $\chi$ be the
fraction of that value expected to be lost.

The private gain from acquiring $S$ can then be written as

\[
\Delta(S)=
\text{direct ownership gains}
+(1-q)\times\text{learning kept inside }S
-\text{organization cost}
-\chi D(S).
\]

The customer term has an unusual shape. It is zero when the intermediary owns
nothing, because it remains neutral. It is also zero when it owns the entire
network, because no customer relationship crosses its ownership boundary. The
term is largest in the middle.

So customer conflict does not simply favor small firms. It favors pure forms.

> A highly trusted intermediary may remain a platform until ownership creates
> enough additional learning value to justify integrating the whole network.

In the symmetric version of the model, one can calculate the exact level of
customer conflict above which every partial acquisition is dominated by either
the platform or the full rollup. Above that level, a single threshold in
external learning efficiency separates the two:

- low $q$: full rollup;
- high $q$: neutral platform.

Crossing the threshold can produce a jump from all assets owned to none, not a
gradual reduction in firm size.

![Customer access, customer conflict, and ownership regimes](outputs/ownership-access-regime-map.svg)

The horizontal axis measures how much useful learning can be achieved without
ownership. The vertical axis measures how much customer value partial ownership
places at risk. The dashed line compares the two pure forms.

At the top of each panel, customer conflict removes the partial structures. To
the left of the line, ownership unlocks enough otherwise inaccessible learning
to support a full rollup. To the right, customer access works well enough for a
neutral platform to win.

At the bottom, customer relationships are less sensitive to partial ownership,
so intermediate firms survive. The heterogeneous network on the right has a
larger middle because some assets are much more useful together than others.

## Asset types change which boundary is valuable

Treating every operating asset as interchangeable hid another important fact.
Learning is directional and type-specific.

A lab result may greatly improve a clinic's decision, while the clinic's outcome
provides a smaller but still useful lesson back to the lab. Two clinics may
share a workflow but little patient-specific context. An insurer may contribute
long-run outcome labels but create a difficult governance conflict. These are
different edges, not more units of one generic “data” stock.

The model therefore represents learning as a directed matrix. Each entry asks:

> How much does learning generated at this operation improve decisions at that
> operation?

This makes the topology of learning decisive. The next figure compares two
networks with the same six businesses, the same direct ownership values, the
same customer relationships, the same costs, and exactly the same total amount
of learning.

![The topology of learning changes firm boundaries](outputs/ownership-access-topology.svg)

Only the placement of the learning opportunities changes.

- When learning is spread across many complementary vertical links, external
  access is good enough and the intermediary remains a platform.
- When the same total learning is concentrated between businesses of the same
  type, owning the two clinics becomes profitable.

Aggregate learning is identical. The firm boundary is not.

That is a useful correction to the language of “data scale.” A pile of context
does not determine an efficient firm. What matters is a map of transfer: which
experience improves which decisions, by how much, under what governance.

## How this extends the cybernetic-rollup thesis

The combined argument now has four layers.

1. **Why might one relationship move inside a firm?** An outside provider can
   learn after the sale, and that future value may be impossible to deter or
   collect through a contract.
2. **Why might one owner acquire several assets?** A shared AI system and
   cross-asset learning can make joint ownership more valuable.
3. **Why might the same scale economy produce a platform instead?** The AI
   intermediary can sometimes learn across independent customers without buying
   them.
4. **Which assets should share a boundary?** The directed learning network and
   the customer relationships cut by ownership determine the answer.

This does not kill the rollup thesis. It gives it a sharper condition:

> Learning economies predict large integrated AI firms only when useful
> learning cannot travel through arm's-length customer relationships; when it
> can, the same economies support a platform.

That statement isolates learning and assumes the intermediary can monetize a
unit of value equally well through a service relationship or ownership. The
unified exposition then relaxes that assumption: a platform may reproduce the
learning and still lose to ownership if the operating value cannot be carried
back through its prices. The focused value-capture chapter is
[“Access Is Not Appropriation”](APPROPRIATION-DRAFT.md).

And the customer network adds a second condition:

> If partial ownership makes remaining customers distrust the intermediary,
> market structure may polarize between a neutral platform and a full rollup.

## What the code actually solves

The code uses one potential intermediary and six operating businesses. For any
chosen set of parameter values, it evaluates all (2^6=64) possible acquisition
sets, including buying nothing and buying everything.

For every set, it adds:

- the direct contracting benefit of owning each business;
- the extra learning available because particular pairs are now jointly owned;

and subtracts:

- the fixed cost of becoming an owner;
- organization and pair-specific coordination costs; and
- customer value put at risk where the ownership boundary cuts a directed
  buyer-supplier relationship.

It selects the highest-value set, reports every tied set, and verifies that no
other acquisition set is more profitable. The phase map repeats that exact
solution over a grid of external learning efficiency and customer conflict.

A separate synthetic robustness exercise perturbs every directed learning edge,
every customer edge, each node's direct ownership value, and organization cost,
then resolves all 64 choices. This tests whether the illustrated conclusions
survive nearby assumptions. In 600 fixed-seed draws, the three anchors retain
their predicted full-rollup, partial-rollup, and platform forms in 98.8, 97.3,
and 100 percent of cases, respectively. Those are local frequencies under the
stated synthetic perturbations, not estimates of real-world probabilities.

The reproducible artifacts are:

- the phase map in SVG and PNG;
- the topology comparison in SVG and PNG;
- a CSV containing every solved phase-map cell;
- a CSV containing robustness probabilities;
- JSON worked examples and run metadata;
- a command for solving one scenario; and
- tests of the analytical thresholds, topology counterexample, and exhaustive
  deviation check.

The technical model and proofs are in
[`OWNERSHIP-ACCESS-RESULT.md`](OWNERSHIP-ACCESS-RESULT.md). The implementation is
in
[`src/hidden_reuse/ownership_access.py`](src/hidden_reuse/ownership_access.py).

## What one would measure in the world

The model points toward more discriminating evidence than acquisition counts or
dataset size.

- **External learning efficiency:** compare task performance when learning is
  pooled under common ownership with performance under permissioned external
  access, federated learning, clean rooms, or portable evaluations.
- **Directed transfer:** train or update on outcomes from operation $i$, then
  measure the change in accepted outcomes at operation $j$. Repeat in both
  directions.
- **Customer neutrality:** measure whether customers reduce usage, information
  sharing, or renewal after their AI supplier acquires a vertically related
  business or a competitor.
- **Boundary composition:** test whether acquisitions follow the strongest
  directed learning edges rather than merely targeting the largest available
  datasets.

The strongest falsifier is straightforward. If independently owned customers
can transmit nearly all useful learning, yet ownership still follows the
learning network, the mechanism here is incomplete. Control of prices,
foreclosure, financing, regulation, or operational authority may be doing the
work instead.

## The contribution in one sentence

This model shows when the same cross-business AI learning economy produces a
neutral platform, a partial specialist, or an integrated rollup—and why valuable
customer relationships can eliminate the middle rather than simply make firms
smaller.

The result is theoretical. The numbers in the figures are transparent
normalizations, not estimates of current AI market structure.
