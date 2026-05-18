from app.processors.calcular_distancia_processor import CalcularDistanciaProcessor
from app.processors.geolocalizacao_processor import GeolocalizacaoProcessor

def calcular_distancia_teleconsultoria(session, parametro=None):
    geolocalizacao_processor = GeolocalizacaoProcessor(session)
    geolocalizacao_processor.run()

    calcular_distancia_processor = CalcularDistanciaProcessor(session)
    calcular_distancia_processor.run()