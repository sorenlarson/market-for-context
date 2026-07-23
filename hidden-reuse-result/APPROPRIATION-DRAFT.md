# Access Is Not Appropriation

> **Chapter extract:** This note isolates the value-capture extension. It
> assumes the learning-access setup introduced earlier in the research. New
> readers should instead start with
> [The Market for Context](FULL-EXPOSITION.md), the single self-contained
> exposition of the entire argument.

Imagine an AI company serving six independent operating businesses.

The company learns from their work and improves their decisions. Suppose the
improvements create one hundred dollars of operating value. The AI company may
still collect only twenty-five dollars. Each business sees its own savings,
mistakes avoided, and revenue gained more clearly than the AI company does. It
can also switch providers, run a cheaper model, or simply decline to reveal how
valuable the service became.

Now suppose the AI company buys one of those businesses. An improvement at the
owned business no longer needs to be converted into a service invoice. It
appears in operating cash flow—the money the business keeps after paying its
costs.

That does not make ownership free. The acquirer must pay the seller, finance the
purchase, bear liability, and operate the business. Some expected AI gains may
already be included in the acquisition price. But ownership can still change
how much of the value the AI company retains.

This creates a second reason for an AI firm to own operating assets:

> It may acquire a business not because ownership produces better AI learning,
> but because ownership lets the firm receive more of the value that the same
> learning creates.

The distinction changes the earlier platform-versus-rollup result.

## Two things must travel through a customer relationship

The previous model asked whether **learning travels**. Can an AI provider learn
from independent customers and apply the result elsewhere, or must the
businesses share an owner?

That remains important, but it is only half the platform problem. A scalable
platform needs two things to travel:

1. useful learning must travel from customers into the shared system; and
2. some of the value created by that learning must travel back to the provider
   through prices.

The first is an access problem. The second is an appropriation problem—who gets
to keep the value that was created.

A provider may solve the access problem while failing the appropriation problem.
It can technically improve a customer's operation yet have no enforceable way
to say, “This saved you exactly $12.4 million, so you owe us 30 percent.” The
improvement may occur months later, depend on decisions made by the customer,
or be visible only inside the customer's accounts.

## What task pricing implies

