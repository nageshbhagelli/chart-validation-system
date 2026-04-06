"""
Application Entry Point
========================
Creates and configures the FastAPI application instance.
Run with:  uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import router


def create_app() -> FastAPI:
    """
    Application factory — builds and returns a fully configured FastAPI app.

    Using a factory function makes testing easier (you can create isolated
    app instances) and keeps global state minimal.
    """
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        docs_url="/docs",        # Swagger UI
        redoc_url="/redoc",      # ReDoc alternative
        openapi_url="/openapi.json",
    )

    # ── CORS Middleware ──────────────────────────────────────────────────
    # Allows the API to be consumed from any frontend origin.
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Register Routes ──────────────────────────────────────────────────
    application.include_router(router)

    return application


# Create the app instance — uvicorn looks for this symbol.
app = create_app()
