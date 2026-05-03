from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from supabase import create_client
from app.config import get_settings
from app.core.dependencies import get_current_user
from typing import Optional

router = APIRouter(prefix="/profiles", tags=["profiles"])


def get_supabase_client():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


class BrandingFields(BaseModel):
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    footer_text: Optional[str] = None


class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    establishment_name: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    footer_text: Optional[str] = None


@router.get("/me")
async def get_profile(user: dict = Depends(get_current_user)):
    """Get current user's profile with branding fields"""
    supabase = get_supabase_client()
    response = supabase.table("profiles").select("*").eq("id", user["id"]).execute()
    if response.data:
        return response.data[0]
    return {
        "id": user["id"],
        "email": user.get("email"),
        "full_name": None,
        "role": "owner",
        "establishment_name": None,
        "logo_url": None,
        "primary_color": None,
        "footer_text": None
    }


@router.patch("/me")
async def update_profile(data: ProfileUpdate, user: dict = Depends(get_current_user)):
    """Update current user's profile including branding fields"""
    supabase = get_supabase_client()
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    response = supabase.table("profiles").update(update_data).eq("id", user["id"]).execute()
    return response.data[0] if response.data else None


@router.get("/me/branding")
async def get_branding(user: dict = Depends(get_current_user)):
    """Get branding configuration for PDF generation"""
    supabase = get_supabase_client()
    response = supabase.table("profiles").select("logo_url", "primary_color", "footer_text").eq("id", user["id"]).execute()
    if response.data:
        return response.data[0]
    return {
        "logo_url": None,
        "primary_color": "#2563eb",  # Default blue
        "footer_text": None
    }