# How to interrogate the hidden-reuse model

> **Research companion:** This is not the public essay. Read
> [`FULL-EXPOSITION.md`](FULL-EXPOSITION.md) for the reader-facing argument. Use
> this guide to test scenarios, question assumptions, or work with the code.

Start here if you want to understand, challenge, or modify the result. The
phase diagram is an answer surface; this guide supplies the question it is
answering.

## The model in plain English

A context owner hires an AI provider.

Sharing more context improves today's service. But after seeing that context,
the provider may learn something it can use tomorrow. That learning can improve
the provider's capability, give it more leverage when the price is renegotiated,
and reduce the scarcity of the owner's information.

The owner therefore asks three questions before disclosing everything:

1. Can the provider be stopped from reusing the context?
2. If not, can enough future capability value be verified or secured for the
   provider to pay the owner?
3. If neither is possible, is it cheaper to reveal less or to integrate?

Those three questions generate the four main outcomes:

- **secure modularity:** disclose everything and credibly prevent reuse;
- **priced reuse:** disclose everything and charge the provider for reuse;
- **strategic withholding:** use the provider but reveal less;
- **ownership:** abandon the external contract and build or acquire the
  capability instead.

Later sections use two economics terms:

- An **outside option** is the fallback if a deal is not signed or renewed—for
  example, what the provider can earn from other customers or what the owner
  can earn by building the capability internally.
- An **arm's-length contract** is an ordinary market agreement between
  independent firms, as opposed to one firm owning the relevant activity.
- **Pledgeable value** is future value that can be credibly promised as a
  payment because it is either secured now or verifiable later.
- A **private signal** is information the provider sees before contracting
  about whether its own future capability value is likely to be high or low.

## The decision logic

Read any scenario from top to bottom.

### 1. Does the provider want to reuse the context?

`provider_reuse_gain_before_enforcement` is the provider's discounted future
gain from reuse, net of its direct reuse cost.

- If the value is zero or negative, reuse needs no deterrence.
- If it is positive, a zero-retention promise must change the provider's
  incentives.

### 2. Can reuse be deterred?

`required_monitoring_to_deter` is the minimum monitoring intensity needed under
the scenario's enforcement capacity. Monitoring runs from `0` (none) to `1`
(the maximum available).

- A value at or below `1` means deterrence is feasible.
- A value above `1` means even full monitoring is insufficient.
- Feasible deterrence can still be too expensive for the parties to choose.

This is the difference between a **feasibility boundary**—where an arrangement
becomes possible—and a **chosen-outcome boundary**—where it actually becomes
the preferred contract.

### 3. If reuse cannot be stopped, can it be priced?

The baseline `context_payment_cap` directly limits how much the provider can pay
per disclosed unit for permission to retain and benefit from what it learns.
It is useful for isolating the effect of payment capacity.

The extension derives that cap. If \(\mu\) is expected net capability value,
\(W\) is collateral, and \(\phi\) is the verifiable future-value share, then

\[
P^*=\min\{\mu,\;W+\phi\mu\}.
\]

`maximum_pledgeable_payment` is \(P^*\). `pledgeable_share` is \(P^*\) divided
by \(\mu\). `unpledgeable_expected_value` is the expected remainder that the
owner cannot collect even if the capability later becomes extremely valuable.

The reported `transfer_to_provider` uses the service-payment convention:

- positive: the owner pays the provider;
- negative: the provider pays the owner.

When a negative transfer reaches the allowed cap and
`payment_cap_binding` is true, the provider's ability to pay for reuse is
constraining the contract.

Use `scripts/solve_scenario.py` when you want to set the reduced-form cap
directly. Use `scripts/solve_pricing.py` when you want the model to derive it
from verifiability and collateral.

### 4. If full disclosure fails, what disciplines the relationship?

`integration_cost` determines how credible ownership is as the owner's
alternative.

- Low integration cost gives the owner an attractive fallback: build or buy the
  capability instead.
