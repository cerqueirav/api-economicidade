from app.jobs.calcular_economicidade_job import calcular_economicidade
from app.jobs.distancia_teleconsultoria_job import calcular_distancia_teleconsultoria

options = {
    "1": calcular_distancia_teleconsultoria,
    "2": calcular_economicidade
}