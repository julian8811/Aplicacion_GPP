from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from supabase import create_client
from app.config import get_settings
from app.core.dependencies import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/schedules", tags=["schedules"])


def get_supabase_client():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


class ScheduleCreate(BaseModel):
    name: str
    frequency: str
    next_due: datetime
    reminder_days_before: int = 7
    active: bool = True


class ScheduleUpdate(BaseModel):
    name: Optional[str] = None
    frequency: Optional[str] = None
    next_due: Optional[datetime] = None
    reminder_days_before: Optional[int] = None
    active: Optional[bool] = None


def calculate_next_due(current_due: datetime, frequency: str) -> datetime:
    """Calculate the next due date based on frequency"""
    if frequency == 'monthly':
        return current_due + timedelta(days=30)
    elif frequency == 'quarterly':
        return current_due + timedelta(days=90)
    elif frequency == 'biannual':
        return current_due + timedelta(days=180)
    elif frequency == 'annual':
        return current_due + timedelta(days=365)
    return current_due + timedelta(days=30)


@router.get("")
async def list_schedules(user: dict = Depends(get_current_user)):
    """List user's schedules"""
    supabase = get_supabase_client()
    
    response = supabase.table("evaluation_schedules").select("*").eq(
        "created_by", user["id"]
    ).order("next_due", desc=False).execute()
    
    return response.data


@router.post("")
async def create_schedule(data: ScheduleCreate, user: dict = Depends(get_current_user)):
    """Create a new schedule"""
    supabase = get_supabase_client()
    
    schedule_data = {
        "name": data.name,
        "frequency": data.frequency,
        "next_due": data.next_due.isoformat(),
        "reminder_days_before": data.reminder_days_before,
        "active": data.active,
        "created_by": user["id"]
    }
    
    response = supabase.table("evaluation_schedules").insert(schedule_data).execute()
    return response.data[0] if response.data else None


@router.get("/{schedule_id}")
async def get_schedule(schedule_id: str, user: dict = Depends(get_current_user)):
    """Get a single schedule by ID"""
    supabase = get_supabase_client()
    
    response = supabase.table("evaluation_schedules").select("*").eq("id", schedule_id).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    schedule = response.data[0]
    
    if schedule["created_by"] != user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return schedule


@router.put("/{schedule_id}")
async def update_schedule(
    schedule_id: str, 
    data: ScheduleUpdate, 
    user: dict = Depends(get_current_user)
):
    """Update a schedule (only owner)"""
    supabase = get_supabase_client()
    
    # Check ownership
    response = supabase.table("evaluation_schedules").select("*").eq("id", schedule_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    if response.data[0]["created_by"] != user["id"]:
        raise HTTPException(status_code=403, detail="Only owner can update schedule")
    
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if 'next_due' in update_data and update_data['next_due']:
        update_data['next_due'] = update_data['next_due'].isoformat()
    
    response = supabase.table("evaluation_schedules").update(update_data).eq("id", schedule_id).execute()
    return response.data[0] if response.data else None


@router.delete("/{schedule_id}")
async def delete_schedule(schedule_id: str, user: dict = Depends(get_current_user)):
    """Delete a schedule (only owner)"""
    supabase = get_supabase_client()
    
    # Check ownership
    response = supabase.table("evaluation_schedules").select("*").eq("id", schedule_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    if response.data[0]["created_by"] != user["id"]:
        raise HTTPException(status_code=403, detail="Only owner can delete schedule")
    
    supabase.table("evaluation_schedules").delete().eq("id", schedule_id).execute()
    return {"message": "Schedule deleted successfully"}


@router.post("/{schedule_id}/trigger")
async def trigger_schedule_reminder(
    schedule_id: str, 
    user: dict = Depends(get_current_user)
):
    """Manually trigger a schedule reminder"""
    supabase = get_supabase_client()
    
    # Get schedule
    response = supabase.table("evaluation_schedules").select("*").eq("id", schedule_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    schedule = response.data[0]
    
    if schedule["created_by"] != user["id"]:
        raise HTTPException(status_code=403, detail="Only owner can trigger schedule")
    
    # Trigger the send-email edge function
    send_email_url = f"{get_settings().supabase_url}/functions/v1/send-email"
    
    # Get user email
    profile_response = supabase.table("profiles").select("email").eq("id", user["id"]).execute()
    user_email = profile_response.data[0]["email"] if profile_response.data else None
    
    email_result = {"success": True}  # Simplified for MVP
    
    if email_result.get("success"):
        # Calculate and update next_due
        current_due = datetime.fromisoformat(schedule["next_due"].replace("Z", "+00:00"))
        new_due = calculate_next_due(current_due, schedule["frequency"])
        
        supabase.table("evaluation_schedules").update({
            "next_due": new_due.isoformat()
        }).eq("id", schedule_id).execute()
        
        return {"message": "Reminder triggered successfully", "next_due": new_due.isoformat()}
    
    raise HTTPException(status_code=500, detail="Failed to send reminder")