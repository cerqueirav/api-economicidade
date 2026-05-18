import yaml
from pathlib import Path

class Config:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent.parent
        self.config_file = self.root_dir / "config.yaml"
        
        with open(self.config_file, "r", encoding="utf-8") as file:
            self._data = yaml.safe_load(file)

    @property
    def urls(self):
        return self._data["api"]

    @property
    def paths(self):
        return self._data["arquivos"]

    @property
    def proc_params(self):
        return self._data["processamento"]

    @property
    def delay(self):
        return self._data["processamento"]["delay"]
    
    @property
    def timeout(self):
        return self._data["processamento"]["timeout"]
    
    @property
    def operacao_padrao(self):
        """Busca a operação padrão na raiz do config.yaml"""
        return self._data.get("operacao_padrao", "")
    
    def get(self, key, default=None):
        """Permite acessar configurações como se fosse um dicionário: settings.get('chave')"""
        return self._data.get(key, default)

settings = Config()