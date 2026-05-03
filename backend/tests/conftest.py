import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_evaluation():
    return {
        "nombre_establecimiento": "Test Restaurant",
        "fecha": "2026-05-01",
        "general_pct": 75.5,
        "pa_pct": 78.0,
        "po_pct": 73.0,
        "evaluaciones_pa": {"PLANEACIÓN": {"Analisis": 4}},
        "evaluaciones_po": {"LOGÍSTICA DE COMPRAS": {"Entrada": 3}}
    }