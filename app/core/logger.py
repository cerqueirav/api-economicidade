import logging
import os
from datetime import datetime

def configurar_logger():
    if logging.getLogger().hasHandlers():
        return logging.getLogger()

    os.makedirs("logs", exist_ok=True)
    log_filename = f"logs/execucao_{datetime.now().strftime('%Y%m%d')}.log"

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return root_logger