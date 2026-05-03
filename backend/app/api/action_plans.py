from fastapi import APIRouter, HTTPException
from supabase import create_client
from app.config import get_settings
from typing import Optional

router = APIRouter(prefix="/action-plans", tags=["action-plans"])


def get_supabase_client():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


@router.get("")
async def list_action_plans(evaluation_id: Optional[str] = None):
    """List action plans, optionally filtered by evaluation"""
    supabase = get_supabase_client()

    query = supabase.table("action_plans").select("*")

    if evaluation_id:
        query = query.eq("evaluation_id", evaluation_id)

    response = query.execute()
    return response.data


@router.post("")
async def create_action_plan(data: dict):
    """Create a new action plan"""
    supabase = get_supabase_client()
    response = supabase.table("action_plans").insert(data).execute()
    return response.data[0] if response.data else None


@router.put("/{action_plan_id}")
async def update_action_plan(action_plan_id: str, data: dict):
    """Update an action plan"""
    supabase = get_supabase_client()

    # Check action plan exists
    response = supabase.table("action_plans").select("*").eq("id", action_plan_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Action plan not found")

    updated = supabase.table("action_plans").update(data).eq("id", action_plan_id).execute()
    return updated.data[0] if updated.data else None


@router.delete("/{action_plan_id}")
async def delete_action_plan(action_plan_id: str):
    """Delete an action plan"""
    supabase = get_supabase_client()

    response = supabase.table("action_plans").select("id").eq("id", action_plan_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Action plan not found")

    supabase.table("action_plans").delete().eq("id", action_plan_id).execute()
    return {"message": "Deleted successfully"}