"""
API Routes
==========
Defines all HTTP endpoints for the Chart Validation System.
Routes delegate work to the service layer — no business logic lives here.
"""

from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.models.schemas import ChartData, HealthResponse, ValidationResult
from app.services.validation_engine import validate_chart
from app.utils.helpers import timestamp_now

# Create a router instance with a descriptive prefix & tag for Swagger docs
router = APIRouter(tags=["Chart Validation"])


# ─── Root / Health-Check ─────────────────────────────────────────────────────

@router.get(
    "/",
    response_model=HealthResponse,
    summary="Health Check",
    description="Returns basic application info and health status.",
)
async def root() -> HealthResponse:
    """Root endpoint — useful for container liveness / readiness probes."""
    return HealthResponse(
        app=settings.APP_NAME,
        version=settings.APP_VERSION,
        status="healthy",
        message="Chart Validation API is running. Visit /docs for Swagger UI.",
    )


# ─── Chart Validation ────────────────────────────────────────────────────────

@router.post(
    "/validate-chart",
    response_model=ValidationResult,
    status_code=status.HTTP_200_OK,
    summary="Validate Chart Data",
    description=(
        "Accepts a JSON payload containing chart metadata and data, "
        "runs it through the rule-based validation engine, and returns "
        "a score, list of issues, and an overall pass/fail status."
    ),
)
async def validate_chart_endpoint(chart: ChartData) -> ValidationResult:
    """
    POST /validate-chart

    Accepts chart data and returns validation results.

    Raises
    ------
    HTTPException 400
        If the request body is completely empty or cannot be processed.
    """
    # Guard: reject a completely empty payload
    if all(
        value is None
        for value in [
            chart.chart_type,
            chart.title,
            chart.labels,
            chart.data,
            chart.objective,
        ]
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body is empty. Provide at least one chart field.",
        )

    # Delegate to the validation engine
    result: ValidationResult = validate_chart(chart)
    return result
