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

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
log.addHandler(handler)
