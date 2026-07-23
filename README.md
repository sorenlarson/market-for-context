# Hayek–Arrow–Coase context game

This repository contains a first-pass analytical and Monte Carlo model of the
choice among:

1. modular context sharing,
2. strategic withholding, and
3. ownership of the context-generating asset.

The baseline model is deliberately small. It isolates three forces:

- information leakage, which erodes the context owner's future exclusivity;
- contractual protection, which reduces effective leakage; and
- integration cost, which makes ownership an expensive substitute for market
  contracting.

The analytical characterization is in
[`notes/first-result.md`](notes/first-result.md). The implementation lives in
[`src/context_game`](src/context_game), with boundary tests in
[`tests/test_model.py`](tests/test_model.py).

## Run the first experiment

```bash
python3 -m pip install -e .
python3 scripts/generate_phase_diagrams.py
python3 -m pytest
```

This writes a deterministic regime map, Monte Carlo regime probabilities, and
the underlying grid to `outputs/`.

## Baseline interpretation

Let `s` be the fraction of context disclosed to an external model/application
counterparty. The context owner receives a concave current benefit from
disclosure but loses future exclusivity in proportion to effective Arrow
friction:

```text
effective friction = context rent × leakage × (1 − contractual protection)
```

The owner can instead integrate and use the full context internally, paying a
fixed integration cost. Monte Carlo draws vary initial context rent, application
value, and integration capability around the analytical benchmark. They do not
replace the equilibrium calculation; they estimate how frequently each regime
is selected across heterogeneous initial conditions.

