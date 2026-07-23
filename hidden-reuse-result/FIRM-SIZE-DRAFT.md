# How Many Context Factories Should One AI Firm Own?

> **Chapter extract:** This note isolates the homogeneous firm-size result.
> New readers should start with
> [The Market for Context](FULL-EXPOSITION.md) for the complete argument from
> hidden reuse through platform boundaries and value capture.

The reason to own something is not yet a theory of how large its owner should
be.

That distinction matters for AI. A warehouse, clinic, laboratory, insurer, or
industrial site continually produces local information: exceptions, outcomes,
customer behavior, operating constraints, and feedback from real actions. Call
each one a **context-generating asset**.

My earlier argument was that a market contract can fail when an outside AI
provider learns from this context. The provider may become more capable, gain
leverage in the next negotiation, or reuse what it learned elsewhere. If that
future value cannot be prevented or paid back to the context owner, the owner
may share less information or bring the AI activity inside the firm.

That explains why one asset might cross a firm boundary. It does not explain
why the same firm should own four assets, forty assets, or an entire industry.
This note supplies the missing step.

## The answer in one paragraph

Hidden reuse determines whether ownership is worth considering. Firm size is a
different calculation. A larger owner can spread one AI platform across more
assets, transfer useful learning from one operation to another, and reuse an
integration playbook so successive acquisitions become cheaper to execute.
But ongoing coordination, bureaucracy, correlated liability, and loss of local
adaptation can eventually rise with scale. The equilibrium firm owns assets up
to the point where the scale economies no longer outweigh that ongoing burden.
If the hidden-reuse benefit is the same for every asset, it changes whether
firms form but not how large they should be.

That last sentence is the result.

## Two decisions that are easy to conflate

Suppose an asset has a good arm's-length option: it can hire an AI provider
without surrendering valuable future learning. Ownership then has little
special advantage.

Now weaken enforcement. The provider can privately reuse context, and the
asset cannot collect a meaningful share of the resulting future capability.
Ownership becomes more attractive because it keeps use, learning, and control
inside one boundary.

Call that per-asset gain \(A\), the **internalization advantage**. It is the
private value of full internal operation minus what the asset owner can earn
under its best remaining market arrangement.

The first decision is:

> Is \(A\) large enough for any integrated firm to beat modular contracting?

The second is:

> If it is, how many assets should share the same owner?

The first question is about hidden reuse and contracting. The second is about
scale.

## A small model of scale

Consider a firm with \(n\) otherwise similar context-generating assets. Its
incremental value is

\[
V(n)
=nA-K
+nL\frac{n-1}{\kappa+n-1}
-dn^\rho
-cn^{1+\eta}.
\]

The symbols correspond to four ordinary forces:

- \(nA\): owning each asset avoids the same contracting problem;
- \(K\): one shared AI platform, evaluation system, or operating layer has a
  fixed cost;
- \(L\): learning at one owned asset can improve other owned assets, although
  that benefit eventually saturates;
- \(dn^\rho\), with \(0<\rho<1\): cumulative integration-execution cost grows
  sublinearly because later integrations reuse systems and experience; and
- \(cn^{1+\eta}\): ongoing coordination becomes increasingly costly as the
  firm adds operations.

Potential firms compete for assets, so the relevant quantity is value per
asset:

\[
g(n)
=A-\frac Kn
+L\frac{n-1}{\kappa+n-1}
-dn^{\rho-1}
-cn^\eta.
\]

An equilibrium integrated firm chooses the size with the highest value per
asset. That lets it offer each asset more than any differently sized rival
coalition could offer.

Now notice what happens to \(A\). It appears once, as the same additive amount
at every candidate size. Raising it shifts the entire value-per-asset curve
upward. It can turn every integrated firm from unprofitable to profitable, but
it does not change which point on the curve is highest.

So:

> Hidden reuse can switch ownership on. Shared costs, transferable learning,
> integration experience, and ongoing coordination burden set the scale after
> it is on.

## A worked example

In the illustrative normalization, the scale terms make eight assets the best
integrated size. An integrated firm becomes viable only when the per-asset
internalization advantage exceeds \(0.482\).

The earlier two-period contracting model supplies three examples:

