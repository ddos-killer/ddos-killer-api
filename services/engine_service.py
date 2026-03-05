# Import du module asyncio pour gérer les tâches asynchrones
import asyncio

# Import du détecteur DDoS principal
from ddos_killer.DDosDetector import DDosDetector

# Import de la configuration du moteur
from ddos_killer.config import Config

# Import du logger pour enregistrer les événements du moteur
from ddos_killer.Logger import logger


class EngineService:

    def __init__(self):
        # Création d'une instance de configuration
        self.config = Config()

        # Initialisation du détecteur DDoS avec la configuration
        self.detector = DDosDetector(self.config)

        # Référence vers la tâche asynchrone qui exécutera le moteur
        self.task: asyncio.Task | None = None

        # Indique si le context manager du détecteur a été activé
        self._context_entered = False


    async def __aenter__(self):
        """Entre dans le context manager du service"""

        # Initialise les ressources nécessaires au détecteur
        await self.detector.__aenter__()

        # Marque que le context manager est actif
        self._context_entered = True

        return self


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Sort du context manager du service"""

        # Si le context manager a été activé
        if self._context_entered:

            # Libère les ressources utilisées par le détecteur
            await self.detector.__aexit__(exc_type, exc_val, exc_tb)

            self._context_entered = False


    async def start(self):
        # Si une tâche existe déjà et qu'elle n'est pas terminée,
        # le moteur est déjà en cours d'exécution
        if self.task and not self.task.done():
            return False

        # Si le context manager n'a pas encore été activé
        if not self._context_entered:
            await self.detector.__aenter__()
            self._context_entered = True


        # Fonction interne qui exécutera le moteur
        async def runner():

            # Utilise le détecteur comme context manager
            async with self.detector:

                # Lance la boucle principale du détecteur
                initialized = await self.detector.run()

                # Si l'initialisation échoue
                if not initialized:
                    return False


        # Création d'une tâche asynchrone qui exécute le moteur
        self.task = asyncio.create_task(runner())

        logger.info("Engine started")

        return True


    async def stop(self):
        # Si une tâche existe
        if self.task:

            # Annule la tâche (arrête le moteur)
            self.task.cancel()

            logger.info("Engine stopped")

            return True

        return False
    

    async def set_threshold(self, attack_type: str, threshold: int):

        # Si le moteur n'est pas actif
        if not self.task or self.task.done():
            return False

        # Modifie dynamiquement le seuil de détection
        return await self.detector.set_threshold(attack_type, threshold)


    def status(self):
        # Retourne l'état du moteur
        return {
            # Indique si le moteur est en cours d'exécution
            "running": self.task is not None and not self.task.done(),

            # Nombre d'IP actuellement dans la blacklist
            "blacklist_size": len(self.detector.blacklist),
        }