import logging
import requests

from app.core import logger
from app.core.config import settings

class OSRMService:
    def __init__(self):
        logger.configurar_logger()

        self.logger = logging.getLogger(
            __name__
        )

        self.base_url = settings.urls[
            "osrm_base_url"
        ]

        self.session = requests.Session()

    def calculate_osrm(
        self,
        lat_origem,
        lon_origem,
        lat_destino,
        lon_destino
    ):
        try:
            url = (
                f"{self.base_url}/"
                f"{settings.urls['osrm_driving_suffix_url']}/"
                f"{lon_origem},{lat_origem};"
                f"{lon_destino},{lat_destino}"
                "?overview=false"
            )

            r = self.session.get(
                url,
                timeout=10
            )

            r.raise_for_status()

            data = r.json()

            if (
                "routes" not in data
                or not data["routes"]
            ):
                self.logger.warning(
                    "[OSRM] Nenhuma rota encontrada"
                )

                return None

            route = data["routes"][0]

            distancia_km = round(
                route["distance"] / 1000,
                4
            )

            tempo_segundos = round(
                route["duration"],
                2
            )

            tempo_minutos = round(
                tempo_segundos / 60,
                2
            )

            tempo_horas = round(
                tempo_minutos / 60,
                2
            )

            return {
                "distancia_km": distancia_km,
                "tempo_segundos": tempo_segundos,
                "tempo_minutos": tempo_minutos,
                "tempo_horas": tempo_horas
            }

        except Exception as e:
            self.logger.error(
                f"[OSRM ERROR] {e}"
            )

            return None