"""
Notification API endpoints for email management.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.config import get_settings
from app.core.dependencies import get_current_user
from app.email import resend_client

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/notifications", tags=["notifications"])


class SendEmailRequest(BaseModel):
    type: str  # "welcome" | "action_plan_reminder" | "weekly_summary"
    user_id: Optional[str] = None
    data: Optional[dict] = None


class TestEmailRequest(BaseModel):
    email: str


@router.post("/send")
async def send_notification(
    request: SendEmailRequest,
    user: dict = Depends(get_current_user)
):
    """
    Manually trigger an email notification (admin only).
    For now, any authenticated user can use this endpoint.
    """
    # Check if user has admin role (you may want to add this check)
    # For now, we'll allow any authenticated user

    email_type = request.type
    data = request.data or {}

    try:
        if email_type == "welcome":
            name = data.get("name", user.get("email", "Usuario"))
            establishment_name = data.get("establishment_name", get_settings().establishment_name)
            result = resend_client.send_welcome_email(user["email"], name, establishment_name)

        elif email_type == "action_plan_reminder":
            action_plans = data.get("action_plans", [])
            result = resend_client.send_action_plan_reminder(user["email"], action_plans)

        elif email_type == "weekly_summary":
            stats = data.get("stats", {
                "evaluations_completed": 0,
                "pending_action_plans": 0,
                "overdue_action_plans": 0
            })
            result = resend_client.send_weekly_summary(user["email"], stats)

        else:
            raise HTTPException(status_code=400, detail=f"Unknown email type: {email_type}")

        if result.get("success"):
            return {"success": True, "message_id": result.get("message_id")}
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to send email"))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test")
async def send_test_email(
    request: TestEmailRequest,
    user: dict = Depends(get_current_user)
):
    """
    Send a test email to the specified address.
    Useful for verifying email configuration.
    """
    try:
        result = resend_client.send_welcome_email(
            request.email,
            "Test User",
            get_settings().establishment_name
        )

        if result.get("success"):
            return {
                "success": True,
                "message": f"Test email sent to {request.email}",
                "message_id": result.get("message_id")
            }
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to send test email"))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending test email: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/preferences")
async def get_notification_preferences(user: dict = Depends(get_current_user)):
    """
    Get user's notification preferences from profiles table.
    """
    from supabase import create_client

    settings = get_settings()
    supabase = create_client(settings.supabase_url, settings.supabase_anon_key)

    response = supabase.table("profiles").select("notification_preferences").eq("id", user["id"]).execute()

    if response.data:
        prefs = response.data[0].get("notification_preferences")
        return {
            "action_plan_reminders": prefs.get("action_plan_reminders", True) if prefs else True,
            "weekly_summary": prefs.get("weekly_summary", True) if prefs else True,
            "marketing": prefs.get("marketing", False) if prefs else False,
        }

    # Return defaults if no preferences stored
    return {
        "action_plan_reminders": True,
        "weekly_summary": True,
        "marketing": False,
    }


class NotificationPreferences(BaseModel):
    action_plan_reminders: bool = True
    weekly_summary: bool = True
    marketing: bool = False


@router.put("/preferences")
async def update_notification_preferences(
    preferences: NotificationPreferences,
    user: dict = Depends(get_current_user)
):
    """
    Update user's notification preferences in profiles table.
    """
    from supabase import create_client

    settings = get_settings()
    supabase = create_client(settings.supabase_url, settings.supabase_anon_key)

    prefs_dict = {
        "action_plan_reminders": preferences.action_plan_reminders,
        "weekly_summary": preferences.weekly_summary,
        "marketing": preferences.marketing,
    }

    response = supabase.table("profiles").update({
        "notification_preferences": prefs_dict
    }).eq("id", user["id"]).execute()

    if response.data:
        return {"success": True, "preferences": prefs_dict}

    raise HTTPException(status_code=500, detail="Failed to update preferences")