| Contracting environment | Internalization advantage | Outcome |
|---|---:|---|
| Strong enforcement | 0.430 | Assets remain separate |
| Weak enforcement; reuse cannot be priced | 0.778 | Eight-asset firms form |
| Weak enforcement; much future value is verifiable | 0.657 | Eight-asset firms form |

These values are theoretical outputs, not estimates of any real market. The
important point is their structure. Better enforcement lowers the private gain
from ownership enough to prevent integration. It does not turn the eight-asset
target into a two-asset target, because none of the scale terms changed.

![A phase map separating integration entry from conditional firm size](outputs/firm-size-separation-map.svg)

On the left, gray means market contracting remains viable and color means
integrated firms form. Moving horizontally raises the hidden-reuse advantage.
It crosses the black ownership boundary without changing the color within a
given row: conditional size is unchanged.

The right panel isolates the scale decision. More learning that transfers
across assets supports larger firms. The declining-marginal-cost integration
curve is held fixed, while greater ongoing coordination cost supports smaller
ones.

## What this changes about the rollup thesis

The cybernetic-rollup thesis says that capital will buy operating assets not
only for their current cash flow, but because they continuously regenerate the
context an AI system needs.

The model makes that thesis more precise—and less automatic.

There are now three separate claims:

1. **Why own?** Market contracting fails to control or price future learning.
2. **Why own several?** Learning, shared AI infrastructure, and a reusable
   integration capability transfer across assets.
3. **Why stop?** Ongoing coordination, bureaucracy, liability, and local
   heterogeneity eventually overwhelm those gains.

The first claim can be true while the second is false. If the knowledge learned
at warehouse A is useless at warehouses B through Z, hidden reuse may still
produce ownership, but it produces many local integrated operators rather than
a large rollup.

This is the useful negative result: **an Arrowian reason for firm boundaries is
not, by itself, a theory of concentration.** Large firms require an additional
scale mechanism.

## What one would look for in the world

The model suggests measuring the margins separately.

- A change in credible non-retention or enforcement should primarily affect
  whether assets integrate.
- A change in how well lessons transfer across sites should affect how many
  assets an integrated owner wants.
- Reusable diligence, financing, systems, and operating playbooks should lower
  marginal integration-execution cost and support larger firms.
- Higher ongoing coordination costs, liability, regulation, or losses of local
  adaptation should reduce firm size even if the original hidden-reuse problem
  remains.
- An acquirer claiming a data flywheel should be able to show that an outcome
  at one asset improves decisions at other assets. Merely pooling more records
  is not enough.

The sharpest falsifier is also simple. If a pure contracting or enforcement
shock changes the size of already-integrated firms, then the ownership benefit
was not additive. Perhaps a larger firm enforces secrecy more cheaply, bargains
more effectively with model providers, or learns more from each unit of
withheld context. In that case hidden reuse itself has scale economies, and the
next model must put them in explicitly.

## What the code does

The code does not release autonomous agents into a simulated economy. It solves
the stated equilibrium directly.

For every possible integer firm size, it computes total and per-asset surplus.
It identifies all sizes tied for the maximum, tests whether the maximum is
positive relative to modular contracting, and reports one of four outcomes:
modular market, standalone integration, finite rollup, or ownership at the
maximum feasible scale. The last label is a boundary warning, not a claim that
the displayed ceiling is naturally optimal.

It then sweeps two parameter grids:

- internalization advantage × transferable learning, to show the ownership
  entry boundary; and
- ongoing coordination cost × transferable learning, to show conditional firm
  size while holding the integration learning curve fixed.

The package produces an SVG, PNG, two CSV files containing every solved grid
cell, JSON worked examples, JSON run metadata, a single-scenario command, and
tests of the theorem and comparative statics. There is no Monte Carlo layer and
no empirical estimation in this result.

The technical statement and proof are in
[`FIRM-SIZE-RESULT.md`](FIRM-SIZE-RESULT.md). The full package starts at
[`README.md`](README.md).

## The contribution in one sentence

This model shows that hidden AI context reuse can determine whether operating
assets move inside firms, while the equilibrium number of assets per firm is
separately determined by shared fixed costs, cross-asset learning, declining
marginal integration cost, and increasing ongoing coordination cost.
