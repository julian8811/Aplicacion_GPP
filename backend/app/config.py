from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Supabase (required for production)
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_key: str = ""
    supabase_db_password: str = ""

    # Google OAuth (optional)
    google_client_id: str = ""
    google_client_secret: str = ""

    # Deployment-specific (optional)
    VERCEL_URL: str = ""
    RAILWAY_PUBLIC_DOMAIN: str = ""
    port: int = 8080

    # CORS - comma-separated list of allowed origins
    cors_origins: str = ""

    establishment_name: str = "Establecimiento GPP"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()