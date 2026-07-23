# The Market for Context

The canonical, self-contained publication package is
[`hidden-reuse-result/`](hidden-reuse-result/README.md). The single
reader-facing exposition is
[**The Market for Context**](hidden-reuse-result/FULL-EXPOSITION.md).

It introduces the bilateral hidden-reuse result and then develops firm size,
platform-versus-rollup boundaries, heterogeneous learning networks, and value
appropriation as one argument.

## Reproduce

```bash
cd hidden-reuse-result
python3 -m pip install -e .
python3 -m pytest
```

See [`hidden-reuse-result/README.md`](hidden-reuse-result/README.md) for the
full reproduction guide, figure regeneration, and package checks.

## Earlier exploratory models

The rest of the repository preserves earlier stages of the research for
provenance. None of it is required to understand or reproduce the
hidden-reuse result.

- **Hayek–Arrow–Coase context game** — the first-pass analytical and Monte
  Carlo model of modular sharing, strategic withholding, and ownership. The
  analytical note is [`notes/first-result.md`](notes/first-result.md), the
  implementation is in [`src/`](src), and
  `scripts/generate_phase_diagrams.py` regenerates `outputs/`.
- **Endogenous contracting extension** —
  [`ENDOGENOUS-CONTRACTING.md`](ENDOGENOUS-CONTRACTING.md), with code in
  `endogenous_scripts/` and tests in `endogenous_tests/`.
- **Hidden-reuse working notes** — [`HIDDEN-REUSE.md`](HIDDEN-REUSE.md).
