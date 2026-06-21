"""Small simulation helpers for the SmartRetireNL demo dashboard."""

from __future__ import annotations

import numpy as np


def build_demo_projection(seed: int = 42) -> dict:
    """Return mock retirement outcomes until real profiler input is connected."""
    rng = np.random.default_rng(seed)
    target_pot = 650_000
    outcomes = rng.normal(loc=610_000, scale=95_000, size=1_000)
    outcomes = np.clip(outcomes, 250_000, None)

    median_pot = float(np.median(outcomes))
    chance_of_target = float(np.mean(outcomes >= target_pot))
    pension_gap = max(0.0, target_pot - median_pot)
    risk_label = _risk_label(chance_of_target)

    return {
        "outcomes": outcomes,
        "target_pot": target_pot,
        "median_pot": median_pot,
        "chance_of_target": chance_of_target,
        "pension_gap": pension_gap,
        "risk_label": risk_label,
    }


def _risk_label(chance_of_target: float) -> str:
    if chance_of_target >= 0.75:
        return "Low risk"
    if chance_of_target >= 0.5:
        return "Moderate risk"
    return "High risk"
