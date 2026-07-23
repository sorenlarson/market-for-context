"""Monte Carlo regime maps for the endogenous-protection bargaining game."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ContractHeterogeneity:
    """Mean-one lognormal dispersion in economically distinct initial states."""

    value_sigma: float = 0.20
    context_sigma: float = 0.30
    integration_sigma: float = 0.25
    protection_cost_sigma: float = 0.20

    def validate(self) -> None:
        if (
            min(
                self.value_sigma,
                self.context_sigma,
                self.integration_sigma,
                self.protection_cost_sigma,
            )
            < 0
        ):
            raise ValueError("heterogeneity sigmas cannot be negative")


@dataclass(frozen=True)
class ContractGridResult:
    leakages: np.ndarray
    integration_costs: np.ndarray
    modular_probability: np.ndarray
    withholding_probability: np.ndarray
    ownership_probability: np.ndarray
    no_trade_probability: np.ndarray
    agreement_probability: np.ndarray
    mean_disclosure: np.ndarray
    mean_context_use: np.ndarray
    mean_protection: np.ndarray
    mean_owner_payoff: np.ndarray
    mean_provider_payoff: np.ndarray
    mean_transfer_to_provider: np.ndarray


def _mean_one_lognormal(
    rng: np.random.Generator, sigma: float, size: int
) -> np.ndarray:
    if sigma == 0:
        return np.ones(size)
    return np.exp(sigma * rng.standard_normal(size) - 0.5 * sigma * sigma)


def simulate_contract_grid(
    leakages: np.ndarray,
    integration_costs: np.ndarray,
    *,
    protectability: float = 0.8,
    protection_cost: float = 0.4,
    provider_learning_share: float = 0.25,
    owner_bargaining_weight: float = 0.5,
    provider_outside_option: float = 0.0,
    marginal_value_at_full: float = 0.55,
    curvature: float = 0.45,
    context_rent: float = 1.0,
    draws: int = 10_000,
    seed: int = 7,
    heterogeneity: ContractHeterogeneity = ContractHeterogeneity(),
) -> ContractGridResult:
    """Estimate equilibrium regimes across heterogeneous initial conditions.

    Common random numbers are reused in every grid cell so counterfactual
    differences are not obscured by independent Monte Carlo noise.
    """

    if not 0 <= protectability <= 1:
        raise ValueError("protectability must lie in [0, 1]")
    if protection_cost < 0:
        raise ValueError("protection_cost cannot be negative")
    if not 0 <= provider_learning_share <= 1:
        raise ValueError("provider_learning_share must lie in [0, 1]")
    if not 0 <= owner_bargaining_weight <= 1:
        raise ValueError("owner_bargaining_weight must lie in [0, 1]")
    if provider_outside_option < 0:
        raise ValueError("provider_outside_option cannot be negative")
    if marginal_value_at_full <= 0 or curvature <= 0 or context_rent < 0:
        raise ValueError("value and curvature must be positive; rent nonnegative")
    if draws <= 0:
        raise ValueError("draws must be positive")
    heterogeneity.validate()

    leakages = np.asarray(leakages, dtype=float)
    integration_costs = np.asarray(integration_costs, dtype=float)
    if np.any((leakages < 0) | (leakages > 1)):
        raise ValueError("all leakages must lie in [0, 1]")
    if np.any(integration_costs < 0):
        raise ValueError("integration costs cannot be negative")

    rng = np.random.default_rng(seed)
    value_scale = _mean_one_lognormal(rng, heterogeneity.value_sigma, draws)
    context_scale = _mean_one_lognormal(rng, heterogeneity.context_sigma, draws)
    integration_scale = _mean_one_lognormal(rng, heterogeneity.integration_sigma, draws)
    protection_scale = _mean_one_lognormal(
        rng, heterogeneity.protection_cost_sigma, draws
    )

    m = marginal_value_at_full * value_scale
    c = curvature * value_scale
    full_internal = m + 0.5 * c
    owner_loss = context_rent * context_scale
    provider_learning = provider_learning_share * owner_loss
    dissipation = owner_loss - provider_learning
    unit_protection_cost = protection_cost * protection_scale

    shape = (integration_costs.size, leakages.size)
    modular = np.empty(shape)
    withholding = np.empty(shape)
    ownership = np.empty(shape)
    no_trade = np.empty(shape)
    agreement_probability = np.empty(shape)
    mean_disclosure = np.empty(shape)
    mean_context_use = np.empty(shape)
    mean_protection = np.empty(shape)
    mean_owner_payoff = np.empty(shape)
    mean_provider_payoff = np.empty(shape)
    mean_transfer = np.empty(shape)

    for row, base_integration_cost in enumerate(integration_costs):
        integrated = full_internal - base_integration_cost * integration_scale
        owner_outside = np.maximum(0.0, integrated)
        total_outside = owner_outside + provider_outside_option

        for col, leakage in enumerate(leakages):
            incentive = dissipation * leakage * protectability
            protection = np.zeros(draws)
            positive_cost = unit_protection_cost > 0
            np.divide(
                incentive,
                unit_protection_cost,
                out=protection,
                where=positive_cost,
            )
            protection = np.clip(protection, 0.0, 1.0)
            protection[(~positive_cost) & (incentive > 0)] = 1.0

            leak_after_protection = leakage * (1.0 - protectability * protection)
            friction = (
                dissipation * leak_after_protection
                + 0.5 * unit_protection_cost * protection * protection
            )
            disclosure = np.clip((m + c - friction) / c, 0.0, 1.0)
            gross = (m + c) * disclosure - 0.5 * c * disclosure * disclosure
            separated = np.maximum(0.0, gross - friction * disclosure)

            agreement = separated >= total_outside
            owns = (~agreement) & (integrated > 1e-12)
            shares_fully = agreement & (disclosure >= 1.0 - 1e-12)
            withholds = (~owns) & (~shares_fully)
            trades_nothing = (~agreement) & (~owns)

            surplus = np.maximum(0.0, separated - total_outside)
            owner_if_agreement = owner_outside + owner_bargaining_weight * surplus
            provider_if_agreement = (
                provider_outside_option + (1.0 - owner_bargaining_weight) * surplus
            )
            owner_payoff = np.where(
                agreement,
                owner_if_agreement,
                np.where(owns, integrated, 0.0),
            )
            provider_payoff = np.where(
                agreement,
                provider_if_agreement,
                provider_outside_option,
            )
            transfer = np.where(
                agreement,
                gross
                - owner_loss * leak_after_protection * disclosure
                - owner_if_agreement,
                0.0,
            )

            modular[row, col] = np.mean(shares_fully)
            withholding[row, col] = np.mean(withholds)
            ownership[row, col] = np.mean(owns)
            no_trade[row, col] = np.mean(trades_nothing)
            agreement_probability[row, col] = np.mean(agreement)
            mean_disclosure[row, col] = np.mean(np.where(agreement, disclosure, 0.0))
            mean_context_use[row, col] = np.mean(
                np.where(owns, 1.0, np.where(agreement, disclosure, 0.0))
            )
            mean_protection[row, col] = np.mean(
                np.where(agreement & (disclosure > 1e-12), protection, 0.0)
            )
            mean_owner_payoff[row, col] = np.mean(owner_payoff)
            mean_provider_payoff[row, col] = np.mean(provider_payoff)
            mean_transfer[row, col] = np.mean(transfer)

    return ContractGridResult(
        leakages=leakages,
        integration_costs=integration_costs,
        modular_probability=modular,
        withholding_probability=withholding,
        ownership_probability=ownership,
        no_trade_probability=no_trade,
        agreement_probability=agreement_probability,
        mean_disclosure=mean_disclosure,
        mean_context_use=mean_context_use,
        mean_protection=mean_protection,
        mean_owner_payoff=mean_owner_payoff,
        mean_provider_payoff=mean_provider_payoff,
        mean_transfer_to_provider=mean_transfer,
    )
