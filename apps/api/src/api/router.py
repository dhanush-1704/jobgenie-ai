from fastapi import APIRouter

from src.api.v1 import job, matching, resume
from src.api.v1.auth import router as auth_router
from src.api.v1.health import router as health_router

router = APIRouter()

router.include_router(health_router)
router.include_router(auth_router)
router.include_router(resume.router)
router.include_router(job.router)
router.include_router(matching.router)