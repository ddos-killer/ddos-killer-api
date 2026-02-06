from fastapi import APIRouter
from controllers.engine import engine

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("")
def get_events(limit: int = 50):
    return engine.detector.events[-limit:]
