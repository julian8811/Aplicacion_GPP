from fastapi import APIRouter, HTTPException, Depends
from supabase import create_client
from app.config import get_settings
from app.core.dependencies import get_current_user
from typing import Dict, Any

router = APIRouter(prefix="/comparison", tags=["comparison"])


def get_supabase_client():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


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


@router.get("/{eval_a_id}/{eval_b_id}")
async def compare_evaluations(eval_a_id: str, eval_b_id: str, user: dict = Depends(get_current_user)):
    """Compare two evaluations side by side with delta calculations"""
    supabase = get_supabase_client()
    
    # Fetch both evaluations (must belong to user)
    response_a = supabase.table("evaluations").select("*").eq("id", eval_a_id).eq("owner_id", user["id"]).execute()
    response_b = supabase.table("evaluations").select("*").eq("id", eval_b_id).eq("owner_id", user["id"]).execute()
    
    if not response_a.data:
        raise HTTPException(status_code=404, detail="Evaluation A not found")
    if not response_b.data:
        raise HTTPException(status_code=404, detail="Evaluation B not found")
    
    eval_a = response_a.data[0]
    eval_b = response_b.data[0]
    
    # Import matrices
    from app.api.matrices import MATRIZ_PA, MATRIZ_PO
    
    # Compute breakdowns for both
    evals_pa_a = eval_a.get("evaluaciones_pa", {})
    evals_po_a = eval_a.get("evaluaciones_po", {})
    evals_pa_b = eval_b.get("evaluaciones_pa", {})
    evals_po_b = eval_b.get("evaluaciones_po", {})
    
    pa_breakdown_a = _compute_breakdown(evals_pa_a, MATRIZ_PA)
    po_breakdown_a = _compute_breakdown(evals_po_a, MATRIZ_PO)
    pa_breakdown_b = _compute_breakdown(evals_pa_b, MATRIZ_PA)
    po_breakdown_b = _compute_breakdown(evals_po_b, MATRIZ_PO)
    
    # Build comparison data for PA aspects
    pa_comparison = []
    for aspect in MATRIZ_PA.keys():
        val_a = pa_breakdown_a.get(aspect, 0)
        val_b = pa_breakdown_b.get(aspect, 0)
        delta = val_b - val_a
        delta_pct = (delta / val_a * 100) if val_a > 0 else 0
        
        pa_comparison.append({
            "aspect": aspect,
            "eval_a_value": round(val_a, 1),
            "eval_b_value": round(val_b, 1),
            "delta": round(delta, 1),
            "delta_pct": round(delta_pct, 1)
        })
    
    # Build comparison data for PO aspects
    po_comparison = []
    for aspect in MATRIZ_PO.keys():
        val_a = po_breakdown_a.get(aspect, 0)
        val_b = po_breakdown_b.get(aspect, 0)
        delta = val_b - val_a
        delta_pct = (delta / val_a * 100) if val_a > 0 else 0
        
        po_comparison.append({
            "aspect": aspect,
            "eval_a_value": round(val_a, 1),
            "eval_b_value": round(val_b, 1),
            "delta": round(delta, 1),
            "delta_pct": round(delta_pct, 1)
        })
    
    # Overall comparison
    pa_pct_a = eval_a.get("pa_pct", 0)
    pa_pct_b = eval_b.get("pa_pct", 0)
    po_pct_a = eval_a.get("po_pct", 0)
    po_pct_b = eval_b.get("po_pct", 0)
    general_pct_a = eval_a.get("general_pct", 0)
    general_pct_b = eval_b.get("general_pct", 0)
    
    overall = {
        "eval_a": {
            "id": eval_a["id"],
            "fecha": eval_a.get("fecha"),
            "general_pct": round(general_pct_a, 1),
            "pa_pct": round(pa_pct_a, 1),
            "po_pct": round(po_pct_a, 1)
        },
        "eval_b": {
            "id": eval_b["id"],
            "fecha": eval_b.get("fecha"),
            "general_pct": round(general_pct_b, 1),
            "pa_pct": round(pa_pct_b, 1),
            "po_pct": round(po_pct_b, 1)
        },
        "delta": {
            "general_pct": round(general_pct_b - general_pct_a, 1),
            "pa_pct": round(pa_pct_b - pa_pct_a, 1),
            "po_pct": round(po_pct_b - po_pct_a, 1)
        }
    }
    
    return {
        "evaluation_a": eval_a,
        "evaluation_b": eval_b,
        "pa_comparison": pa_comparison,
        "po_comparison": po_comparison,
        "overall": overall
    }