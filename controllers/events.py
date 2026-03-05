# Import d'APIRouter depuis FastAPI
# Permet de regrouper plusieurs routes liées à une même fonctionnalité
from fastapi import APIRouter

# Import de l'objet engine depuis le module controllers.engine
# Cet objet contient probablement le moteur de détection et ses données
from controllers.engine import engine


# Création d'un routeur FastAPI
# prefix="/events" → toutes les routes commenceront par /events
# tags=["Events"] → permet d'organiser les routes dans la documentation Swagger
router = APIRouter(prefix="/events", tags=["Events"])


# Route GET accessible sur /events
# Elle permet de récupérer les derniers événements détectés par le moteur
@router.get("")
def get_events(limit: int = 50):

    # engine.detector.events semble être une liste contenant les événements détectés
    # [-limit:] permet de récupérer uniquement les "limit" derniers éléments
    # Par défaut, on renvoie les 50 derniers événements
    return engine.detector.events[-limit:]