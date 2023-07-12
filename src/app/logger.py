import logging
import logging.config
import logging_loki
from os import path
from config import NAME, LOKIURL

handler = logging_loki.LokiHandler(
    url=LOKIURL + "/loki/api/v1/push", 
    tags={"application": NAME},
    version="1",
)
log_file_path = path.join(path.dirname(path.abspath(__file__)), "logger.conf")

logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

log = logging.getLogger(__name__)
log.addHandler(handler)
