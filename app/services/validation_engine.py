"""
Validation Engine (Rule-Based)
===============================
The core business logic that evaluates incoming chart data against a
set of compliance rules.  Each rule is an independent function that
returns (points_deducted, issue_message | None).  This keeps the engine
easy to extend — just add a new rule function and register it.
"""

from typing import Any, Dict, List, Optional, Tuple

from app.core.config import settings
from app.models.schemas import ChartData, ValidationResult


# ─── Individual Rule Functions ───────────────────────────────────────────────
# Each rule receives the raw ChartData and returns:
#   (penalty: int, issue: Optional[str])
# If issue is None the rule passed.

def _check_data_presence(chart: ChartData) -> Tuple[int, Optional[str]]:
    """Rule 1 — Chart must contain data points."""
    if chart.data is None or len(chart.data) == 0:
        return 25, "Missing or empty 'data' field."
    return 0, None


def _check_chart_type(chart: ChartData) -> Tuple[int, Optional[str]]:
    """Rule 2 — chart_type must be one of the allowed types."""
    if chart.chart_type is None:
        return 15, "Missing 'chart_type' field."
    if chart.chart_type.lower() not in settings.ALLOWED_CHART_TYPES:
        allowed = ", ".join(settings.ALLOWED_CHART_TYPES)
        return 15, (
            f"Invalid chart type '{chart.chart_type}'. "
            f"Allowed types: {allowed}."
        )
    return 0, None


def _check_labels_existence(chart: ChartData) -> Tuple[int, Optional[str]]:
    """Rule 3 — Labels should be present."""
    if chart.labels is None or len(chart.labels) == 0:
        return 15, "Missing or empty 'labels' field."
    return 0, None


def _check_objective_existence(chart: ChartData) -> Tuple[int, Optional[str]]:
    """Rule 4 — An objective / purpose should be stated."""
    if chart.objective is None or chart.objective.strip() == "":
        return 10, "Missing or empty 'objective' field."
    return 0, None


def _check_data_label_consistency(chart: ChartData) -> Tuple[int, Optional[str]]:
    """Rule 5 — Number of data points must match number of labels."""
    if (
        chart.data is not None
        and chart.labels is not None
        and len(chart.data) != len(chart.labels)
    ):
        return 20, (
            f"Data-label length mismatch: {len(chart.data)} data points "
            f"vs {len(chart.labels)} labels."
        )
    return 0, None


def _check_title_presence(chart: ChartData) -> Tuple[int, Optional[str]]:
    """Rule 6 (BONUS) — A descriptive title improves chart clarity."""
    if chart.title is None or chart.title.strip() == "":
        return 5, "Missing 'title' field — charts should have a descriptive title."
    return 0, None


def _check_data_numeric(chart: ChartData) -> Tuple[int, Optional[str]]:
    """Rule 7 (BONUS) — All data values should be numeric."""
    if chart.data is not None:
        for idx, value in enumerate(chart.data):
            if not isinstance(value, (int, float)):
                return 10, (
                    f"Non-numeric value at data index {idx}: "
                    f"'{value}' (type {type(value).__name__})."
                )
    return 0, None


# ─── Rule Registry ───────────────────────────────────────────────────────────
# Add new rules here — order determines evaluation priority.

RULES = [
    _check_data_presence,
    _check_chart_type,
    _check_labels_existence,
    _check_objective_existence,
    _check_data_label_consistency,
    _check_title_presence,
    _check_data_numeric,
]


# ─── Public API ──────────────────────────────────────────────────────────────

def validate_chart(chart: ChartData) -> ValidationResult:
    """
    Run all registered rules against the supplied chart data.

    Returns a ``ValidationResult`` with:
    - score  : 100 minus accumulated penalties (clamped to 0).
    - issues : list of human-readable issue descriptions.
    - status : 'valid' if score >= 70, else 'invalid'.
    """
    total_penalty: int = 0
    issues: List[str] = []

    for rule_fn in RULES:
        penalty, issue = rule_fn(chart)
        total_penalty += penalty
        if issue is not None:
            issues.append(issue)

    # Clamp score between 0 and 100
    score = max(0, 100 - total_penalty)

    # Determine overall status
    status = "valid" if score >= 70 else "invalid"

    return ValidationResult(score=score, issues=issues, status=status)
