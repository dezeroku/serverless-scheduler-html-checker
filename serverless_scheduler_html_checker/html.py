import logging

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_html(url: str) -> str:
    logger.debug("Get state for: %s", url)
    return requests.get(url, timeout=10).text
