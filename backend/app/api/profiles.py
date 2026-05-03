from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from supabase import create_client
from app.config import get_settings

router = APIRouter(prefix="/profiles", tags=["profiles"])


def get_supabase_client():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


class ProfileUpdate(BaseModel):
    full_name: str | None = None
    establishment_name: str | None = None


@router.get("/me")
async def get_profile():
    supabase = get_supabase_client()
    # Return a default profile since we don't have real auth
    return {
        "id": "00000000-0000-0000-0000-000000000000",
        "email": "guest@local",
        "full_name": None,
        "role": "owner",
        "establishment_name": None
    }


@router.patch("/me")
async def update_profile(data: ProfileUpdate):
    supabase = get_supabase_client()
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    response = supabase.table("profiles").update(update_data).eq("id", "00000000-0000-0000-0000-000000000000").execute()
    return response.data[0] if response.data else None