My earlier essay
[“A Complexity Theory of AI Value Accrual”](https://hypersoren.xyz/posts/price-elasticity/)
describes task value with a Pareto distribution. The parameter \(\alpha\) says
how heavy the right tail is—how much exceptional value is concentrated in a
small number of tasks.

Under a deliberately favorable benchmark in which one provider sets one price,
its share of the net value produced on served tasks is

\[
\frac{\alpha-1}{2\alpha-1}.
\]

At \(\alpha=1.5\), the provider receives 25 percent and customers retain 75
percent. This does not mean every AI provider captures exactly one quarter. It
gives the firm-boundary model a disciplined reference point: valuable AI and
high provider margins do not imply that the provider receives most of the value
its product creates.

## The ownership decision in one line

For any set of businesses the intermediary might buy, the model calculates:

\[
\begin{aligned}
\text{advantage of ownership}
=\;&\text{value already producible but not collectible through prices}\\
&+\text{extra learning available only under common ownership}\\
&+\text{direct benefit of internalizing difficult contracts}\\
&-\text{acquisition, organization, and lost-customer costs}.
\end{aligned}
\]

The first line is new. The second line was the center of the previous
platform-versus-rollup result.

Keeping them separate matters. If learning travels perfectly but prices capture
little value, the first line can support a rollup by itself. If prices capture
value well but customer relationships transmit little learning, the second line
can support a rollup. A neutral platform requires both reasonably good learning
access and reasonably good value capture.

## The surprising hybrid

The interaction becomes more interesting when the intermediary buys some
businesses but continues serving others.

An outside customer can supply experience that improves an owned operation. The
customer remains independent, so the intermediary receives only a service fee
for value created at the customer. But when the same learning improves the
owned operation, the intermediary receives part of the operating cash flow.

In that case, customer access and ownership are complements:

- customers are sources of learning;
- owned businesses are destinations where learning produces cash flow.

Better access to customer learning can therefore increase selective ownership.
This is the reverse of the earlier learning-only result, where better customer
access always weakened the productive case for ownership.

The code contains an exact two-business example. One independent customer
supplies learning to one operating target. With no customer access, neither
business is purchased. With complete access, the intermediary buys only the
target. Ownership creates no additional learning; it changes where the value is
received.

## Why this hybrid may collapse

The strategy works only while outside customers continue trusting the
intermediary.

Suppose the AI provider buys a clinic while continuing to serve competing
clinics. Those customers may now reasonably ask whether their experience will
improve a competitor owned by their supplier. They can reveal less information,
reduce usage, or leave.

When that conflict is strong, partial ownership loses its learning sources. The
middle disappears and the choice becomes:

- remain a neutral platform that owns none of the operating businesses; or
- become a full rollup that owns the whole relevant network.

The same neutrality force appeared in the previous result. Value capture makes
the partial hybrid more attractive; customer conflict can make it unsustainable.

## What the calculation finds

The figure uses six otherwise similar operating assets. The horizontal axis is
the fraction of useful learning available while the assets remain independent.
The vertical axis is the share of AI-created operating value the platform can
collect through prices.

![Access and value appropriation phase map](outputs/value-appropriation-regime-map.svg)

The left panel assumes customer conflict is strong enough to rule out partial
ownership. The dashed curve compares a neutral platform with a full rollup.

- In the upper-right, learning travels and the provider captures enough value:
  the neutral platform wins.
- In the lower-left, neither travels well: the full rollup wins.
- Most importantly, the lower-right remains a rollup region. Learning travels
  perfectly there, but its value does not travel back through the service price.

The dotted horizontal line marks the \(\alpha=1.5\) task-pricing benchmark: a
25-percent provider share. Under the displayed normalization, a full rollup
still wins at that share even when all useful learning is available without
ownership. Its extra productive learning is exactly zero; the result is driven
by value capture, direct internalization, and ownership cost.

The right panel removes customer conflict. Partial platform-owner organizations
fill much of the middle because the intermediary can serve outside customers
while owning selected operating destinations.

These are theoretical regions, not estimates of today's AI industry. Their
purpose is to characterize the mechanism and identify what evidence would move
the boundaries.

## What the code actually does

For each point in the figure, the program considers a neutral platform, every
possible intermediate ownership size, and a full six-asset rollup. It computes
the private value of each organization and selects the largest. The general
network solver goes further: for \(N\) named businesses, it checks all
\(2^N\) possible acquisition sets, because two four-business firms can have the
same size but very different learning relationships.

For every candidate it separately records:

- operating value landing at owned businesses;
- learning imported from independent customers;
- learning newly unlocked inside the firm;
- value gained because ownership retains more than the service price;
- fixed, organization, coordination, and customer-conflict costs; and
- the gain from the best unchosen acquisition set.

The package also solves the Pareto pricing benchmark, repeats the phase-map
calculation under synthetic parameter perturbations, and verifies the analytical
boundaries in tests.

The generated artifacts are:

- the phase map in SVG and PNG;
- a CSV containing every solved phase-map cell;
- a CSV mapping Pareto tail parameters into prices, demand, provider profit,
  customer surplus, capture share, and pricing losses;
- JSON worked examples and run metadata;
- a synthetic sensitivity CSV;
- an optional interactive explorer; and
- a command-line solver for one scenario.

The technical derivation and proofs are in
[`APPROPRIATION-RESULT.md`](APPROPRIATION-RESULT.md). The computational source is
[`src/hidden_reuse/appropriation.py`](src/hidden_reuse/appropriation.py).

## What would distinguish this mechanism in the world

The most useful measurements concern where value originates, where learning
travels, and who gets paid.

1. Estimate the operating value customers attribute to an AI service and compare
   it with provider contribution profit. This measures platform capture.
2. Measure how much of an acquired business's AI improvement remains with the
   acquirer after the purchase premium, financing, liability, and lower output
   prices. This measures owner retention.
3. Train or update on experience from business \(i\), then test the change in
   accepted outcomes at business \(j\). This identifies the direction of
   learning.
4. Test whether AI acquisitions target businesses where outside-customer
   learning becomes valuable, not merely businesses that generate the most
   records.
5. Measure whether customers reduce usage or information sharing after their AI
   supplier buys a competitor or vertically related operation.

The strongest falsifier is equally direct. If providers can reliably charge for
the realized value they create, or if acquisition prices absorb nearly all
expected AI gains, ownership should not arise merely to improve value capture.

## What this adds to the rollup thesis

The previous result supplied a necessary qualification:

> Learning economies support a rollup only when useful learning cannot travel
> through independent customer relationships.

That statement was correct for the learning-only model but incomplete as a
general account of private firm boundaries. The extended result is:

> A platform requires both learning portability and value portability. When
> learning travels but its value cannot be priced, ownership can arise without
> any productive learning advantage. The intermediary may then combine outside
> customers as learning sources with owned operations as value-capture
> destinations—unless the conflict causes those customers to leave.

This does not say rollups are inevitable. The provider may capture value through
better contracts, the seller may demand the expected gain in the acquisition
price, operating competition may pass efficiency gains to consumers, or the
cost of ownership may dominate. It identifies the condition under which the
value-accrual argument changes the predicted organization.

## The contribution in one sentence

This model shows that an AI platform can reproduce a rollup's learning yet still
lose to ownership because the operating value it creates cannot be carried back
through service prices—and that customer learning can consequently feed, rather
than replace, selective vertical integration.
