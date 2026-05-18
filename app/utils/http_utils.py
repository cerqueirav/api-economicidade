import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from app.core.config import settings

def criar_session():
    retries = settings.proc_params["retries"]

    retry_strategy = Retry(
        total=retries,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session