from fastapi import APIRouter, Query
from typing import Optional, List
from supabase import create_client
from app.config import get_settings

router = APIRouter(prefix="/benchmarks", tags=["benchmarks"])


def get_supabase_client():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


@router.get("")
async def list_benchmarks(
    sector: Optional[str] = Query(None, description="Filter by sector"),
    category: Optional[str] = Query(None, description="Filter by category (PA or PO)")
):
    """List industry benchmarks (public, no auth required)"""
    supabase = get_supabase_client()
    
    query = supabase.table("industry_benchmarks").select("*")
    
    if sector:
        query = query.eq("sector", sector)
    
    if category:
        query = query.eq("category", category)
    
    response = query.order("category").order("aspect").execute()
    
    return response.data


@router.get("/{benchmark_id}")
async def get_benchmark(benchmark_id: str):
    """Get a single benchmark by ID (public)"""
    supabase = get_supabase_client()
    
    response = supabase.table("industry_benchmarks").select("*").eq("id", benchmark_id).execute()
    
    if not response.data:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Benchmark not found")
    
    return response.data[0]


@router.get("/sectors/list")
async def list_sectors():
    """List all available sectors"""
    supabase = get_supabase_client()
    
    response = supabase.table("industry_benchmarks").select("sector").execute()
    
    sectors = list(set(item["sector"] for item in response.data))
    return [{"sector": s} for s in sorted(sectors)]