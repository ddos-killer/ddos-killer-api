# Import d'APIRouter depuis FastAPI
# Permet de regrouper des routes liées à une même fonctionnalité
from fastapi import APIRouter

# Import du service qui encapsule la logique métier du moteur
# EngineService gère probablement le démarrage, l'arrêt et la configuration du moteur
from services.engine_service import EngineService


# Création d'un routeur pour les endpoints liés au moteur
# prefix="/engine" : toutes les routes commenceront par /engine
# tags=["Engine"] : permet de regrouper ces endpoints dans la documentation Swagger
router = APIRouter(prefix="/engine", tags=["Engine"])


# Création d'une instance du service moteur
# Cette instance sera utilisée par les différentes routes
engine = EngineService()


# Route POST /engine/start
# Permet de démarrer le moteur
@router.post("/start")
async def start():

    # Appelle la méthode start du service moteur
    # await car la fonction est asynchrone
    return {"started": await engine.start()}


# Route POST /engine/stop
# Permet d'arrêter le moteur
@router.post("/stop")
async def stop():

    # Appelle la méthode stop du moteur
    return {"stopped": await engine.stop()}


# Route GET /engine/status
# Permet de connaître l'état actuel du moteur
@router.get("/status")
def status():

    # Retourne l'état du moteur (par exemple : running, stopped, etc.)
    return engine.status()


# Route POST /engine/threshold
# Permet de modifier le seuil de détection d'un type d'attaque
@router.post("/threshold")
async def threshold(attack_type: str, threshold: int):

    # Appelle la méthode set_threshold du moteur
    # attack_type : type d'attaque (ex: bruteforce, scan, etc.)
    # threshold : nombre de tentatives avant déclenchement
    return {"changed": await engine.set_threshold(attack_type, threshold)}