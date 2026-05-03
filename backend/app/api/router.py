from fastapi import APIRouter
from app.api import evaluations, results, action_plans, matrices, pdf, recommendations, profiles, drafts, exports, notifications
from app.auth.router import router as auth_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(profiles.router)
api_router.include_router(evaluations.router)
api_router.include_router(results.router)
api_router.include_router(action_plans.router)
api_router.include_router(matrices.router)
api_router.include_router(pdf.router)
api_router.include_router(recommendations.router)
api_router.include_router(drafts.router)
api_router.include_router(exports.router)
api_router.include_router(notifications.router)