import asyncio
from ddos_killer.DDosDetector import DDosDetector
from ddos_killer.config import Config
from ddos_killer.Logger import logger

class EngineService:
    def __init__(self):
        self.config = Config()
        self.detector = DDosDetector(self.config)
        self.task: asyncio.Task | None = None

    async def start(self):
        if self.task and not self.task.done():
            return False

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

    def status(self):
        return {
            "running": self.task is not None and not self.task.done(),
            "blacklist_size": len(self.detector.blacklist),
        }
