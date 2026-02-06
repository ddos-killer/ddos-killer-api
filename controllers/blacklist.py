import time
from fastapi import APIRouter
from controllers.engine import engine

router = APIRouter(prefix="/blacklist", tags=["Blacklist"])


@router.get("")
def get_blacklist():
    entries = []

    now = time.time()

    for expiry, _, metadata in engine.detector.blacklist.entries:
        entries.append({
            "ip": metadata.get("ip"),
            "attack_type": metadata.get("attack_type"),
            "expires_in": max(0, int(expiry - now)),
        })

    return entries
