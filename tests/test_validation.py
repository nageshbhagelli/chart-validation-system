"""
Automated Tests for the Chart Validation API
=============================================
Run with:  pytest tests/ -v
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ─── Health Check ────────────────────────────────────────────────────────────

def test_root_endpoint():
    """GET / should return app info and healthy status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


# ─── Valid Chart ─────────────────────────────────────────────────────────────

def test_valid_chart():
    """A fully correct chart should score 100 and be valid."""
    payload = {
        "chart_type": "bar",
        "title": "Q1 Sales",
        "labels": ["Jan", "Feb", "Mar"],
        "data": [100, 200, 150],
        "objective": "Show monthly sales growth",
    }
    response = client.post("/validate-chart", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 100
    assert data["status"] == "valid"
    assert data["issues"] == []


# ─── Missing Data ────────────────────────────────────────────────────────────

def test_missing_data_field():
    """Missing data should deduct 25 points."""
    payload = {
        "chart_type": "line",
        "title": "Empty Chart",
        "labels": ["A", "B"],
        "objective": "Test objective",
    }
    response = client.post("/validate-chart", json=payload)
    data = response.json()
    assert data["score"] <= 75
    assert any("data" in issue.lower() for issue in data["issues"])


# ─── Invalid Chart Type ─────────────────────────────────────────────────────

def test_invalid_chart_type():
    """An unsupported chart_type should trigger an issue."""
    payload = {
        "chart_type": "radar",
        "title": "Bad Type",
        "labels": ["X"],
        "data": [10],
        "objective": "Testing invalid type",
    }
    response = client.post("/validate-chart", json=payload)
    data = response.json()
    assert any("chart type" in issue.lower() for issue in data["issues"])


# ─── Data-Label Mismatch ────────────────────────────────────────────────────

def test_data_label_mismatch():
    """Mismatched data/labels should deduct 20 points."""
    payload = {
        "chart_type": "pie",
        "title": "Mismatch",
        "labels": ["A", "B"],
        "data": [10, 20, 30],
        "objective": "Testing mismatch",
    }
    response = client.post("/validate-chart", json=payload)
    data = response.json()
    assert any("mismatch" in issue.lower() for issue in data["issues"])


# ─── Empty Payload ───────────────────────────────────────────────────────────

def test_empty_payload():
    """A fully empty payload should return 400."""
    response = client.post("/validate-chart", json={})
    assert response.status_code == 400


# ─── Non-Numeric Data ───────────────────────────────────────────────────────

def test_non_numeric_data():
    """Non-numeric data values should trigger a validation issue."""
    payload = {
        "chart_type": "bar",
        "title": "Bad Data",
        "labels": ["A", "B"],
        "data": [10, "not_a_number"],
        "objective": "Testing non-numeric data",
    }
    response = client.post("/validate-chart", json=payload)
    data = response.json()
    assert any("non-numeric" in issue.lower() for issue in data["issues"])


# ─── Missing Title ──────────────────────────────────────────────────────────

def test_missing_title():
    """A missing title should flag a minor issue (5-point deduction)."""
    payload = {
        "chart_type": "line",
        "labels": ["Q1", "Q2"],
        "data": [50, 75],
        "objective": "Revenue trend",
    }
    response = client.post("/validate-chart", json=payload)
    data = response.json()
    assert data["score"] == 95
    assert any("title" in issue.lower() for issue in data["issues"])
