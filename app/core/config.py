"""
Configuration Management Module
================================
Centralizes all application settings and environment variables.
Uses Pydantic's BaseSettings for automatic .env file loading and
environment variable parsing — ready for future Docker/CI integration.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application-wide settings loaded from environment / .env file."""

    # ── General ──────────────────────────────────────────────────────────
    APP_NAME: str = "Chart Validation & Objective Compliance System"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "DevSecOps-integrated API for validating chart data against "
        "objective compliance rules."
    )
    DEBUG: bool = True

    # ── Server ───────────────────────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ── Validation defaults ──────────────────────────────────────────────
    ALLOWED_CHART_TYPES: List[str] = ["bar", "line", "pie", "scatter", "histogram"]
    MIN_DATA_POINTS: int = 1

    # ── Future-ready placeholders ────────────────────────────────────────
    DATABASE_URL: str = "sqlite:///./chart_validation.db"
    SECRET_KEY: str = "change-me-in-production"
    CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton instance — import this everywhere
settings = Settings()
