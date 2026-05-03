from fpdf import FPDF
from datetime import datetime
import urllib.request
import io


def crear_pdf_auditoria(nombre_est, fecha, resultados, evals_pa, evals_po,
                        matriz_pa=None, matriz_po=None, recommendations=None, action_plans=None,
                        logo_url=None, primary_color=None, footer_text=None):
    """
    Generate professional PDF audit report for GPP evaluation.

    Args:
        nombre_est: Establishment name
        fecha: Date of report
        resultados: Dict with general_pct, pa_pct, po_pct
        evals_pa: PA evaluation data {aspect: {question_id: rating}}
        evals_po: PO evaluation data {aspect: {question_id: rating}}
        matriz_pa: PA matrix data (optional)
        matriz_po: PO matrix data (optional)
        recommendations: List of {aspect, element, recommendation, priority}
        action_plans: List of action plans
        logo_url: URL to logo image for PDF header (optional)
        primary_color: Hex color for header and accents (optional, default blue)
        footer_text: Custom text for footer (optional)
    """
    # Default primary color to blue if not provided
    if not primary_color:
        primary_color = "#2563eb"

    # Parse hex color to RGB
    header_rgb = _hex_to_rgb(primary_color)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # === PAGE 1: Header and Summary ===
    pdf.add_page()

    # Header with optional logo and branding
    if logo_url:
        try:
            # Try to fetch and embed logo
            logo_data = _fetch_image_data(logo_url)
            if logo_data:
                # Add logo on the right side
                pdf.image(logo_data, x=150, y=8, w=40)
        except Exception:
            # If logo fails, just use text header
            pass

    # Colored header bar
    pdf.set_fill_color(*header_rgb)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(10)
    pdf.cell(0, 15, "AUDITORIA GPP", ln=True, align="C")
    pdf.set_font("Helvetica", "", 14)
    pdf.cell(0, 10, f"Establecimiento: {nombre_est}", ln=True, align="C")
    pdf.ln(25)

    # Reset text color
    pdf.set_text_color(0, 0, 0)

    # Date
    pdf.set_font("Helvetica", "", 11)
    fecha_formateada = fecha.strftime("%d/%m/%Y") if isinstance(fecha, (datetime, str)) and not isinstance(fecha, str) else str(fecha)
    if isinstance(fecha, str):
        try:
            fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
            fecha_formateada = fecha_dt.strftime("%d/%m/%Y")
        except:
            fecha_formateada = fecha
    pdf.cell(0, 8, f"Fecha del Informe: {fecha_formateada}", ln=True)
    pdf.ln(10)

    # Summary Section Title
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_fill_color(236, 240, 241)
    pdf.cell(0, 10, "RESUMEN DE RESULTADOS", ln=True, fill=True)
    pdf.ln(5)

    # Main percentages with visual indicators
    general_pct = resultados.get("general", {}).get("porcentaje", resultados.get("general_pct", 0))
    pa_pct = resultados.get("pa", {}).get("porcentaje", resultados.get("pa_pct", 0))
    po_pct = resultados.get("po", {}).get("porcentaje", resultados.get("po_pct", 0))

    # General percentage gauge
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Indice de Cumplimiento General", ln=True)
    _draw_gauge(pdf, general_pct)
    pdf.ln(5)

    # PA and PO percentages
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(90, 8, f"Proceso Administrativo (PA): {pa_pct:.1f}%", ln=True)
    pdf.cell(90, 8, f"Proceso Operativo (PO): {po_pct:.1f}%", ln=True)
    pdf.ln(10)

    # Determine priority
    priority = "BALANCED"
    if pa_pct < po_pct:
        priority = "PA"
    elif po_pct < pa_pct:
        priority = "PO"

    pdf.set_font("Helvetica", "B", 11)
    priority_colors = {"PA": (231, 76, 60), "PO": (230, 126, 34), "BALANCED": (46, 204, 113)}
    r, g, b = priority_colors.get(priority, (0, 0, 0))
    pdf.set_text_color(r, g, b)
    priority_labels = {"PA": "Prioridad en Proceso Administrativo", "PO": "Prioridad en Proceso Operativo", "BALANCED": "Procesos Equilibrados"}
    pdf.cell(0, 8, priority_labels.get(priority, ""), ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)

    # === PA Breakdown Section ===
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_fill_color(236, 240, 241)
    pdf.cell(0, 10, "DETALLE PROCESO ADMINISTRATIVO (PA)", ln=True, fill=True)
    pdf.ln(3)

    pa_breakdown = _compute_pa_breakdown(evals_pa)
    _draw_breakdown_table(pdf, pa_breakdown, is_pa=True)
    pdf.ln(5)

    # === PO Breakdown Section ===
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "DETALLE PROCESO OPERATIVO (PO)", ln=True, fill=True)
    pdf.ln(3)

    po_breakdown = _compute_po_breakdown(evals_po)
    _draw_breakdown_table(pdf, po_breakdown, is_pa=False)

    # === PAGE 2: Recommendations ===
    if recommendations:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_fill_color(142, 68, 173)  # Purple
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, "RECOMENDACIONES", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)

        # Group by priority
        alta_recs = [r for r in recommendations if r.get("priority") == "ALTA"]
        media_recs = [r for r in recommendations if r.get("priority") == "MEDIA"]

        if alta_recs:
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(231, 76, 60)
            pdf.cell(0, 8, "Prioridad ALTA", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Helvetica", "", 10)
            for rec in alta_recs:
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(0, 6, f"{rec.get('aspect', '')} - {rec.get('element', '')}", ln=True)
                pdf.set_font("Helvetica", "", 9)
                pdf.multi_cell(0, 5, rec.get("recommendation", ""))
                pdf.ln(2)
            pdf.ln(5)

        if media_recs:
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(230, 126, 34)
            pdf.cell(0, 8, "Prioridad MEDIA", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Helvetica", "", 10)
            for rec in media_recs:
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(0, 6, f"{rec.get('aspect', '')} - {rec.get('element', '')}", ln=True)
                pdf.set_font("Helvetica", "", 9)
                pdf.multi_cell(0, 5, rec.get("recommendation", ""))
                pdf.ln(2)

    # === PAGE 3: Action Plans ===
    if action_plans:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_fill_color(39, 174, 96)  # Green
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, "PLANES DE ACCION", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)

        for i, plan in enumerate(action_plans, 1):
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 7, f"Plan #{i}", ln=True)
            pdf.set_font("Helvetica", "", 10)

            if isinstance(plan, dict):
                title = plan.get("title", plan.get("titulo", ""))
                description = plan.get("description", plan.get("descripcion", ""))
                responsible = plan.get("responsible", plan.get("responsable", ""))
                deadline = plan.get("deadline", plan.get("fecha_limite", ""))

                if title:
                    pdf.set_font("Helvetica", "B", 10)
                    pdf.cell(0, 6, f"Titulo: {title}", ln=True)
                if description:
                    pdf.set_font("Helvetica", "", 9)
                    pdf.multi_cell(0, 5, f"Descripcion: {description}")
                if responsible:
                    pdf.cell(0, 5, f"Responsable: {responsible}", ln=True)
                if deadline:
                    pdf.cell(0, 5, f"Fecha Limite: {deadline}", ln=True)
            else:
                pdf.multi_cell(0, 5, str(plan))

            pdf.ln(5)

    # Footer on all pages
    pdf.set_y(-20)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(127, 127, 127)
    if footer_text:
        pdf.cell(0, 10, footer_text, ln=True, align="C")
    pdf.cell(0, 10, f"GPP Auditoria - {nombre_est} - Generado {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")

    return bytes(pdf.output())


