# Import du module time pour manipuler les timestamps
import time

# Import d'APIRouter depuis FastAPI pour créer un groupe de routes API
from fastapi import APIRouter

# Import de l'objet engine depuis le module controllers.engine
# Cet objet semble contenir la logique principale du moteur de détection
from controllers.engine import engine


# Création d'un routeur FastAPI
# prefix="/blacklist" signifie que toutes les routes commenceront par /blacklist
# tags=["Blacklist"] sert à organiser la documentation Swagger de l'API
router = APIRouter(prefix="/blacklist", tags=["Blacklist"])


# Définition d'une route GET accessible sur /blacklist
@router.get("")
def get_blacklist():
    
    # Liste qui contiendra les entrées de la blacklist formatées
    entries = []

    # Récupération du timestamp actuel (en secondes depuis epoch)
    now = time.time()

    # Parcours des entrées présentes dans la blacklist du moteur de détection
    # Chaque entrée semble être un tuple : (expiry, _, metadata)
    # expiry : timestamp d'expiration du bannissement
    # _ : valeur ignorée (probablement non utilisée ici)
    # metadata : dictionnaire contenant des informations sur l'attaque
    for expiry, _, metadata in engine.detector.blacklist.entries:

        # Ajout d'une entrée formatée dans la liste
        entries.append({

            # Récupération de l'adresse IP stockée dans metadata
            "ip": metadata.get("ip"),

            # Type d'attaque détectée
            "attack_type": metadata.get("attack_type"),

            # Temps restant avant la fin du bannissement
            # expiry - now donne le temps restant
            # max(0, ...) évite d'avoir une valeur négative si l'expiration est passée
            "expires_in": max(0, int(expiry - now)),
        })

    # Retourne la liste des entrées blacklistées sous forme JSON
    return entries