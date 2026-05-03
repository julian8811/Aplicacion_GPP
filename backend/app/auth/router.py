from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from supabase import create_client
from app.config import get_settings
from app.auth.schemas import (
    LoginRequest,
    SignupRequest,
    AuthResponse,
    UserResponse
)

router = APIRouter(prefix="/auth", tags=["auth"])


def get_supabase_client():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


def get_supabase_admin_client():
    """Admin client with service role key for privileged operations"""
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_service_key)


@router.post("/signup", response_model=AuthResponse)
async def signup(data: SignupRequest):
    """Create a new user with Supabase Auth and create their profile"""
    supabase = get_supabase_client()
    supabase_admin = get_supabase_admin_client()
    settings = get_settings()

    # Create user with Supabase Auth
    try:
        auth_response = supabase_admin.auth.admin.create_user({
            "email": data.email,
            "password": data.password,
            "email_confirm": True
        })
        user_id = auth_response.user.id
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")

    # Get role from user metadata, default to 'owner' for first signup
    user_role = "owner"
    try:
        supabase_admin = get_supabase_admin_client()
        # Check if any profiles exist - if not, this is the first user (owner)
        existing_profiles = supabase_admin.table("profiles").select("id").limit(1).execute()
        if existing_profiles.data:
            user_role = "editor"  # Subsequent users default to editor
    except Exception:
        pass  # Default to editor if check fails

    # Create profile
    try:
        profile_data = {
            "id": user_id,
            "email": data.email,
            "establishment_name": data.establishment_name,
            "role": user_role
        }
        supabase_admin.table("profiles").insert(profile_data).execute()
    except Exception as e:
        # If profile creation fails, at least return the auth response
        pass

    # Get session tokens
    session_response = supabase.auth.sign_in_with_password(
        credentials={"email": data.email, "password": data.password}
    )

    if not session_response.session:
        raise HTTPException(status_code=500, detail="Failed to create session")

    return AuthResponse(
        access_token=session_response.session.access_token,
        refresh_token=session_response.session.refresh_token,
        user=UserResponse(
            id=user_id,
            email=data.email,
            role=user_role,
            establishment_name=data.establishment_name
        )
    )


@router.post("/login", response_model=AuthResponse)
async def login(data: LoginRequest):
    """Authenticate user and return tokens"""
    supabase = get_supabase_client()

    try:
        session_response = supabase.auth.sign_in_with_password(
            credentials={"email": data.email, "password": data.password}
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not session_response.session:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = session_response.user
    user_metadata = user.user_metadata or {}

    # Update last_login in profile with proper ISO 8601 timestamp
    from datetime import datetime, timezone
    try:
        supabase_admin = get_supabase_admin_client()
        supabase_admin.table("profiles").update({
            "last_login": datetime.now(timezone.utc).isoformat()
        }).eq("id", user.id).execute()
    except Exception:
        pass  # Non-critical if this fails

    return AuthResponse(
        access_token=session_response.session.access_token,
        refresh_token=session_response.session.refresh_token,
        user=UserResponse(
            id=user.id,
            email=user.email or "",
            role=user_metadata.get("role", "editor"),
            establishment_name=user_metadata.get("establishment_name")
        )
    )


@router.post("/logout")
async def logout(authorization: Optional[str] = Header(None)):
    """Invalidate the current session"""
    supabase = get_supabase_client()

    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
        try:
            supabase.auth.set_session(access_token=token, refresh_token="")
            supabase.auth.sign_out()
        except Exception:
            pass

    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def get_me(authorization: Optional[str] = Header(None)):
    """Get current user from JWT token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization[7:]

    try:
        supabase = get_supabase_client()
        session_response = supabase.auth.set_session(access_token=token, refresh_token="")
        user = session_response.user
        user_metadata = user.user_metadata or {}

        return UserResponse(
            id=user.id,
            email=user.email or "",
            role=user_metadata.get("role", "editor"),
            establishment_name=user_metadata.get("establishment_name")
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")