def _draw_gauge(pdf, percentage):
    """Draw a simple text-based gauge representation"""
    pdf.set_font("Helvetica", "", 10)
    filled = int(percentage / 5)  # Each block = 5%
    empty = 20 - filled

    bar = "[" + "=" * filled + " " * empty + "]"
    pdf.cell(0, 6, bar, ln=True)
    pdf.cell(0, 6, f"  {percentage:.1f}%", ln=True)


def _draw_breakdown_table(pdf, breakdown, is_pa=True):
    """Draw a breakdown table for PA or PO aspects"""
    if not breakdown:
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, "No hay datos disponibles", ln=True)
        return

    # Table header
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(189, 195, 199)
    pdf.cell(80, 7, "Aspecto", 1, 0, "C", True)
    pdf.cell(40, 7, "Porcentaje", 1, 0, "C", True)
    pdf.cell(70, 7, "Estado", 1, 1, "C", True)

    # Table rows
    pdf.set_font("Helvetica", "", 10)
    for aspect, pct in breakdown.items():
        pdf.cell(80, 7, aspect, 1, 0, "L")
        pdf.cell(40, 7, f"{pct:.1f}%", 1, 0, "C")

        # Status with color
        if pct >= 75:
            status = "Cumple"
            pdf.set_text_color(46, 204, 113)
        elif pct >= 60:
            status = "Cumple Parcial"
            pdf.set_text_color(230, 126, 34)
        else:
            status = "No Cumple"
            pdf.set_text_color(231, 76, 60)

        pdf.cell(70, 7, status, 1, 1, "C")
        pdf.set_text_color(0, 0, 0)