- High integration cost leaves the owner more likely to accept a partial
  contract or withhold completely.

### 5. What happens tomorrow?

`period_two_route` reports whether the owner renews, uses more than one provider
(multi-homes), builds or acquires the capability itself (integrates), or stops.
Reuse matters partly because it can change this route and partly because it
changes bargaining payoffs even when renewal continues.

## Four anchor cases

Run these from the package root. They differ in only the parameters needed to
isolate each mechanism.

### Ownership: weak enforcement and cheap integration

```bash
python3 scripts/solve_scenario.py \
  --enforcement 0.20 \
  --integration-cost 0.40 \
  --payment-cap 0
```

The owner rejects a contract between independent firms because building or
buying the capability is a better initial alternative.

### Strategic withholding: weak enforcement and expensive integration

```bash
python3 scripts/solve_scenario.py \
  --enforcement 0.20 \
  --integration-cost 0.80 \
  --payment-cap 0
```

The provider cannot be fully deterred or pay for permission to reuse what it
learns. The owner discloses about 60 percent of its context in the baseline
calibration.

### Priced reuse: let the provider pay for reuse

```bash
python3 scripts/solve_scenario.py \
  --enforcement 0.20 \
  --integration-cost 0.80 \
  --payment-cap 0.15
```

Nothing about enforcement or integration changes. Allowing the provider to pay
for context converts withholding into full disclosure with reuse.

### Endogenous price: ask where the payment capacity comes from

```bash
python3 scripts/solve_pricing.py \
  --verifiable-share 0.10 \
  --collateral 0.02
```

At the baseline expected learning value of 0.295, only 0.0495 can be pledged.
The result remains strategic withholding.

Now run:

```bash
python3 scripts/solve_pricing.py \
  --verifiable-share 0.50 \
  --collateral 0
```

Half the expected capability value can now be claimed through a verifiable
royalty. The endogenous cap is 0.1475 and the baseline moves to full disclosure
with priced reuse.

### Private signal: pool or screen

```bash
python3 scripts/solve_private_signal.py
```

The owner cannot see whether the provider's expected value is 0.15 or 0.45.
Under the default 30 percent chance of the high signal, it charges the low
financeable fee of 0.035 to both types. The high type keeps a large information
gain.

Now run:

```bash
python3 scripts/solve_private_signal.py --high-probability 0.90
```

The high type is now common enough that the owner posts the high fee and
excludes the low type. The provider still keeps the part of high value that is
not verifiable or secured.

### Secure modularity: make non-reuse credible

```bash
python3 scripts/solve_scenario.py \
  --enforcement 0.40 \
  --integration-cost 0.40 \
  --payment-cap 0
```

Monitoring is strong enough to deter reuse, so the owner fully discloses
without selling permission to reuse what the provider learns.

## The most useful comparisons

Do not vary every parameter at once. Hold two levers fixed and change one.

### Does enforcement preserve modularity?

Hold integration cost and payment capacity fixed. Increase `--enforcement`
from 0.20 to 0.40.

Look for:

- `required_monitoring_to_deter` falling below one;
- reuse moving from positive to zero;
- disclosure moving toward one; and
- the regime changing to secure modularity.

Then ask whether the switch occurs exactly at the deterrence threshold. It need
not: monitoring can be feasible before it is economically preferred.

### Can a price substitute for enforcement?

Hold enforcement at 0.20 and integration cost at 0.80. Increase
`--payment-cap` from zero to 0.15.

Look for:

- monitoring remaining zero;
- reuse remaining positive;
- disclosure rising to one;
- a negative transfer; and
- the payment cap binding.

This comparison isolates the market for permission to reuse what was learned.

Then replace the assumed payment cap with `solve_pricing.py`. Increase either
`--verifiable-share` or `--collateral` and check that:

- `maximum_pledgeable_payment` rises;
- `unpledgeable_expected_value` falls;
- the price never exceeds `expected_net_capability_value`; and
- enough pledgeability converts withholding to priced reuse.

