from app.core import logger
from app.core.config import settings

class DemasService:
    def __init__(self, session):
        self.session = session
        self.logger = logger
        self.demas_base_url = settings.urls["demas_base_url"]
        self.suffix_url_cnes = settings.urls["demas_estabelecimentos_suffix_url"]
        self.suffix_url_macro = settings.urls["demas_macrorregiao_suffix_url"]
        self.timeout = settings.timeout
        
    def obter_dados_unidade(self, cnes_id: str):
        """Busca dados da unidade para extrair o código IBGE"""
        try:
            url = f"{self.demas_base_url}/{self.suffix_url_cnes}/{cnes_id}"
            response = self.session.get(url, timeout=self.timeout)
            return response.json() if response.ok else None
        except Exception as e:
            self.logger.error(f"Erro ao consultar CNES {cnes_id}: {e}")
            return None

    def obter_macrorregiao(self, ibge_code: str):
        """Busca a macrorregião e NRS baseada no código IBGE"""
        try:
            params = {"codigo_municipio": ibge_code, "limit": 1}
            response = self.session.get(
                f"{self.demas_base_url}/{self.suffix_url_macro}",
                params=params,
                timeout=self.timeout
            )
            if response.ok:
                dados = response.json().get("macrorregiao_regiao_saude_municipios", [])
                return dados[0] if dados else None
            return None
        except Exception as e:
            self.logger.error(f"Erro ao consultar Macrorregião para IBGE {ibge_code}: {e}")
            return None