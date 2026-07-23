"""Hayek–Arrow–Coase context game."""

from .model import Outcome, Primitives, Regime, solve
from .simulation import Heterogeneity, GridResult, simulate_grid

__all__ = [
    "GridResult",
    "Heterogeneity",
    "Outcome",
    "Primitives",
    "Regime",
    "simulate_grid",
    "solve",
]

