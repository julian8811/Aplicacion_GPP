from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from supabase import create_client
from app.config import get_settings
from app.pdf_generator import crear_pdf_auditoria

router = APIRouter(prefix="/pdf", tags=["pdf"])


def get_supabase_client():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


@router.get("/{evaluation_id}")
async def get_pdf(evaluation_id: str):
    """Generate and download PDF for an evaluation"""
    supabase = get_supabase_client()

    # Get evaluation
    response = supabase.table("evaluations").select("*").eq("id", evaluation_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    evaluation = response.data[0]

    # Get establishment name from config
    settings = get_settings()
    establishment_name = getattr(settings, 'establishment_name', 'Establecimiento GPP')

    # Build results dict
    resultados = {
        "general": {"porcentaje": evaluation.get("general_pct", 0)},
        "pa": {"porcentaje": evaluation.get("pa_pct", 0)},
        "po": {"porcentaje": evaluation.get("po_pct", 0)}
    }

    # Compute recommendations directly from evaluation data (mirrors recommendations.py logic)
    evals_pa = evaluation.get("evaluaciones_pa", {})
    evals_po = evaluation.get("evaluaciones_po", {})
    recommendations = _compute_recommendations(evals_pa, evals_po)

    # Fetch action plans for this evaluation
    action_plans = []
    try:
        ap_response = supabase.table("action_plans").select("*").eq("evaluation_id", evaluation_id).execute()
        if ap_response.data:
            action_plans = ap_response.data
    except Exception:
        pass

    # Parse date from evaluation
    fecha = evaluation.get("fecha", "")
    if isinstance(fecha, str) and "T" in fecha:
        fecha = fecha.split("T")[0]

    # Generate PDF
    try:
        pdf_bytes = crear_pdf_auditoria(
            nombre_est=establishment_name,
            fecha=fecha,
            resultados=resultados,
            evals_pa=evals_pa,
            evals_po=evals_po,
            matriz_pa={},
            matriz_po={},
            recommendations=recommendations,
            action_plans=action_plans if action_plans else None
        )

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=auditoria_{evaluation_id}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


def _compute_recommendations(evals_pa, evals_po):
    """Compute recommendations based on low-scored aspects in evaluation"""
    # Element to aspect mapping (same as recommendations.py)
    element_to_aspect = {
        "Análisis del contexto": "PLANEACIÓN",
        "Existencia de un plan estratégico": "PLANEACIÓN",
        "Existencia de una estructura organizativa": "ORGANIZACIÓN",
        "Departamentalización": "ORGANIZACIÓN",
        "Procesos documentados": "ORGANIZACIÓN",
        "Ciclo PHVA": "ORGANIZACIÓN",
        "Liderazgo organizacional": "DIRECCIÓN",
        "Canales de comunicación efectivos": "DIRECCIÓN",
        "Cultura organizacional": "DIRECCIÓN",
        "Sistemas de control": "CONTROL",
        "Auditorías internas": "CONTROL",
        "Acciones correctivas y preventivas": "CONTROL",
        "Logística de entrada": "LOGÍSTICA DE COMPRAS",
        "Gestión de inventarios": "LOGÍSTICA DE COMPRAS",
        "Equipos": "GESTIÓN DE PRODUCCIÓN",
        "Infraestructura": "GESTIÓN DE PRODUCCIÓN",
        "Distribución de los procesos (flujo)": "GESTIÓN DE PRODUCCIÓN",
        "Planeación de la producción": "GESTIÓN DE PRODUCCIÓN",
        "Materia prima": "GESTIÓN DE PRODUCCIÓN",
        "Control de la producción": "GESTIÓN DE PRODUCCIÓN",
        "Distribución": "LOGÍSTICA EXTERNA"
    }

    # Recommendations matrix
    matriz_recomendaciones = {
        "PLANEACIÓN": {
            "Análisis del contexto": "Implementar un análisis PESTEL y DOFA formal cada 6 meses involucrando a los líderes de área.",
            "Existencia de un plan estratégico": "Definir objetivos SMART y socializar la visión empresarial mediante talleres de alineación cultural."
        },
        "ORGANIZACIÓN": {
            "Existencia de una estructura organizativa": "Actualizar el organigrama y definir claramente las líneas de reporte para evitar duplicidad de mando.",
            "Departamentalización": "Agrupar actividades por procesos lógicos y asignar dueños de proceso con autoridad de decisión.",
            "Procesos documentados": "Iniciar la estandarización de procesos críticos (compras, producción) mediante flujogramas y perfiles de cargo.",
            "Ciclo PHVA": "Establecer reuniones de mejora continua para analizar desviaciones y ajustar planes operativos."
        },
        "DIRECCIÓN": {
            "Liderazgo organizacional": "Desarrollar un programa de capacitación en liderazgo situacional para supervisores y jefes de cocina.",
            "Canales de comunicación efectivos": "Implementar un tablero de gestión visual (Obeya) y herramientas digitales de comunicación interna.",
            "Cultura organizacional": "Crear un programa de incentivos no monetarios y reforzar el sentido de pertenencia con actividades de Team Building."
        },
        "CONTROL": {
            "Sistemas de control": "Implementar un Cuadro de Mando Integral (Balanced Scorecard) con indicadores financieros y operativos.",
            "Auditorías internas": "Programar auditorías cruzadas entre departamentos para asegurar la objetividad en las revisiones.",
            "Acciones correctivas y preventivas": "Documentar cada falla mediante el método de los 5 Porqués para eliminar la causa raíz."
        },
        "LOGÍSTICA DE COMPRAS": {
            "Logística de entrada": "Homologar proveedores y establecer acuerdos de nivel de servicio (SLA) para insumos críticos.",
            "Gestión de inventarios": "Implementar un software de gestión de inventarios con alertas de stock mínimo y control PEPS riguroso."
        },
        "GESTIÓN DE PRODUCCIÓN": {
            "Equipos": "Establecer un plan de mantenimiento preventivo anual y renovar equipos con baja eficiencia energética.",
            "Infraestructura": "Rediseñar el flujo de la cocina bajo el principio de 'Marcha Adelante' para evitar contaminaciones cruzadas.",
            "Distribución de los procesos (flujo)": "Señalizar áreas de trabajo y optimizar el layout para reducir tiempos de desplazamiento del personal.",
            "Planeación de la producción": "Implementar fichas técnicas estandarizadas con costeo real para cada plato del menú.",
            "Materia prima": "Fortalecer la inspección de recibo de mercancía con termómetros y listas de chequeo de calidad.",
            "Control de la producción": "Digitalizar el registro de tiempos y temperaturas durante el servicio para asegurar inocuidad."
        },
        "LOGÍSTICA EXTERNA": {
            "Distribución": "Implementar encuestas de satisfacción digitales (NPS) y protocolos de recuperación de servicios fallidos."
        }
    }

    # Find low-scoring aspects (rating <= 2)
    low_scoring_aspects = set()
    for aspect, questions in evals_pa.items():
        for q_id, rating in questions.items():
            if rating <= 2:
                low_scoring_aspects.add(aspect)
                break

    for aspect, questions in evals_po.items():
        for q_id, rating in questions.items():
            if rating <= 2:
                low_scoring_aspects.add(aspect)
                break

    # Build recommendations with priority
    recommendations = []
    for aspect, elements in matriz_recomendaciones.items():
        for element, recommendation_text in elements.items():
            if aspect in low_scoring_aspects:
                priority = "ALTA"
            else:
                priority = "MEDIA"

            recommendations.append({
                "aspect": aspect,
                "element": element,
                "recommendation": recommendation_text,
                "priority": priority
            })

    return recommendations