Vary `--value-log-sigma` while holding the expected value fixed. Realized-value
quantiles change, but the risk-neutral expected payment ceiling does not. That
comparison separates uncertainty from unverifiability.

Then increase `--expected-value` while keeping verifiability and collateral
fixed. Once collateral is exhausted, pledgeable payment rises only at the
verifiable share while the hidden remainder grows faster.

For private information, vary `--high-probability`. Check when
`policy` changes from `pool_both_types` to `screen_high_type`, and compare the
offered fee with `high_type_rent_if_served`.

### When does provider learning reverse sign?

Increase `--provider-outside-gain` first with a positive payment cap and then
with a zero payment cap.

With payment capacity, a larger provider gain can help finance full exchange.
Without payment capacity, the same gain increases the deterrence requirement
and can push the owner toward withholding or ownership.

This is the model's most important contrast.

### Is ownership caused by leakage alone or by a credible alternative?

Hold enforcement weak and vary `--integration-cost`.

If lower integration cost moves the outcome from withholding to ownership, the
model is not saying that leakage mechanically causes acquisition. Leakage
weakens the contract; a credible integration alternative determines what
replaces it.

## How to challenge the result

Use these questions when reading the model or asking another AI to inspect it:

1. Which transition follows directly from the provider's incentives, and which
   depends on the illustrative parameter values?
2. Is the dotted line a feasibility boundary or an equilibrium-selection
   boundary?
3. Which assumption makes reuse binary, and would continuous reuse change the
   mechanism or only smooth the map?
4. Is future capability value unknown, unverifiable, unsecured, or all three?
   Which friction actually limits \(P^*\)?
5. Does the provider learn a private signal before signing? If so, does the
   owner pool types, screen out low-value trade, or need a richer mechanism?
6. Does provider learning create value for society even while eroding the
   owner's exclusive advantage?
7. What internal leakage, bureaucracy, financing, or capability cost is
   missing from ownership?
8. Which real-world measurements could distinguish enforcement capacity,
   payment capacity, and integration cost?
9. Could competition or using multiple providers prevent the incumbent's
   future bargaining advantage without monitoring?
10. Does a parameter change alter total value, who captures that value, or both?
11. Is a claimed market-structure prediction actually present in the two-party
    model, the homogeneous firm-size model, the single-intermediary
    heterogeneous network, or only a future competing-platform extension?

## How to interrogate the firm-size model

