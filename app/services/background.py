import asyncio
from app.core.logger import get_logger

logger = get_logger("background")


class BackgroundService:
    @staticmethod
    async def retry_task(task_func, retries=3, delay=2):
        for attempt in range(1, retries + 1):
            try:
                await task_func()
                return
            except Exception as e:
                logger.warning(
                    f"task_retry attempt={attempt} error={str(e)}"
                )
                if attempt == retries:
                    logger.error("task_failed_after_retries")
                    raise
                await asyncio.sleep(delay)
