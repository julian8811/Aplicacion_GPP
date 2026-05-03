from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.config import get_settings

app = FastAPI(title="GPP API", version="1.0.0", description="Gestion Por Procesos API")

# CORS middleware
settings = get_settings()

# Build allowed origins dynamically from environment
dynamic_origins = []
if settings.VERCEL_URL:
    dynamic_origins.append(f"https://{settings.VERCEL_URL}")
if settings.RAILWAY_PUBLIC_DOMAIN:
    dynamic_origins.append(f"https://{settings.RAILWAY_PUBLIC_DOMAIN}")

# Static local origins
static_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://frontend-iota-blond-75.vercel.app",
    "https://*.vercel.app",
]

# Combine and filter out empty strings
origins = list(filter(None, set(static_origins + dynamic_origins)))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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