Read the firm-size section of
[FULL-EXPOSITION.md](FULL-EXPOSITION.md#result-ii-in-detail-integration-entry-and-firm-size-separate)
first and [FIRM-SIZE-RESULT.md](FIRM-SIZE-RESULT.md) when checking the theorem.

The size model asks a different question from the bilateral game. The bilateral
game produces a per-asset private internalization advantage \(A\). The scale
model compares that same advantage across firms owning one through \(N\)
homogeneous assets.

Start with these commands:

```bash
python3 scripts/solve_firm_size.py
python3 scripts/solve_firm_size.py \
  --derive-advantage-from-hidden-reuse \
  --enforcement 0.20
python3 scripts/solve_firm_size.py \
  --derive-advantage-from-hidden-reuse \
  --enforcement 0.80
```

Check five things in order:

1. What bilateral contract or fallback determines \(A\)?
2. What size maximizes surplus per asset **conditional on integration**?
3. Is the maximum surplus positive relative to modular contracting?
4. Is the reported target interior, tied, or constrained by the industry cap?
5. Does a claimed comparative static change entry, conditional size, or both?

The most revealing challenge is to vary only
`--internalization-advantage`. It should move the market across the modular
entry threshold without changing `conditional_target_size`. Then vary
`--cross-node-learning`, `--integration-cost`, or `--organization-cost`; those
parameters should change the size ranking itself. A higher sublinear
integration-cost scale raises the entry threshold but can increase conditional
size because larger firms spread execution capability more effectively;
ongoing organization cost reduces size.

Do not call `equilibrium_firm_size = 0` an optimal zero-sized firm. It means the
best integrated coalition cannot beat the normalized modular alternative. Do
not call a target at `max_firm_size` a finite optimum when
`industry_boundary_binding` is true.

## How to interrogate the ownership-access model

Read the platform-versus-rollup section of
[FULL-EXPOSITION.md](FULL-EXPOSITION.md#result-iii-in-detail-when-a-learning-network-becomes-a-platform-or-a-rollup)
first and [OWNERSHIP-ACCESS-RESULT.md](OWNERSHIP-ACCESS-RESULT.md) when checking
the theorems.

The network model asks whether useful learning requires ownership at all. Run:

```bash
python3 scripts/solve_ownership_access.py \
  --external-learning-efficiency 0.60 \
  --neutrality-penalty 0.10 \
  --show-candidates
```

The command evaluates all 64 acquisition subsets. For the chosen subset, check:

1. `internalization_value`: direct private gain from owning the selected nodes;
2. `learning_upgrade`: learning that ownership adds beyond customer access;
3. `organization_cost` and `coordination_cost`;
4. `boundary_customer_exposure` and the resulting `neutrality_loss`;
5. `selection_margin`: value over the best unchosen subset; and
6. `maximum_deviation_gain`, which must be zero.

Then vary only `--external-learning-efficiency`. Higher values mean that
permissioned relationships among independent customers carry more of the same
learning; they do not mean more hidden reuse. The maximum incremental value of
ownership must weakly fall.

Next vary only `--neutrality-penalty`. The platform and full rollup have no
cross-boundary customer links, so their relative values do not change. Partial
ownership loses value. This is why customer conflict can remove the middle
rather than simply select a smaller firm.

Finally compare:

```bash
python3 scripts/solve_ownership_access.py \
  --learning-topology complementary \
  --external-learning-efficiency 0.85
python3 scripts/solve_ownership_access.py \
  --learning-topology within_type \
  --external-learning-efficiency 0.85
```

The two networks have identical aggregate learning weight. The first remains a
platform; the second acquires both clinics. This is a topology counterexample,
not evidence about a measured healthcare network.

Do not call the solution a decentralized network equilibrium. It is the exact
private optimum for one intermediary that can compensate acquired nodes for
their independent fallbacks. Do not interpret the robustness probabilities as
empirical frequencies.

## How to interrogate the value-appropriation model

Read the value-capture section of
[FULL-EXPOSITION.md](FULL-EXPOSITION.md#result-iv-in-detail-learning-access-is-not-value-capture)
first and [APPROPRIATION-RESULT.md](APPROPRIATION-RESULT.md) when checking the
derivations.

Start with complete external learning and the Pareto (alpha=1.5) capture
benchmark:

```bash
python3 scripts/solve_appropriation.py \
  --external-learning 1.00 \
  --platform-capture 0.25 \
  --owner-capture 0.45 \
  --customer-conflict 5.00
```

The selected full rollup must report a zero
`productive_learning_upgrade`. Its positive private advantage comes from
`capture_upgrade`, direct internalization, and ownership costs. This is the
clean test that Result IV is not relabeling Result III's learning mechanism.

Next raise only `--platform-capture` to `0.40`. The neutral platform should win.
Higher service-price appropriation weakly lowers every ownership candidate's
incremental value.

Then lower `--customer-conflict` to zero. Partial ownership can survive because
outside customers remain learning sources. For a named network candidate,
inspect:

1. `owned_operating_surplus`: value realized at owned destinations;
2. `incoming_customer_learning`: learning imported from independent customers;
3. `capture_upgrade`: the ownership return on value already producible at
   platform-level learning;
4. `productive_learning_upgrade`: extra value created only because both ends of
   an edge are owned; and
5. `external_access_slope`: whether a marginal rise in lawful customer access
   raises or lowers this subset's ownership value.

Do not interpret the capture shares as welfare weights. They allocate private
claims. A firm can acquire an asset to improve appropriation even when the
acquisition creates no extra total value. Also do not treat the Pareto mapping
as a general optimal contract: it is a one-price monopoly benchmark.

Then pose the sharpest question the calibration invites: why should the owner
share exceed the platform share at all, when the same verifiability friction
that stops a provider from billing realized customer value should also let a
seller resist parting with prospective gains cheaply? The package's answer is
that the friction sits on opposite sides of the two markets: it suppresses the
charging party's collection, and the charging party is the AI firm in the
service market but the *seller* in the acquisition market. Test it directly:

```python
from hidden_reuse import CaptureShareFrictions, derive_capture_shares

symmetric = CaptureShareFrictions(
    service_verifiable_share=0.30, service_commitment_share=0.0,
    acquisition_verifiable_share=0.30, acquisition_commitment_share=0.0,
)
print(derive_capture_shares(symmetric))
```

Under symmetric frictions the wedge is positive exactly when the pledgeable
share of AI-created value is below one half. Raise the acquisition-side
verifiability (better diligence, earn-outs) above the service-side
verifiability and the wedge reverses: acquisition prices capitalize the gains
and the capture case for ownership disappears. If you believe real corporate
control markets verify prospective AI gains *better* than service contracts
verify realized ones, the capture-rollup region of the phase map is not about
your world.

## How to read the phase diagram

Only after working through the anchor cases, open the
[phase map](outputs/hidden-reuse-regime-map.svg).

- Move horizontally to ask what stronger enforcement changes.
- Move vertically to ask what a more expensive integration alternative
  changes.
- Move across panels to ask what changes when the provider can pay more for
  reuse.
- Treat the dotted curve only as the point where full-disclosure deterrence
  becomes technically and legally feasible.
- Use the CSV or scenario solver—not visual pixel positions—for numerical
  claims.

Then open the
[pledgeability map](outputs/capability-pledgeability-map.svg).

- Move horizontally to make more future value verifiable.
- Move vertically to add collateral that can be committed before realization.
- The dashed diagonal is where the entire expected value becomes pledgeable.
- The governance panel shows how that pricing constraint changes disclosure;
  it does not estimate real-world verifiability or collateral.

The [interactive explorer](outputs/hidden-reuse-explorer.html) is optional. It
is most useful after this decision logic is familiar and uses a coarser grid
than the authoritative static output.

## A prompt for another AI

> Read `INTERROGATE.md`, `RESULT.md`, `MODEL.md`,
> `FIRM-SIZE-RESULT.md`, `OWNERSHIP-ACCESS-RESULT.md`, and
> `APPROPRIATION-RESULT.md`. Explain one
> bilateral scenario by
> tracing, in order: expected capability value, its verifiable and secured
> shares, any provider private signal, the maximum pledgeable payment, whether
> the owner pools or screens types, the provider's reuse gain, deterrence
> feasibility, monitoring cost, each party's fallback if no deal is reached,
> chosen disclosure, transfer, and period-two route. Separate results that
> follow directly from the equations from those that depend on the illustrative
> parameter values. Then map its private internalization advantage into the
> firm-size model, explain separately whether integration occurs and which size
> maximizes surplus per asset, and test whether any other coalition can offer
> members more. State the homogeneous, transferable-utility, and replica-
> population assumptions. Then solve the ownership-access extension, distinguish
> permissioned external learning from hidden reuse, decompose the selected
> subset's value, and verify that no alternative subset is profitable. State
> the single-intermediary assumption and explain why equal aggregate learning
> need not imply equal firm boundaries. Finally solve the appropriation
> extension, separate capture from productive learning, test the (q=1) case,
> and determine whether incoming customer learning complements selective
> ownership. State why capture changes private organization without necessarily
> changing welfare. Do not describe any model or synthetic robustness
> probability as empirical evidence.
