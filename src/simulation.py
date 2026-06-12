import numpy as np


def run_monte_carlo(
    current_savings,
    monthly_contribution,
    years_until_retirement,
    simulations=1000
):
    results = []

    for _ in range(simulations):
        wealth = current_savings

        for _ in range(years_until_retirement):
            annual_return = np.random.normal(0.07, 0.15)

            wealth += monthly_contribution * 12
            wealth *= (1 + annual_return)

        results.append(wealth)

    return results
