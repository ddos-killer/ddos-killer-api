from fastapi import APIRouter
from services.engine_service import EngineService

router = APIRouter(prefix="/engine", tags=["Engine"])
engine = EngineService()

@router.post("/start")
async def start():
    return {"started": await engine.start()}

@router.post("/stop")
async def stop():
    return {"stopped": await engine.stop()}

@router.get("/status")
def status():
    return engine.status()

@router.post("/threshold")
async def threshold(attack_type: str, threshold: int):
    return {"changed": await engine.set_threshold(attack_type, threshold) }
