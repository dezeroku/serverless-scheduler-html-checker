import requests


def get_html(url: str) -> str:
    return requests.get(url, timeout=10).text
