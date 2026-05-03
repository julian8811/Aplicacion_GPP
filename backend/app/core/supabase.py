"""
Centralized Supabase client initialization.
All code paths should use get_supabase_client() from this module.
"""
from functools import lru_cache
from supabase import create_client, Client
from app.config import get_settings


@lru_cache()
def get_supabase_client() -> Client:
    """
    Get a Supabase client instance configured from environment variables.
    Uses lru_cache to ensure the same instance is returned on repeated calls.
    """
    settings = get_settings()
    if not settings.supabase_url or not settings.supabase_anon_key:
        raise ValueError(
            "Missing required Supabase configuration. "
            "Ensure SUPABASE_URL and SUPABASE_ANON_KEY are set in environment."
        )
    return create_client(settings.supabase_url, settings.supabase_anon_key)


@lru_cache()
def get_supabase_admin_client() -> Client:
    """
    Get a Supabase admin client with service role key.
    Used for privileged operations that require admin access.
    """
    settings = get_settings()
    if not settings.supabase_url or not settings.supabase_service_key:
        raise ValueError(
            "Missing required Supabase admin configuration. "
            "Ensure SUPABASE_URL and SUPABASE_SERVICE_KEY are set in environment."
        )
    return create_client(settings.supabase_url, settings.supabase_service_key)