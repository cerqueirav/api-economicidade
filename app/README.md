# API STT x Moodle

Este projeto automatiza a consulta de profissionais no sistema STT, extraindo vínculos e enriquecendo os dados com informações geográficas do Ministério da Saúde.

## Clone o repositório ou navegue até a pasta do projeto
```
cd api-stt
```

## Crie um ambiente virtual (recomendado)
```
python -m venv .venv
```

## Ative o ambiente virtual
### No Windows:
```
.venv\Scripts\activate
```
### No Linux/Mac:
```
source .venv/bin/activate
```

## Instalação de Dependências
```
pip install -r requirements.txt
```

## Configuração

Verifique o arquivo config.yaml na raiz do projeto. Certifique-se de que as credenciais do STT e os caminhos dos arquivos estão corretos:

```
YAML
auth:
  usuario: "seu_usuario"
  senha: "sua_senha"

arquivos:
  entrada: "resources/dados.xlsx"
  saida: "resources/resultado.xlsx"
```

## Execução padrão (sem parâmetros)

Processa todos os cursos disponíveis no Moodle:
```
python -m app.main
```

## Execução com cursos específicos

Você pode informar um ou mais cursos diretamente na execução:

### Um único curso
```
python -m app.main ID_CURSO
```
### Múltiplos cursos (separados por vírgula)
```
python -m app.main ID_CURSO_1,ID_CURSO_2...,ID_CURSO_N
```