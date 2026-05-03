from fastapi import APIRouter, HTTPException
from supabase import create_client
from app.config import get_settings
from app.api.matrices import MATRIZ_PA, MATRIZ_PO
from typing import Optional, List, Dict, Any

router = APIRouter(prefix="/evaluations", tags=["evaluations"])


def get_supabase_client():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


def _build_questions_from_evals(
    evals_pa: Dict[str, Dict[str, int]],
    evals_po: Dict[str, Dict[str, int]]
) -> List[Dict[str, Any]]:
    """Build questions array from evaluation data, enriching with question text and context."""
    questions = []
    
    # Process PA evaluations
    for aspect, categories in MATRIZ_PA.items():
        if aspect not in evals_pa:
            continue
        aspect_evals = evals_pa[aspect]
        for category, questions_list in categories.items():
            for q in questions_list:
                qid = q["id"]
                if qid in aspect_evals:
                    rating = aspect_evals[qid]
                    questions.append({
                        "aspect": aspect,
                        "question": q["pregunta"],
                        "context": q.get("contexto", ""),
                        "rating": rating,
                        "percentage": (rating / 5) * 100
                    })
    
    # Process PO evaluations
    for aspect, categories in MATRIZ_PO.items():
        if aspect not in evals_po:
            continue
        aspect_evals = evals_po[aspect]
        for category, questions_list in categories.items():
            for q in questions_list:
                qid = q["id"]
                if qid in aspect_evals:
                    rating = aspect_evals[qid]
                    questions.append({
                        "aspect": aspect,
                        "question": q["pregunta"],
                        "context": q.get("contexto", ""),
                        "rating": rating,
                        "percentage": (rating / 5) * 100
                    })
    
    return questions


def _compute_breakdown(evals: Dict[str, Dict[str, int]], matriz: Dict) -> Dict[str, float]:
    """Compute aspect breakdown percentages from evaluation data."""
    breakdown = {}
    for aspect, categories in matriz.items():
        if aspect not in evals:
            breakdown[aspect] = 0.0
            continue
        aspect_evals = evals[aspect]
        ratings = []
        for category, questions_list in categories.items():
            for q in questions_list:
                qid = q["id"]
                if qid in aspect_evals:
                    ratings.append(aspect_evals[qid])
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            breakdown[aspect] = (avg_rating / 5) * 100
        else:
            breakdown[aspect] = 0.0
    return breakdown


def _compute_priority(pa_pct: float, po_pct: float) -> str:
    """Compute priority based on the difference between PA and PO percentages."""
    if pa_pct < po_pct - 5:
        return "PA"
    elif po_pct < pa_pct - 5:
        return "PO"
    else:
        return "BALANCED"


@router.get("")
async def list_evaluations():
    """List all evaluations (no auth required)"""
    supabase = get_supabase_client()
    response = supabase.table("evaluations").select("*").order("fecha", desc=True).execute()
    return response.data


@router.post("")
async def create_evaluation(data: dict):
    """Create a new evaluation"""
    supabase = get_supabase_client()
    evaluation_data = {
        "general_pct": data.get("general_pct", 0),
        "pa_pct": data.get("pa_pct", 0),
        "po_pct": data.get("po_pct", 0),
        "evaluaciones_pa": data.get("evaluaciones_pa", {}),
        "evaluaciones_po": data.get("evaluaciones_po", {})
    }
    response = supabase.table("evaluations").insert(evaluation_data).execute()
    return response.data[0] if response.data else None


@router.get("/{evaluation_id}")
async def get_evaluation(evaluation_id: str):
    """Get a specific evaluation with enriched breakdown data"""
    supabase = get_supabase_client()
    response = supabase.table("evaluations").select("*").eq("id", evaluation_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    evaluation = response.data[0]
    
    # Get evaluation data
    evals_pa = evaluation.get("evaluaciones_pa", {})
    evals_po = evaluation.get("evaluaciones_po", {})
    pa_pct = evaluation.get("pa_pct", 0)
    po_pct = evaluation.get("po_pct", 0)
    
    # Compute breakdowns
    pa_breakdown = _compute_breakdown(evals_pa, MATRIZ_PA)
    po_breakdown = _compute_breakdown(evals_po, MATRIZ_PO)
    
    # Build questions array
    questions = _build_questions_from_evals(evals_pa, evals_po)
    
    # Compute priority
    priority = _compute_priority(pa_pct, po_pct)
    
    # Enrich the evaluation response
    evaluation["pa_breakdown"] = pa_breakdown
    evaluation["po_breakdown"] = po_breakdown
    evaluation["questions"] = questions
    evaluation["priority"] = priority
    
    return evaluation


@router.put("/{evaluation_id}")
async def update_evaluation(evaluation_id: str, data: dict):
    """Update an evaluation"""
    supabase = get_supabase_client()
    response = supabase.table("evaluations").update(data).eq("id", evaluation_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return response.data[0]


@router.delete("/{evaluation_id}")
async def delete_evaluation(evaluation_id: str):
    """Delete an evaluation"""
    supabase = get_supabase_client()
    supabase.table("evaluations").delete().eq("id", evaluation_id).execute()
    return {"message": "Deleted successfully"}