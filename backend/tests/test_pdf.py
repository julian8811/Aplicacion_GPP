"""
Regression tests for PDF generation.
Tests that PDF generation doesn't crash and produces valid output.
"""
import pytest
from io import BytesIO
from app.pdf_generator import crear_pdf_auditoria


class TestPDFGeneration:
    """Test suite for PDF generation functionality."""

    def test_pdf_generation_does_not_crash(self, sample_evaluation):
        """Test that PDF generation completes without exceptions."""
        # Arrange
        resultados = {
            "general": {"porcentaje": sample_evaluation["general_pct"], "promedio": 4.0},
            "pa": {"porcentaje": sample_evaluation["pa_pct"]},
            "po": {"porcentaje": sample_evaluation["po_pct"]}
        }

        # Act - should not raise
        pdf_bytes = crear_pdf_auditoria(
            nombre_est=sample_evaluation["nombre_establecimiento"],
            fecha=sample_evaluation["fecha"],
            resultados=resultados,
            evals_pa=sample_evaluation["evaluaciones_pa"],
            evals_po=sample_evaluation["evaluaciones_po"],
            matriz_pa={},
            matriz_po={}
        )

        # Assert
        assert pdf_bytes is not None

    def test_pdf_has_content(self, sample_evaluation):
        """Test that PDF output has actual content (not empty)."""
        # Arrange
        resultados = {
            "general": {"porcentaje": sample_evaluation["general_pct"], "promedio": 4.0},
            "pa": {"porcentaje": sample_evaluation["pa_pct"]},
            "po": {"porcentaje": sample_evaluation["po_pct"]}
        }

        # Act
        pdf_bytes = crear_pdf_auditoria(
            nombre_est=sample_evaluation["nombre_establecimiento"],
            fecha=sample_evaluation["fecha"],
            resultados=resultados,
            evals_pa=sample_evaluation["evaluaciones_pa"],
            evals_po=sample_evaluation["evaluaciones_po"],
            matriz_pa={},
            matriz_po={}
        )

        # Assert
        assert isinstance(pdf_bytes, (bytes, bytearray))
        # Check it's not empty
        assert len(pdf_bytes) > 0

    def test_pdf_output_size_is_reasonable(self, sample_evaluation):
        """Test that output size is greater than 0 bytes (basic sanity check)."""
        # Arrange
        resultados = {
            "general": {"porcentaje": sample_evaluation["general_pct"], "promedio": 4.0},
            "pa": {"porcentaje": sample_evaluation["pa_pct"]},
            "po": {"porcentaje": sample_evaluation["po_pct"]}
        }

        # Act
        pdf_bytes = crear_pdf_auditoria(
            nombre_est=sample_evaluation["nombre_establecimiento"],
            fecha=sample_evaluation["fecha"],
            resultados=resultados,
            evals_pa=sample_evaluation["evaluaciones_pa"],
            evals_po=sample_evaluation["evaluaciones_po"],
            matriz_pa={},
            matriz_po={}
        )

        # Assert
        # A minimal PDF should be at least a few hundred bytes
        assert len(pdf_bytes) > 500, f"PDF seems too small: {len(pdf_bytes)} bytes"

    def test_pdf_starts_with_pdf_header(self, sample_evaluation):
        """Test that output starts with PDF magic bytes."""
        # Arrange
        resultados = {
            "general": {"porcentaje": sample_evaluation["general_pct"], "promedio": 4.0},
            "pa": {"porcentaje": sample_evaluation["pa_pct"]},
            "po": {"porcentaje": sample_evaluation["po_pct"]}
        }

        # Act
        pdf_bytes = crear_pdf_auditoria(
            nombre_est=sample_evaluation["nombre_establecimiento"],
            fecha=sample_evaluation["fecha"],
            resultados=resultados,
            evals_pa=sample_evaluation["evaluaciones_pa"],
            evals_po=sample_evaluation["evaluaciones_po"],
            matriz_pa={},
            matriz_po={}
        )

        # Assert - PDF files start with "%PDF"
        assert pdf_bytes[:4] == b"%PDF", "PDF should start with %PDF header"

    def test_pdf_can_be_read_as_bytes(self, sample_evaluation):
        """Test that PDF can be wrapped in BytesIO for further processing."""
        # Arrange
        resultados = {
            "general": {"porcentaje": sample_evaluation["general_pct"], "promedio": 4.0},
            "pa": {"porcentaje": sample_evaluation["pa_pct"]},
            "po": {"porcentaje": sample_evaluation["po_pct"]}
        }

        # Act
        pdf_bytes = crear_pdf_auditoria(
            nombre_est=sample_evaluation["nombre_establecimiento"],
            fecha=sample_evaluation["fecha"],
            resultados=resultados,
            evals_pa=sample_evaluation["evaluaciones_pa"],
            evals_po=sample_evaluation["evaluaciones_po"],
            matriz_pa={},
            matriz_po={}
        )

        # Assert - should be readable as BytesIO
        buffer = BytesIO(pdf_bytes)
        buffer.seek(0)
        content = buffer.read()
        assert len(content) == len(pdf_bytes)

    def test_pdf_with_different_percentage_ranges(self):
        """Test PDF generation across different percentage ranges."""
        test_cases = [
            {"general_pct": 25.0, "pa_pct": 30.0, "po_pct": 20.0},  # 0-30 range (CRITICAL)
            {"general_pct": 55.0, "pa_pct": 50.0, "po_pct": 60.0},  # 31-60 range (ALERTA)
            {"general_pct": 70.0, "pa_pct": 72.0, "po_pct": 68.0},  # 61-74 range (ALERTA)
            {"general_pct": 85.0, "pa_pct": 88.0, "po_pct": 82.0},  # 75-100 range (OPTIMO)
        ]

        for tc in test_cases:
            resultados = {
                "general": {"porcentaje": tc["general_pct"], "promedio": 4.0},
                "pa": {"porcentaje": tc["pa_pct"]},
                "po": {"porcentaje": tc["po_pct"]}
            }

            pdf_bytes = crear_pdf_auditoria(
                nombre_est="Test Establishment",
                fecha="2026-05-01",
                resultados=resultados,
                evals_pa={},
                evals_po={},
                matriz_pa={},
                matriz_po={}
            )

            assert pdf_bytes is not None
            assert len(pdf_bytes) > 500

    def test_pdf_with_special_characters_in_name(self):
        """Test PDF generation with special characters in establishment name."""
        resultados = {
            "general": {"porcentaje": 75.0, "promedio": 4.0},
            "pa": {"porcentaje": 78.0},
            "po": {"porcentaje": 72.0}
        }

        pdf_bytes = crear_pdf_auditoria(
            nombre_est="Restaurante El Niño & Cáfe",
            fecha="2026-05-01",
            resultados=resultados,
            evals_pa={},
            evals_po={},
            matriz_pa={},
            matriz_po={}
        )

        assert pdf_bytes is not None
        assert len(pdf_bytes) > 500