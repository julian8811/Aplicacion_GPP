from fastapi import APIRouter, HTTPException
from supabase import create_client
from app.config import get_settings
from app.recomendaciones import MATRIZ_RECOMENDACIONES

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def get_supabase_client():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


@router.get("")
async def get_recommendations(evaluation_id: str = None):
    """Get recommendations based on evaluation results.
    
    If evaluation_id is provided, filters recommendations based on which
    aspects scored low (no-cumple or cumple-parcial answers).
    """
    if not evaluation_id:
        # Return all recommendations without filtering
        recommendations = []
        for aspect, elements in MATRIZ_RECOMENDACIONES.items():
            for element, recommendation in elements.items():
                recommendations.append({
                    "aspect": aspect,
                    "element": element,
                    "recommendation": recommendation,
                    "priority": "MEDIA"
                })
        return recommendations
    
    # Fetch evaluation to determine which aspects scored low
    supabase = get_supabase_client()
    response = supabase.table("evaluations").select("*").eq("id", evaluation_id).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    evaluation = response.data[0]
    evals_pa = evaluation.get("evaluaciones_pa", {})
    evals_po = evaluation.get("evaluaciones_po", {})
    
    # Question ID pattern: PA_CATEGORY_Aspect_SubIndex or PO_CATEGORY_Aspect_SubIndex
    # Example: "PA_PLANEACIÓN_Análisis del contexto_0"
    def extract_aspect_from_qid(qid: str):
        """Extract aspect name from question ID like PA_PLANEACIÓN_Análisis del contexto_0"""
        parts = qid.split("_", 2)
        if len(parts) >= 3:
            # parts: [PA, CATEGORY, Aspect_SubIndex]
            # category is second part, aspect is third part before the _N suffix
            category = parts[1]
            aspect_with_index = parts[2]
            # Remove trailing _N index from aspect name
            aspect = "_".join(aspect_with_index.rsplit("_", 1)[:-1])
            return (category, aspect)
        return (None, None)
    
    def get_priority(rating: int) -> str:
        """Determine priority based on rating value"""
        if rating <= 2:
            return "ALTA"
        elif rating == 3:
            return "MEDIA"
        else:  # rating >= 4
            return "BAJA"
    
    # Map aspect names from evaluation data to categories in MATRIZ_RECOMENDACIONES
    # Keys are aspect names (from MATRIZ_RECOMENDACIONES), values are categories
    aspect_to_category = {
        # PLANEACIÓN aspects
        "Análisis del contexto": "PLANEACIÓN",
        "Existencia de un plan estratégico": "PLANEACIÓN",
        "Estructura organizativa": "PLANEACIÓN",
        "Departamentalización": "PLANEACIÓN",
        "Procesos documentados": "PLANEACIÓN",
        "Ciclo PHVA": "PLANEACIÓN",
        # ORGANIZACIÓN aspects
        "Existencia de una estructura organizativa": "ORGANIZACIÓN",
        "Departamentalización": "ORGANIZACIÓN",
        "Procesos documentados": "ORGANIZACIÓN",
        # DIRECCIÓN aspects
        "Liderazgo organizacional": "DIRECCIÓN",
        "Canales de comunicación efectivos": "DIRECCIÓN",
        "Cultura organizacional": "DIRECCIÓN",
        # CONTROL aspects
        "Sistemas de control": "CONTROL",
        "Auditorías internas": "CONTROL",
        "Acciones correctivas y preventivas": "CONTROL",
        # LOGÍSTICA DE COMPRAS aspects
        "Logística de entrada": "LOGÍSTICA DE COMPRAS",
        "Gestión de inventarios": "LOGÍSTICA DE COMPRAS",
        # GESTIÓN DE PRODUCCIÓN aspects
        "Equipos": "GESTIÓN DE PRODUCCIÓN",
        "Infraestructura": "GESTIÓN DE PRODUCCIÓN",
        "Distribución de los procesos (flujo)": "GESTIÓN DE PRODUCCIÓN",
        "Planeación de la producción": "GESTIÓN DE PRODUCCIÓN",
        "Materia prima": "GESTIÓN DE PRODUCCIÓN",
        "Control de la producción": "GESTIÓN DE PRODUCCIÓN",
        # LOGÍSTICA EXTERNA aspects
        "Distribución": "LOGÍSTICA EXTERNA"
    }
    
    # Collect aspect ratings from evaluations
    aspect_ratings = {}  # {aspect_name: [ratings]}
    
    # Process both PA and PO evaluations
    all_evals = list(evals_pa.items()) + list(evals_po.items())
    for category, questions in all_evals:
        for qid, rating in questions.items():
            _, aspect = extract_aspect_from_qid(qid)
            if aspect and aspect in aspect_to_category:
                if aspect not in aspect_ratings:
                    aspect_ratings[aspect] = []
                aspect_ratings[aspect].append(rating)
    
    # Build recommendations with priority based on average rating for each aspect
    recommendations = []
    for category, elements in MATRIZ_RECOMENDACIONES.items():
        for element, recommendation_text in elements.items():
            # Get ratings for this element's aspect
            ratings = aspect_ratings.get(element, [])
            if ratings:
                avg_rating = sum(ratings) / len(ratings)
                priority = get_priority(int(avg_rating))
            else:
                # No evaluation data for this aspect, use default
                priority = "MEDIA"
            
            recommendations.append({
                "aspect": category,
                "element": element,
                "recommendation": recommendation_text,
                "priority": priority
            })
    
    return recommendations
