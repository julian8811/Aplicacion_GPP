from typing import Optional
from fastapi import Header, HTTPException, Request
from supabase import create_client
from app.config import get_settings


def get_supabase_client():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


async def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """
    Validates the JWT token from Authorization header and returns the user.
    Raises 401 if token is missing or invalid.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization[7:]

    try:
        supabase = get_supabase_client()
        session_response = supabase.auth.set_session(access_token=token, refresh_token="")
        user = session_response.user
        user_metadata = user.user_metadata or {}

        return {
            "id": user.id,
            "email": user.email or "",
            "role": user_metadata.get("role", "editor"),
            "establishment_name": user_metadata.get("establishment_name")
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


async def get_optional_user(authorization: Optional[str] = Header(None)) -> Optional[dict]:
    """
    Returns the user if authenticated, None otherwise.
    Used for guest mode - doesn't raise an error if no token.
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None

    try:
        return await get_current_user(authorization)
    except HTTPException:
        return None


def require_role(roles: list):
    """
    Dependency factory that creates a role checker.
    Usage: async def endpoint(user: dict = Depends(require_role(["admin", "editor"]))):
    """
    async def role_checker(request: Request) -> dict:
        user = await get_current_user(
            request.headers.get("authorization")
        )
        if user.get("role") not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user

    return role_checker


# Keep guest user for backwards compatibility
async def get_guest_user():
    """Returns a hardcoded guest user for all requests (DEPRECATED - use get_optional_user with ?mode=guest)"""
    return {
        "id": "00000000-0000-0000-0000-000000000000",
        "email": "guest@local",
        "role": "owner"
    }