import logging

import pandas as pd
from app.core.config import settings

class IBGEService:
    def __init__(self, session):
        self.session = session
        self.ibge_base_url = settings.urls["ibge_base_url"]
        self.logger = logging.getLogger(__name__)
        
    def obter_todos_municipios_ba(self):
        try:
            url = f"{self.ibge_base_url}/{settings.urls['ibge_municipio_suffix_url']}"
            response = self.session.get(url, timeout=settings.timeout)
            
            if response.ok:
                dados = response.json()
                return pd.DataFrame([
                    {
                        "CIDADE": m["nome"].upper(),
                        "CODIGO_IBGE": str(m["id"])[:6] 
                    } for m in dados
                ])
            
            self.logger.error(f"Falha ao obter lista do IBGE: Status {response.status_code}")
            return pd.DataFrame()
            
        except Exception as e:
            self.logger.error(f"Erro ao obter lista completa de municípios: {e}")
            return pd.DataFrame()