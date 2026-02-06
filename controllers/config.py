from fastapi import APIRouter
from controllers.engine import engine

router = APIRouter(prefix="/config", tags=["Config"])


@router.get("")
def get_config():
    return engine.config.__dict__


@router.post("")
def update_config(new_config: dict):
    updated = {}

    for key, value in new_config.items():
        if hasattr(engine.config, key):
            setattr(engine.config, key, value)
            updated[key] = value

    return {
        "status": "updated",
        "updated_fields": updated,
    }
