import logging
from supabase import create_client, Client
from app.config import get_settings

logger = logging.getLogger(__name__)


def get_supabase() -> Client | None:
    settings = get_settings()
    
    if not settings.supabase_url:
        logger.warning(
            "supabase_url is not set. Supabase client will not be available. "
            "Set SUPABASE_URL and SUPABASE_ANON_KEY environment variables to enable."
        )
        return None
    
    if not settings.supabase_anon_key:
        logger.warning(
            "supabase_anon_key is not set. Supabase client will not be available."
        )
        return None
    
    return create_client(settings.supabase_url, settings.supabase_anon_key)