import logging
import pandas as pd
import json
import os

from app.services.osrm_service import (
    OSRMService
)

class CalcularDistanciaProcessor:
    def __init__(self, session):
        self.logger = logging.getLogger(
            __name__
        )

        self.cache_path = (
            "cache/distancia_osrm.json"
        )

        self.cache = (
            self._carregar_cache()
        )

    def _carregar_cache(self):
        if os.path.exists(
            self.cache_path
        ):
            with open(
                self.cache_path,
                "r",
                encoding="utf-8"
            ) as f:
                return json.load(f)

        return {}

    def _salvar_cache(self):
        os.makedirs(
            os.path.dirname(
                self.cache_path
            ),
            exist_ok=True
        )

        with open(
            self.cache_path,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                self.cache,
                f,
                indent=4,
                ensure_ascii=False
            )

    def _pegar_arquivo_geolocalizado(
        self
    ):
        folder = "output"

        arquivos = [
            f
            for f in os.listdir(
                folder
            )
            if f.startswith(
                "teleconsultorias_coords"
            )
        ]

        if not arquivos:
            raise FileNotFoundError(
                "Nenhum arquivo "
                "de coordenadas "
                "encontrado."
            )

        arquivos.sort(
            reverse=True
        )

        return os.path.join(
            folder,
            arquivos[0]
        )

    def run(self):
        self.logger.info(
            "Iniciando cálculo "
            "OSRM..."
        )

        input_file = (
            self
            ._pegar_arquivo_geolocalizado()
        )

        df = pd.read_excel(
            input_file
        )

        osrm = OSRMService()

        df[
            "DISTANCIA_KM_OSRM"
        ] = None

        df[
            "TEMPO_MINUTOS_OSRM"
        ] = None

        df[
            "TEMPO_HORAS_OSRM"
        ] = None

        total = len(df)

        for i, row in (
            df.iterrows()
        ):
            self.logger.info(
                f"Processando "
                f"{i + 1}/{total} "
                f"- "
                f"{row['CNES_SOLICITANTE']}"
                f" -> "
                f"{row['CNES_SERVICO']}"
            )

            try:
                if (
                    pd.isna(
                        row[
                            "LAT_SOLICITANTE"
                        ]
                    )
                    or pd.isna(
                        row[
                            "LON_SOLICITANTE"
                        ]
                    )
                    or pd.isna(
                        row[
                            "LAT_SERVICO"
                        ]
                    )
                    or pd.isna(
                        row[
                            "LON_SERVICO"
                        ]
                    )
                ):
                    self.logger.warning(
                        f"[{i}] "
                        f"Coordenadas "
                        f"incompletas"
                    )

                    continue

                chave = (
                    f"{row['CNES_SOLICITANTE']}"
                    f"-"
                    f"{row['CNES_SERVICO']}"
                )

                resultado = (
                    self.cache.get(
                        chave
                    )
                )

                # usa cache
                if resultado:
                    self.logger.info(
                        f"[CACHE] "
                        f"{chave} = "
                        f"{resultado.get('distancia_km')} km | "
                        f"{resultado.get('tempo_minutos')} min"
                    )

                # consulta OSRM
                else:
                    resultado = (
                        osrm
                        .calculate_osrm(
                            row[
                                "LAT_SOLICITANTE"
                            ],
                            row[
                                "LON_SOLICITANTE"
                            ],
                            row[
                                "LAT_SERVICO"
                            ],
                            row[
                                "LON_SERVICO"
                            ]
                        )
                    )

                    if resultado:
                        self.cache[
                            chave
                        ] = resultado

                        self.logger.info(
                            f"[OSRM] "
                            f"{chave} = "
                            f"{resultado['distancia_km']} km | "
                            f"{resultado['tempo_minutos']} min"
                        )

                if resultado:
                    df.at[
                        i,
                        "DISTANCIA_KM_OSRM"
                    ] = resultado.get(
                        "distancia_km"
                    )

                    df.at[
                        i,
                        "TEMPO_MINUTOS_OSRM"
                    ] = resultado.get(
                        "tempo_minutos"
                    )

                    df.at[
                        i,
                        "TEMPO_HORAS_OSRM"
                    ] = resultado.get(
                        "tempo_horas"
                    )

                # salva cache
                if i % 100 == 0:
                    self._salvar_cache()

            except Exception as e:
                self.logger.error(
                    f"[{i}] erro "
                    f"ao calcular "
                    f"OSRM: {e}"
                )

        self._salvar_cache()

        output_path = (
            os.path.join(
                "output",
                "teleconsultorias_distancia_"
                f"{pd.Timestamp.now().strftime('%Y%m%d-%H%M')}"
                ".xlsx"
            )
        )

        df.to_excel(
            output_path,
            index=False
        )

        self.logger.info(
            f"Arquivo final "
            f"gerado: "
            f"{output_path}"
        )

        return df