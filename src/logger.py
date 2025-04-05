from loguru import logger
import sys

# Remove default logger to avoid duplicate logs
logger.remove()

logger.add(sys.stdout, format="{level}:     {time} | {message}", level="INFO", enqueue=True)
logger.info("Logger initialized")
