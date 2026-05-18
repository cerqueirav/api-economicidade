from app.processors.calcular_economicidade_processor import CalcularEconomicidadeProcessor

def calcular_economicidade(session, parametro=None):
    calcular_economicidade_processor = CalcularEconomicidadeProcessor(session)
    calcular_economicidade_processor.run(parametro)