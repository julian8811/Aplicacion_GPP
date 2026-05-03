import os
import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import Optional
import uuid
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/drafts", tags=["drafts"])

# Drafts directory relative to backend root
DRAFTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "drafts")


def _ensure_drafts_dir():
    """Ensure drafts directory exists."""
    os.makedirs(DRAFTS_DIR, exist_ok=True)


@router.post("")
async def save_draft(data: dict, user: dict = Depends(get_current_user)):
    """
    Save evaluation draft as a JSON file.
    
    Request body:
    {
        "pa_values": {...},
        "po_values": {...},
        "fecha": "ISO date string",
        "establecimiento": "optional name"
    }
    """
    _ensure_drafts_dir()
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    filename = f"draft_{timestamp}_{unique_id}.json"
    filepath = os.path.join(DRAFTS_DIR, filename)
    
    # Add metadata
    draft_data = {
        "fecha_guardado": datetime.now().isoformat(),
        "pa_values": data.get("pa_values", {}),
        "po_values": data.get("po_values", {}),
        "fecha": data.get("fecha"),
        "establecimiento": data.get("establecimiento", ""),
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(draft_data, f, indent=2, ensure_ascii=False)
    
    return {"filename": filename, "path": filepath}


@router.get("/{filename}")
async def load_draft(filename: str, user: dict = Depends(get_current_user)):
    """
    Load a draft file by filename.
    
    Returns the draft JSON data including pa_values, po_values, and metadata.
    """
    _ensure_drafts_dir()
    
    # Sanitize filename to prevent path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    filepath = os.path.join(DRAFTS_DIR, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Draft not found")
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")


@router.get("")
async def list_drafts(user: dict = Depends(get_current_user)):
    """List all available draft files."""
    _ensure_drafts_dir()
    
    if not os.path.exists(DRAFTS_DIR):
        return []
    
    files = []
    for filename in os.listdir(DRAFTS_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(DRAFTS_DIR, filename)
            stat = os.stat(filepath)
            files.append({
                "filename": filename,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })
    
    return sorted(files, key=lambda x: x["modified"], reverse=True)