def _compute_pa_breakdown(evals_pa):
    """Compute PA breakdown percentages from evaluation data"""
    # Aspect weights for PA
    pesos_pa = {
        "PLANEACION": {"Analisis del contexto": 53.75, "Existencia de un plan estrategico": 46.25},
        "ORGANIZACION": {"Existencia de una estructura organizativa": 11.25, "Departamentalizacion": 35.0, "Procesos documentados": 33.75, "Ciclo PHVA": 20.0},
        "DIRECCION": {"Liderazgo organizacional": 35.0, "Canales de comunicacion efectivos": 30.0, "Cultura organizacional": 35.0},
        "CONTROL": {"Sistemas de control": 45.0, "Auditorias internas": 25.0, "Acciones correctivas y preventivas": 30.0}
    }

    # Aspect order for display
    aspect_order = ["PLANEACION", "ORGANIZACION", "DIRECCION", "CONTROL"]
    aspect_display = {"PLANEACION": "Planificacion", "ORGANIZACION": "Organizacion", "DIRECCION": "Direccion", "CONTROL": "Control"}

    breakdown = {}
    for aspect in aspect_order:
        aspect_key = aspect
        aspect_questions = evals_pa.get(aspect_key, evals_pa.get(aspect, {}))

        if not aspect_questions:
            breakdown[aspect_display.get(aspect, aspect)] = 0
            continue

        # Calculate weighted average for this aspect
        weights = pesos_pa.get(aspect, {})
        total_weight = 0
        weighted_sum = 0

        for q_id, rating in aspect_questions.items():
            # Find element name from question ID
            element = _element_from_question_id(q_id, aspect)
            weight = weights.get(element, 1)  # Default weight if not found
            total_weight += weight
            weighted_sum += rating * weight

        if total_weight > 0:
            avg_rating = weighted_sum / total_weight
            pct = (avg_rating / 5) * 100
        else:
            pct = 0

        breakdown[aspect_display.get(aspect, aspect)] = pct

    return breakdown


def _compute_po_breakdown(evals_po):
    """Compute PO breakdown percentages from evaluation data"""
    pesos_po = {
        "LOGISTICA DE COMPRAS": {"Logistica de entrada": 60.0, "Gestion de inventarios": 40.0},
        "GESTION DE PRODUCCION": {"Equipos": 15.0, "Infraestructura": 15.0, "Distribucion de los procesos (flujo)": 10.0, "Planeacion de la produccion": 25.0, "Materia prima": 15.0, "Control de la produccion": 20.0},
        "LOGISTICA EXTERNA": {"Distribucion": 100.0}
    }

    aspect_order = ["LOGISTICA DE COMPRAS", "GESTION DE PRODUCCION", "LOGISTICA EXTERNA"]
    aspect_display = {"LOGISTICA DE COMPRAS": "Logistica de Compras", "GESTION DE PRODUCCION": "Gestion de Produccion", "LOGISTICA EXTERNA": "Logistica Externa"}

    breakdown = {}
    for aspect in aspect_order:
        aspect_questions = evals_po.get(aspect, evals_po.get(aspect.upper(), {}))

        if not aspect_questions:
            breakdown[aspect_display.get(aspect, aspect)] = 0
            continue

        weights = pesos_po.get(aspect, {})
        total_weight = 0
        weighted_sum = 0

        for q_id, rating in aspect_questions.items():
            element = _element_from_question_id(q_id, aspect)
            weight = weights.get(element, 1)
            total_weight += weight
            weighted_sum += rating * weight

        if total_weight > 0:
            avg_rating = weighted_sum / total_weight
            pct = (avg_rating / 5) * 100
        else:
            pct = 0

        breakdown[aspect_display.get(aspect, aspect)] = pct

    return breakdown


def _element_from_question_id(q_id, aspect):
    """Extract element name from question ID"""
    # Question IDs look like: PA_PLANEACION_01 or PO_LOGISTICA_02
    # Element is extracted from the middle part or derived from the aspect
    if isinstance(q_id, str):
        parts = q_id.split("_")
        if len(parts) >= 3:
            # Last part is the question number, middle is the category
            return parts[1] if len(parts) == 3 else "_".join(parts[1:-1])

    # Fallback: map aspect to element based on standard names
    element_mapping = {
        "PLANEACION": "Planeacion",
        "ORGANIZACION": "Organizacion",
        "DIRECCION": "Direccion",
        "CONTROL": "Control",
        "LOGISTICA DE COMPRAS": "Logistica de Compras",
        "GESTION DE PRODUCCION": "Gestion de Produccion",
        "LOGISTICA EXTERNA": "Logistica Externa"
    }
    return element_mapping.get(aspect, aspect)


def _hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color string to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def _fetch_image_data(url: str) -> bytes:
    """Fetch image data from URL and return as bytes"""
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return io.BytesIO(response.read())
    except Exception:
        return None