from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from supabase import create_client
from app.config import get_settings
from app.core.dependencies import get_current_user
from datetime import datetime
import zipfile
import io
import json

router = APIRouter(prefix="/export", tags=["export"])


def get_supabase_client():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


@router.get("/backup")
async def generate_full_backup(user: dict = Depends(get_current_user)):
    """Generate a full ZIP backup of all user data (admin only)"""
    supabase = get_supabase_client()
    
    # Check if user is admin
    profile_response = supabase.table("profiles").select("role").eq("id", user["id"]).execute()
    
    if not profile_response.data:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if profile_response.data[0].get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Create ZIP file in memory
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # 1. Export all evaluations as JSON
        evaluations_response = supabase.table("evaluations").select("*").execute()
        evaluations = evaluations_response.data
        
        evaluations_folder = "evaluations"
        for eval_data in evaluations:
            eval_json = json.dumps(eval_data, indent=2, default=str)
            eval_filename = f"{evaluations_folder}/evaluation_{eval_data['id'][:8]}_{eval_data.get('fecha', 'nodate')}.json"
            zip_file.writestr(eval_filename, eval_json)
        
        # 2. Export all action plans as CSV
        action_plans_response = supabase.table("action_plans").select("*").execute()
        action_plans = action_plans_response.data
        
        if action_plans:
            csv_lines = ["id,evaluation_id,element,action,responsible,due_date,status,description,created_at"]
            for plan in action_plans:
                line = f"{plan.get('id','')},{plan.get('evaluation_id','')},{plan.get('element','')},{plan.get('action','')},{plan.get('responsible','')},{plan.get('due_date','')},{plan.get('status','')},{plan.get('description','')},{plan.get('created_at','')}"
                csv_lines.append(line)
            zip_file.writestr("action_plans.csv", "\n".join(csv_lines))
        
        # 3. Export all recommendations as CSV
        recommendations_response = supabase.table("recommendations").select("*").execute()
        recommendations = recommendations_response.data
        
        if recommendations:
            csv_lines = ["id,evaluation_id,aspect,element,recommendation,priority,current_score,created_at"]
            for rec in recommendations:
                line = f"{rec.get('id','')},{rec.get('evaluation_id','')},{rec.get('aspect','')},{rec.get('element','')},{rec.get('recommendation','')},{rec.get('priority','')},{rec.get('current_score','')},{rec.get('created_at','')}"
                csv_lines.append(line)
            zip_file.writestr("recommendations.csv", "\n".join(csv_lines))
        
        # 4. Export all templates as JSON
        templates_response = supabase.table("evaluation_templates").select("*").execute()
        templates = templates_response.data
        
        templates_folder = "templates"
        for tmpl in templates:
            tmpl_json = json.dumps(tmpl, indent=2, default=str)
            tmpl_filename = f"{templates_folder}/template_{tmpl['id'][:8]}.json"
            zip_file.writestr(tmpl_filename, tmpl_json)
        
        # 5. Create metadata.json
        metadata = {
            "export_date": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "description": "GPP Full Backup Export",
            "stats": {
                "total_evaluations": len(evaluations),
                "total_action_plans": len(action_plans),
                "total_recommendations": len(recommendations),
                "total_templates": len(templates)
            }
        }
        zip_file.writestr("metadata.json", json.dumps(metadata, indent=2))
    
    # Prepare response
    zip_buffer.seek(0)
    
    filename = f"gpp_backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.zip"
    
    return Response(
        content=zip_buffer.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )