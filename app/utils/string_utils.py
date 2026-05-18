import re


import re
import unicodedata

def normalizar_ids(value):
    if not value:
        return []

    if isinstance(value, str):
        return [x.strip() for x in value.split(",") if x.strip()]

    return list(value)

def normalizar_ibge(serie):
    return (serie.astype(str)
                 .str.replace(r'\.0$', '', regex=True)
                 .str.strip()
                 .str.zfill(6)
                 .str.slice(stop=6))

def sanitizar_nome_arquivo(nome):
    # 1. Remove acentos
    nome = "".join(
        c for c in unicodedata.normalize('NFD', nome)
        if unicodedata.category(c) != 'Mn'
    )
    
    # 2. Tudo minúsculo
    nome = nome.lower()
    
    # 3. Mantém apenas letras, números, espaços e hífens
    nome = re.sub(r'[^a-z0-9\s-]', '', nome)
    
    # 4. Transforma espaços em hífens e evita hífens duplos
    nome = re.sub(r'\s+', '-', nome)
    nome = re.sub(r'-+', '-', nome)
    
    return nome.strip("-")