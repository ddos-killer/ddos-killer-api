import asyncio
from ddos_killer.DDosDetector import DDosDetector
from ddos_killer.config import Config
from ddos_killer.Logger import logger

class EngineService:
    def __init__(self):
        self.config = Config()
        self.detector = DDosDetector(self.config)
        self.task: asyncio.Task | None = None
        self._context_entered = False

    async def __aenter__(self):
        """Entre dans le context manager du service"""
        await self.detector.__aenter__()
        self._context_entered = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Sort du context manager du service"""
        if self._context_entered:
            await self.detector.__aexit__(exc_type, exc_val, exc_tb)
            self._context_entered = False

    async def start(self):
        if self.task and not self.task.done():
            return False
        
        if not self._context_entered:
            await self.detector.__aenter__()
            self._context_entered = True

        async def runner():
            async with self.detector:
                initialized = await self.detector.run()
                if not initialized:
                    return False


        self.task = asyncio.create_task(runner())
        logger.info("Engine started")
        return True

    async def stop(self):
        if self.task:
            self.task.cancel()
            logger.info("Engine stopped")
            return True
        return False
    
    async def set_threshold(self, attack_type: str, threshold: int):
        if not self.task or self.task.done():
            return False
        
        return await self.detector.set_threshold(attack_type, threshold)

    def status(self):
        return {
            "running": self.task is not None and not self.task.done(),
            "blacklist_size": len(self.detector.blacklist),
        }
