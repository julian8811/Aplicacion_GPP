from fastapi import APIRouter, HTTPException, Depends, Query
from supabase import create_client
from app.config import get_settings
from app.core.dependencies import get_current_user
from typing import Optional
from datetime import datetime, timedelta

router = APIRouter(prefix="/action-plans", tags=["action-plans"])


def get_supabase_client():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


@router.get("")
async def list_action_plans(
    evaluation_id: Optional[str] = None,
    status: Optional[str] = Query(None, description="Filter by status (pendiente, completado, etc)"),
    overdue: Optional[bool] = Query(None, description="Filter overdue items"),
    due_this_week: Optional[bool] = Query(None, description="Filter items due this week"),
    user: dict = Depends(get_current_user)
):
    """List action plans for the current user, optionally filtered"""
    supabase = get_supabase_client()

    query = supabase.table("action_plans").select("*").eq("owner_id", user["id"])

    if evaluation_id:
        query = query.eq("evaluation_id", evaluation_id)

    response = query.execute()

    # Apply filters that can't be done in Supabase query
    plans = response.data

    # Filter by status (case-insensitive)
    if status:
        status_lower = status.lower()
        plans = [p for p in plans if p.get("status", "").lower() == status_lower]

    # Filter overdue (due_date < now and status is not completed)
    if overdue:
        now = datetime.now().isoformat()
        plans = [
            p for p in plans
            if p.get("due_date") and p["due_date"] < now
            and p.get("status", "").lower() not in ("completado", "completed", "done")
        ]

    # Filter due this week
    if due_this_week:
        now = datetime.now()
        week_end = now + timedelta(days=7)
        plans = [
            p for p in plans
            if p.get("due_date")
            and p["due_date"] >= now.isoformat()
            and p["due_date"] <= week_end.isoformat()
        ]

    return plans


@router.post("")
async def create_action_plan(data: dict, user: dict = Depends(get_current_user)):
    """Create a new action plan"""
    supabase = get_supabase_client()

    plan_data = {
        **data,
        "owner_id": user["id"]
    }
    response = supabase.table("action_plans").insert(plan_data).execute()
    new_plan = response.data[0] if response.data else None

    # Trigger reminder email if due_date is set
    if new_plan and new_plan.get("due_date"):
        try:
            from app.email import resend_client
            resend_client.send_action_plan_reminder(
                user["email"],
                [{
                    "title": new_plan.get("title", "Sin título"),
                    "due_date": new_plan.get("due_date"),
                    "status": "pending"
                }]
            )
        except Exception as e:
            # Log error but don't fail the request
            import logging
            logging.getLogger(__name__).warning(f"Failed to send action plan reminder: {e}")

    return new_plan


@router.put("/{action_plan_id}")
async def update_action_plan(
    action_plan_id: str,
    data: dict,
    user: dict = Depends(get_current_user)
):
    """Update an action plan"""
    supabase = get_supabase_client()

    # Check ownership
    response = supabase.table("action_plans").select("*").eq("id", action_plan_id).eq("owner_id", user["id"]).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Action plan not found")

    update_data = {k: v for k, v in data.items() if k not in ["id", "owner_id", "created_at"]}
    updated = supabase.table("action_plans").update(update_data).eq("id", action_plan_id).execute()
    updated_plan = updated.data[0] if updated.data else None

    # Trigger reminder email if due_date was set or updated
    if updated_plan and updated_plan.get("due_date"):
        try:
            from app.email import resend_client
            resend_client.send_action_plan_reminder(
                user["email"],
                [{
                    "title": updated_plan.get("title", "Sin título"),
                    "due_date": updated_plan.get("due_date"),
                    "status": "pending"
                }]
            )
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Failed to send action plan reminder: {e}")

    return updated_plan


@router.delete("/{action_plan_id}")
async def delete_action_plan(action_plan_id: str, user: dict = Depends(get_current_user)):
    """Delete an action plan"""
    supabase = get_supabase_client()

    # Check ownership
    response = supabase.table("action_plans").select("id").eq("id", action_plan_id).eq("owner_id", user["id"]).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Action plan not found")

    supabase.table("action_plans").delete().eq("id", action_plan_id).execute()
    return {"message": "Deleted successfully"}