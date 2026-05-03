from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter(prefix="/results", tags=["results"])


class ResultsRequest(BaseModel):
    evals_pa: Dict[str, Dict[str, int]]
    evals_po: Dict[str, Dict[str, int]]


@router.post("/calculate")
async def calculate_results(data: ResultsRequest):
    """
    Calculate results from evaluation ratings.
    Ratings are 0-5, converted to percentage (rating/5 * 100)
    """
    # Calculate PA percentage
    all_pa_ratings = []
    for aspect, questions in data.evals_pa.items():
        for q_id, rating in questions.items():
            all_pa_ratings.append(rating)

    pa_pct = (sum(all_pa_ratings) / len(all_pa_ratings) / 5 * 100) if all_pa_ratings else 0

    # Calculate PO percentage
    all_po_ratings = []
    for aspect, questions in data.evals_po.items():
        for q_id, rating in questions.items():
            all_po_ratings.append(rating)

    po_pct = (sum(all_po_ratings) / len(all_po_ratings) / 5 * 100) if all_po_ratings else 0

    # Calculate general percentage
    all_ratings = all_pa_ratings + all_po_ratings
    general_pct = (sum(all_ratings) / len(all_ratings) / 5 * 100) if all_ratings else 0

    # Determine priority
    if pa_pct < po_pct - 5:
        priority = "PA"
    elif po_pct < pa_pct - 5:
        priority = "PO"
    else:
        priority = "BALANCED"

    return {
        "general_pct": round(general_pct, 1),
        "pa_pct": round(pa_pct, 1),
        "po_pct": round(po_pct, 1),
        "priority": priority,
        "total_questions_pa": len(all_pa_ratings),
        "total_questions_po": len(all_po_ratings)
    }