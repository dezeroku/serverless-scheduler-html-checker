import difflib
import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_html(url: str) -> str:
    logger.debug("Get state for: %s", url)
    return requests.get(url, timeout=10).text


def _prepare_html_to_diff(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    temp = soup.prettify()
    return list(map(lambda x: x + "</br>", temp.split("\n")))


def generate_html_diff(old: str, new: str) -> str:
    logger.debug("Generate HTML diff")

    old_list = _prepare_html_to_diff(old)
    new_list = _prepare_html_to_diff(new)

    # Length is limited to not overflow the SES send message
    return (
        "<p>"
        + "<p>".join(
            list(
                difflib.unified_diff(
                    old_list,
                    new_list,
                    fromfile="previous",
                    tofile="current",
                    lineterm="</p></br>",
                )
            )
        )
        + "</p>"
    )[:2600]
