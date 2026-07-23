# Publishing handoff

## Default publication

- **Title:** The Market for Context
- **Subtitle:** How AI learning reshapes contracts, firm size, platforms, and
  value capture
- **Slug:** `market-for-context`
- **Author:** Soren Larson
- **Description:** A unified theoretical account of when private operating
  context supports secure AI contracting, paid learning rights, strategic
  secrecy, a neutral platform, selective ownership, or a full rollup—and what
  determines the size of the resulting firm.
- **Status label:** Theoretical model / calibrated computation

Publish [`FULL-EXPOSITION.md`](FULL-EXPOSITION.md) as one article. It is the
canonical public text and does not assume familiarity with any earlier result.
The four `*-DRAFT.md` files are optional chapter extracts for a future serialized
edition; they are not the default reader path.

Adapt the metadata syntax to the website's framework rather than copying a
generic frontmatter block.

## Content and assets

1. Use [`FULL-EXPOSITION.md`](FULL-EXPOSITION.md) as the article body.
2. Embed the six static SVGs where the draft places them:
   [Figure 1](outputs/hidden-reuse-regime-map.svg),
   [Figure 2](outputs/capability-pledgeability-map.svg),
   [Figure 3](outputs/firm-size-separation-map.svg),
   [Figure 4](outputs/ownership-access-regime-map.svg),
   [Figure 5](outputs/ownership-access-topology.svg), and
   [Figure 6](outputs/value-appropriation-regime-map.svg).
3. Copy the publication captions and full alt text from
   [`FIGURE.md`](FIGURE.md). The shorter captions in the article are not a
   substitute for accessible image descriptions.
4. The HTML explorers are optional supplements. Place them only after the
   relevant prose and static figure; never use a bare explorer as a reader
   entry point.
5. Link a public code repository containing this package if readers should be
   able to reproduce the calculations.
6. Preserve the theoretical-status warning and the claim limitations near the
   article and figures.

## Pre-publication checklist

- [ ] Choose the final code and text licenses. The current package reserves all
      rights.
- [ ] Confirm the release date and version in `CITATION.cff`.
- [ ] Preserve the phrase “calibrated theoretical computation” near the
      figures.
- [ ] Do not describe normalized parameters as estimates.
- [ ] Distinguish the dotted deterrence-feasibility curve from equilibrium
      selection.
- [ ] Describe \(P^*\) as a maximum pledgeable claim, not the unknowable
      realized “true price” of capability.
- [ ] Distinguish integration entry from conditional firm size and state the
      homogeneous transferable-utility replica assumptions.
- [ ] Distinguish declining marginal integration-execution cost from increasing
      ongoing coordination cost in the firm-size model.
- [ ] Do not turn an industry-boundary solution into a claim of a finite
      optimum.
- [ ] Describe the network result as a single-intermediary private acquisition
      equilibrium, not a welfare result or competing-platform equilibrium.
- [ ] Define external learning efficiency as permissioned or contractible
      learning across independent customers—not hidden reuse.
- [ ] Label the fixed-seed network perturbations as synthetic robustness, not
      empirical probabilities.
- [ ] In the value-capture section, distinguish the capture upgrade from
      productive learning and state that capture shares allocate private value
      rather than measure welfare.
- [ ] Describe the Pareto calculation as a single-price monopoly benchmark, not
      a general optimal contract or empirical estimate.
- [ ] State that the owner retained share is net of reduced-form acquisition
      capitalization and pass-through; ownership does not guarantee full value
      capture.
- [ ] Do not repeat the learning-only model's global access monotonicity after
      adding value capture: incoming customer learning can complement partial
      ownership.
- [ ] Verify that the website's math renderer supports the displayed equations
      and inline dollar-delimited math.
- [ ] Use the supplied alt text rather than the file name as the image
      description.
- [ ] Check the SVG, legend, tables, and equation wrapping on mobile.
- [ ] Run `make audit` from a clean environment.
- [ ] Test every external reference and public repository link.

## Optional serialized edition

If the website ultimately needs a series rather than one long article, divide
the unified exposition at its four numbered model sections. The older draft
files can supply additional chapter-level copy:

1. [`WEBSITE-DRAFT.md`](WEBSITE-DRAFT.md): bilateral hidden reuse and
   pledgeability;
2. [`FIRM-SIZE-DRAFT.md`](FIRM-SIZE-DRAFT.md): integration entry versus
   conditional size;
3. [`OWNERSHIP-ACCESS-DRAFT.md`](OWNERSHIP-ACCESS-DRAFT.md): platform access,
   customer conflict, and topology; and
4. [`APPROPRIATION-DRAFT.md`](APPROPRIATION-DRAFT.md): value capture.

Every serialized page should link first to the unified article so a reader
landing in the middle can recover the complete argument.

## Cold-AI handoff prompt

> Treat this directory as the complete source package for a theoretical result.
> Start with `FULL-EXPOSITION.md`; it is the canonical public article and must
> remain intelligible without prior conversation. Use `README.md` and
> `INTERROGATE.md` for package navigation, then check `RESULT.md`, `MODEL.md`,
> `FIRM-SIZE-RESULT.md`, `OWNERSHIP-ACCESS-RESULT.md`, and
> `APPROPRIATION-RESULT.md` for technical claims. Treat the four `*-DRAFT.md`
> files as optional chapter extracts, not prerequisites. Use `FIGURE.md` for
> accessibility and the modules under `src/hidden_reuse/` as the computational
> sources of truth. Do not treat the two-type posted price as a general optimal
> mechanism, extend the homogeneous size theorem to heterogeneous
> concentration, describe a single-intermediary acquisition solution as
> stack-wide general equilibrium, or confuse private value capture with social
> value creation. The Pareto result is a one-price benchmark. Run `make audit`
> before publishing changed text or numerical output.
