# Cold-reader instructions

This directory is the canonical, self-contained package for the hidden-reuse
result.

1. For public exposition, start with `FULL-EXPOSITION.md`. It is the canonical
   self-contained article and the only document a new reader should need.
   Treat `WEBSITE-DRAFT.md`, `FIRM-SIZE-DRAFT.md`,
   `OWNERSHIP-ACCESS-DRAFT.md`, and `APPROPRIATION-DRAFT.md` as optional
   chapter extracts, not a required reading sequence. Use `INTERROGATE.md`,
   `RESULT.md`, `MODEL.md`, `FIRM-SIZE-RESULT.md`,
   `OWNERSHIP-ACCESS-RESULT.md`, and `APPROPRIATION-RESULT.md` as supporting
   research documents.
2. Treat `src/hidden_reuse/model.py`, `src/hidden_reuse/pledgeability.py`,
   `src/hidden_reuse/firm_size.py`,
   `src/hidden_reuse/ownership_access.py`, and
   `src/hidden_reuse/appropriation.py` as the computational sources of truth.
3. Describe the output as a calibrated theoretical computation, never as
   empirical evidence.
4. Use the canonical regime names: secure modularity, priced reuse, strategic
   withholding, and ownership. `LEAKY_MODULAR` exists only as a backward-
   compatible code alias for priced reuse.
5. Distinguish deterrence feasibility from equilibrium selection.
6. Run `make audit` before reporting that a change is complete.
7. Preserve five levels: bilateral context governance; homogeneous
   free-formation firm size; the single-intermediary heterogeneous
   ownership-access network; the value-appropriation extension; and a
   still-future general equilibrium with competing acquirers and stack-wide
   concentration.
8. Lead explanations with the unified article's decision logic and anchor
   scenario. Do not present an interactive HTML file or a chapter extract as
   the complete result without the surrounding argument in
   `FULL-EXPOSITION.md`.
9. Describe the private-signal result as a two-type posted-price benchmark, not
   a general optimal mechanism or auction equilibrium.
10. Describe the firm-size equilibrium as a homogeneous transferable-utility
    replica result. Do not silently extend it to heterogeneous or non-divisible
    finite industries.
11. Keep the size theorem's two margins separate: additive internalization
    advantage determines entry; fixed costs, transferable learning, declining
    marginal integration-execution cost, and increasing ongoing coordination
    cost determine conditional size.
12. Describe the ownership-access solution as an exact single-intermediary
    acquisition equilibrium, not a welfare optimum or a general equilibrium of
    competing platforms.
13. In the ownership-access model, distinguish directed learning
    `learning[i][j]` from directed customer dependence
    `customer_dependence[i][j]`. External learning efficiency `q` is
    permissioned or contractible access, not hidden reuse.
14. The fixed-seed ownership-access robustness draws are synthetic sensitivity
    evidence, not estimated probabilities about real markets.
15. In the appropriation model, distinguish productive learning from private
    capture. `platform_capture_share` and `owner_capture_share` divide private
    claims; they are not welfare weights, and ownership does not mechanically
    create surplus.
16. State that the Pareto task-pricing result is a single-price monopoly
    benchmark and that the owner retained share remains reduced form.
17. Do not repeat Result III's global monotonicity in external learning inside
    Result IV. With a capture wedge, incoming customer learning can complement
    selective ownership.
