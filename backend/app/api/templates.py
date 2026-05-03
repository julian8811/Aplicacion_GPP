from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from supabase import create_client
from app.config import get_settings
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/templates", tags=["templates"])


def get_supabase_client():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


class TemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    pa_config: Optional[Dict[str, Any]] = None
    po_config: Optional[Dict[str, Any]] = None
    is_public: bool = False


class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    pa_config: Optional[Dict[str, Any]] = None
    po_config: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None


@router.get("")
async def list_templates(user: dict = Depends(get_current_user)):
    """List user's templates + public templates"""
    supabase = get_supabase_client()
    
    response = supabase.table("evaluation_templates").select("*").or_(
        f"created_by.eq.{user['id']},is_public.eq.true"
    ).order("created_at", desc=True).execute()
    
    return response.data


@router.post("")
async def create_template(data: TemplateCreate, user: dict = Depends(get_current_user)):
    """Create a new template"""
    supabase = get_supabase_client()
    
    template_data = {
        "name": data.name,
        "description": data.description,
        "pa_config": data.pa_config or {"selected_aspects": [], "questions": []},
        "po_config": data.po_config or {"selected_aspects": [], "questions": []},
        "is_public": data.is_public,
        "created_by": user["id"]
    }
    
    response = supabase.table("evaluation_templates").insert(template_data).execute()
    return response.data[0] if response.data else None


@router.get("/{template_id}")
async def get_template(template_id: str, user: dict = Depends(get_current_user)):
    """Get a single template by ID"""
    supabase = get_supabase_client()
    
    response = supabase.table("evaluation_templates").select("*").eq("id", template_id).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Template not found")
    
    template = response.data[0]
    
    # Check access: own template or public
    if template["created_by"] != user["id"] and not template.get("is_public"):
        raise HTTPException(status_code=403, detail="Access denied")
    
    return template


@router.put("/{template_id}")
async def update_template(template_id: str, data: TemplateUpdate, user: dict = Depends(get_current_user)):
    """Update a template (only owner)"""
    supabase = get_supabase_client()
    
    # Check ownership
    response = supabase.table("evaluation_templates").select("*").eq("id", template_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if response.data[0]["created_by"] != user["id"]:
        raise HTTPException(status_code=403, detail="Only owner can update template")
    
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    
    response = supabase.table("evaluation_templates").update(update_data).eq("id", template_id).execute()
    return response.data[0] if response.data else None


@router.delete("/{template_id}")
async def delete_template(template_id: str, user: dict = Depends(get_current_user)):
    """Delete a template (only owner)"""
    supabase = get_supabase_client()
    
    # Check ownership
    response = supabase.table("evaluation_templates").select("*").eq("id", template_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if response.data[0]["created_by"] != user["id"]:
        raise HTTPException(status_code=403, detail="Only owner can delete template")
    
    supabase.table("evaluation_templates").delete().eq("id", template_id).execute()
    return {"message": "Template deleted successfully"}


class TemplateFromEvaluation(BaseModel):
    name: str
    description: Optional[str] = None


@router.post("/from-evaluation/{evaluation_id}")
async def create_template_from_evaluation(
    evaluation_id: str,
    data: TemplateFromEvaluation,
    user: dict = Depends(get_current_user)
):
    """Create a template from an existing evaluation"""
    supabase = get_supabase_client()
    
    # Fetch evaluation
    response = supabase.table("evaluations").select("evaluaciones_pa", "evaluaciones_po").eq("id", evaluation_id).eq("owner_id", user["id"]).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    evaluation = response.data[0]
    
    # Extract selected aspects from the evaluation data
    pa_config = {
        "selected_aspects": list(evaluation.get("evaluaciones_pa", {}).keys()),
        "questions": evaluation.get("evaluaciones_pa", {})
    }
    
    po_config = {
        "selected_aspects": list(evaluation.get("evaluaciones_po", {}).keys()),
        "questions": evaluation.get("evaluaciones_po", {})
    }
    
    # Create template
    template_data = {
        "name": data.name,
        "description": data.description or f"Template created from evaluation {evaluation_id[:8]}...",
        "pa_config": pa_config,
        "po_config": po_config,
        "is_public": False,
        "created_by": user["id"]
    }
    
    response = supabase.table("evaluation_templates").insert(template_data).execute()
    return response.data[0] if response.data else None