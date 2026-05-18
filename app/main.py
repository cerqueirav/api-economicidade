from datetime import datetime
import sys
from app.core import operations
from app.utils.http_utils import criar_session
from app.core.logger import configurar_logger

configurar_logger()
logger = configurar_logger()

def main():
    arg1 = sys.argv[1] if len(sys.argv) > 1 else None
    arg2 = sys.argv[2] if len(sys.argv) > 2 else None

    if arg1 and arg1.upper() in operations.options:
        operacao_ativa = arg1.upper()
        parametro = arg2
    else:
        operacao_ativa = "2" 
        parametro = arg1

    logger.info(f"Iniciando | Operação: {operacao_ativa} | Parâmetro: {parametro or 'TODOS'}")
    
    with criar_session() as session:
        try:
            job = operations.options.get(operacao_ativa)
            if job:
                job(session, parametro)
                logger.info(f"{operacao_ativa} finalizado com sucesso.")
            else:
                logger.error(f"Operação '{operacao_ativa}' não mapeada.")
        except Exception as e:
            logger.error(f"Erro crítico durante {operacao_ativa}: {e}", exc_info=True)

if __name__ == "__main__":
    main()