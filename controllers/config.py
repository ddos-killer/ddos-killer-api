# Import d'APIRouter depuis FastAPI
# APIRouter permet de regrouper des routes API liées entre elles
from fastapi import APIRouter

# Import du moteur principal de l'application
# Cet objet "engine" contient probablement la configuration et la logique centrale
from controllers.engine import engine


# Création d'un routeur FastAPI
# prefix="/config" signifie que toutes les routes commenceront par /config
# tags=["Config"] sert à organiser les routes dans la documentation Swagger
router = APIRouter(prefix="/config", tags=["Config"])


# Route GET accessible via /config
# Elle permet de récupérer la configuration actuelle du moteur
@router.get("")
def get_config():
    
    # __dict__ retourne tous les attributs de l'objet sous forme de dictionnaire
    # Cela permet d'exposer toute la configuration actuelle
    return engine.config.__dict__


# Route POST accessible via /config
# Elle permet de modifier dynamiquement la configuration
@router.post("")
def update_config(new_config: dict):

    # Dictionnaire qui contiendra les champs réellement modifiés
    updated = {}

    # Parcours des champs envoyés dans la requête JSON
    for key, value in new_config.items():

        # Vérifie que l'attribut existe dans la configuration actuelle
        # Cela évite d'ajouter des champs inexistants
        if hasattr(engine.config, key):

            # Met à jour la valeur de l'attribut dans la configuration
            setattr(engine.config, key, value)

            # Ajoute le champ modifié dans le dictionnaire de retour
            updated[key] = value

    # Retour de la réponse API
    return {
        "status": "updated",          # indique que la mise à jour a été effectuée
        "updated_fields": updated,    # liste des champs réellement modifiés
    }