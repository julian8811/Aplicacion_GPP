from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.config import get_settings

app = FastAPI(title="GPP API", version="1.0.0", description="Gestion Por Procesos API")

# Startup configuration validation
settings = get_settings()
required_config = [
    ("SUPABASE_URL", settings.supabase_url),
    ("SUPABASE_ANON_KEY", settings.supabase_anon_key),
]
missing_config = [name for name, value in required_config if not value]
if missing_config:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing_config)}. "
        "Set these variables before starting the application."
    )

# Build allowed origins from environment and defaults
dynamic_origins = []
if settings.VERCEL_URL:
    dynamic_origins.append(f"https://{settings.VERCEL_URL}")
if settings.RAILWAY_PUBLIC_DOMAIN:
    dynamic_origins.append(f"https://{settings.RAILWAY_PUBLIC_DOMAIN}")

# Static local origins
static_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

# Parse configurable CORS_ORIGINS from env (comma-separated, supports wildcards)
env_cors_origins = []
if settings.cors_origins:
    env_cors_origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]

# Add Vercel wildcard for all subdomains
vercel_wildcard = "https://*.vercel.app"

# Combine and filter out empty strings
all_origins = list(filter(None, set(static_origins + dynamic_origins + env_cors_origins + [vercel_wildcard])))

app.add_middleware(
    CORSMiddleware,
    allow_origins=all_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router)


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/")
def root():
    return {"message": "GPP API - Gestion Por Procesos"}