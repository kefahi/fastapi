
import logging
import logging.handlers
import json_logging
from utils.settings import settings

logger = logging.getLogger(settings.app_name)
logger.setLevel(logging.INFO)
log_handler = logging.handlers.RotatingFileHandler(filename=settings.log_path + '/x-ljson.log', maxBytes=5000000, backupCount=10)
logger.addHandler(log_handler)
