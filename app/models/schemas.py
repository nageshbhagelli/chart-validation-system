"""
Pydantic Schemas (Data Models)
===============================
Defines the request and response contracts for the Chart Validation API.
Using strict Pydantic models guarantees automatic input validation,
clear error messages, and self-documenting Swagger/OpenAPI specs.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Any


# ─── Request Schema ──────────────────────────────────────────────────────────

class ChartData(BaseModel):
    """
    Incoming chart payload sent by the client.

    Example
    -------
    {
        "chart_type": "bar",
        "title": "Q1 Sales",
        "labels": ["Jan", "Feb", "Mar"],
        "data": [100, 200, 150],
        "objective": "Show monthly sales growth"
    }
    """

    chart_type: Optional[str] = Field(
        None,
        description="Type of chart (bar, line, pie, scatter, histogram).",
        examples=["bar", "line", "pie"],
    )
    title: Optional[str] = Field(
        None,
        description="Title / heading of the chart.",
        examples=["Quarterly Revenue"],
    )
    labels: Optional[List[str]] = Field(
        None,
        description="Category labels for each data point.",
        examples=[["Jan", "Feb", "Mar"]],
    )
    data: Optional[List[Any]] = Field(
        None,
        description="Numeric data values corresponding to each label.",
        examples=[[100, 200, 150]],
    )
    objective: Optional[str] = Field(
        None,
        description="The stated objective / purpose of the chart.",
        examples=["Show monthly sales trend"],
    )


# ─── Response Schemas ────────────────────────────────────────────────────────

class ValidationResult(BaseModel):
    """
    Structured response returned after chart validation.

    Fields
    ------
    score   : 0-100 — higher means fewer issues.
    issues  : human-readable list of problems found.
    status  : 'valid' when score >= 70, otherwise 'invalid'.
    """

    score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Validation score out of 100.",
    )
    issues: List[str] = Field(
        default_factory=list,
        description="List of validation issues detected.",
    )
    status: str = Field(
        ...,
        description="Overall validation verdict: 'valid' or 'invalid'.",
    )


class HealthResponse(BaseModel):
    """Response for the root health-check endpoint."""

    app: str
    version: str
    status: str
    message: str
