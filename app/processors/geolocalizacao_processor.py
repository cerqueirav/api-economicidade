from duckdb import df
import pandas as pd
import logging
import json
import os
import time
from app.core.config import settings
from app.services.demas_service import DemasService
from app.utils.geo_utils import normalizar_coord

class GeolocalizacaoProcessor:
    def __init__(self, session):
        self.logger = logging.getLogger(__name__)
        self.input_file = "input/dataset-teleconsultorias.xlsx"      
        self.cache_path = "cache/unidades_cnes.json"     
        self.timeout = settings.timeout
        self.delay = settings.delay
        self.retries = settings.proc_params.get('retries', 3)
        
        self.demas_service = DemasService(session)
        self.cache = self._carregar_cache()

    def _carregar_cache(self):
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"unidades": {}}

    def _salvar_cache(self):
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=4, ensure_ascii=False)

    def obter_coordenadas_cnes(self, i, total, cod_cnes):
        if not cod_cnes or pd.isna(cod_cnes):
            return None, None

        cod_cnes = str(int(float(cod_cnes))).zfill(7)
        
        # 1. Tenta Cache
        unidade = self.cache["unidades"].get(cod_cnes)
        if unidade and unidade.get("latitude") and unidade.get("longitude"):
            if i % 100 == 0:
                self.logger.info(f"[{i}/{total}] CNES {cod_cnes}: OK (Cache)")
            return unidade["latitude"], unidade["longitude"]

        # 2. Tenta API do DEMAS
        self.logger.info(f"[{i}/{total}] CNES {cod_cnes}: Consultando API... (Aguardando {self.delay}s)")
        time.sleep(self.delay) 

        for tentativa in range(self.retries):
            try:
                dados_u = self.demas_service.obter_dados_unidade(cod_cnes)
                if dados_u:
                    lat = normalizar_coord(dados_u.get("latitude_estabelecimento_decimo_grau"))
                    lon = normalizar_coord(dados_u.get("longitude_estabelecimento_decimo_grau"))
                    
                    if lat and lon:
                        self.cache["unidades"][cod_cnes] = {
                            "latitude": lat,
                            "longitude": lon,
                            "ibge": str(dados_u.get("codigo_municipio", "")),
                            "tipo_unidade": dados_u.get("codigo_tipo_unidade", "")
                        }
                        self._salvar_cache()
                        return lat, lon
                break
            except Exception as e:
                self.logger.error(f"Tentativa {tentativa+1} falhou para CNES {cod_cnes}: {e}")
                time.sleep(self.delay * 2)

        self.cache["unidades"][cod_cnes] = {"latitude": None, "longitude": None}
        return None, None

    def run(self):
        self.logger.info(f"Processando planilha. Timeout: {self.timeout}s | Delay: {self.delay}s")
        
        df = pd.read_excel(self.input_file)

        col_sol = 'CNES_SOLICITANTE'
        col_ser = 'CNES_SERVICO'

        todos_cnes = sorted(list(set(df[col_sol].dropna().unique().tolist() + 
                                     df[col_ser].dropna().unique().tolist())))
        
        total_unicos = len(todos_cnes)
        mapa_coords = {}

        mapa_ibge = {
            cnes: data.get("ibge")
            for cnes, data in self.cache["unidades"].items()
        }

        df['IBGE_SOLICITANTE'] = df[col_sol].map(
            lambda x: mapa_ibge.get(normalizar_cnes(x))
        )

        for i, cnes in enumerate(todos_cnes, 1):
            lat, lon = self.obter_coordenadas_cnes(i, total_unicos, cnes)
            mapa_coords[cnes] = {'lat': lat, 'lon': lon}

        self.logger.info("Mapeando coordenadas de volta para as 80k linhas...")
        
        df['LAT_SOLICITANTE'] = df[col_sol].map(lambda x: mapa_coords.get(x, {}).get('lat'))
        df['LON_SOLICITANTE'] = df[col_sol].map(lambda x: mapa_coords.get(x, {}).get('lon'))
        df['LAT_SERVICO'] = df[col_ser].map(lambda x: mapa_coords.get(x, {}).get('lat'))
        df['LON_SERVICO'] = df[col_ser].map(lambda x: mapa_coords.get(x, {}).get('lon'))
        df['ORIGEM_SALVADOR'] = (df['IBGE_SOLICITANTE'] == "292740")
        df['DT_RESPOSTA'] = pd.to_datetime(df['DT_RESPOSTA'], dayfirst=True, errors='coerce').dt.strftime('%d/%m/%Y')
        df['CNES_SOLICITANTE'] = df['CNES_SOLICITANTE'].map(normalizar_cnes)
        df['CNES_SERVICO'] = df['CNES_SERVICO'].map(normalizar_cnes)

        timestamp = time.strftime("%Y%m%d-%H%M")
        output_path = os.path.join("output", f"teleconsultorias_coords_{timestamp}.xlsx")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        df.to_excel(output_path, index=False)
        self.logger.info(f"Arquivo final gerado: {output_path}")
        
        return df