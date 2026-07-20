"""
config.py
---------
Centraliza TODAS as configuracoes do pipeline:
  - leitura das credenciais do MySQL (a partir do arquivo .env)
  - parametros do que vamos baixar/processar (ID do arquivo no Drive)
  - nomes dos arquivos e das tabelas

"""

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Caminhos do projeto
# ---------------------------------------------------------------------------

PASTA_RAIZ = Path(__file__).resolve().parent
PASTA_DADOS = PASTA_RAIZ / "data"   # onde o .zip e os .csv ficam (ignorada pelo Git)


# ---------------------------------------------------------------------------
# Leitura simples do arquivo .env (sem biblioteca externa)
# ---------------------------------------------------------------------------
def carregar_env():
    """Le o arquivo .env (se existir) e joga as variaveis para os.environ."""
    arquivo_env = PASTA_RAIZ / ".env"
    if not arquivo_env.exists():
        return
    for linha in arquivo_env.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        # ignora linhas vazias e comentarios
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        os.environ.setdefault(chave.strip(), valor.strip())


carregar_env()


# ---------------------------------------------------------------------------
# Credenciais do MySQL (vem do .env)
# ---------------------------------------------------------------------------
MYSQL_CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "port": int(os.environ.get("MYSQL_PORT", "3306")),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "database": os.environ.get("MYSQL_DATABASE", "transparencia"),
}


# ---------------------------------------------------------------------------
# Onde fica o arquivo de dados
# ---------------------------------------------------------------------------
# O arquivo "cafeteria.zip" e disponibilizado pelo(a) professor(a) no Google
# Drive. Baixe-o e coloque-o dentro da pasta "data/" deste projeto:
#     treino_cafeteria_aluno/data/cafeteria.zip
# O 1_extrair.py le esse arquivo direto da sua maquina (sem baixar nada).

# Tamanho do bloco de leitura/insercao (numero de linhas por vez).
# Ler tudo de uma vez poderia estourar a memoria em bases grandes; por isso
# lemos em "pedacos" (aqui a base e pequena, mas mantemos o bom habito).
TAMANHO_BLOCO = 50_000


# ---------------------------------------------------------------------------
# Mapeamento: cada arquivo CSV dentro do .zip -> tabela RAW correspondente
# ---------------------------------------------------------------------------
ARQUIVOS = {
    "2025_Viagem": {"csv": "2025_Viagem.csv", "tabela_raw": "raw_viagem"},
    "2025_Trecho":  {"csv": "2025_Trecho.csv",  "tabela_raw": "raw_trecho"},
    "2025_Passagem":  {"csv": "2025_Passagem.csv",  "tabela_raw": "raw_passagem"},
    "2025_Pagamento":  {"csv": "2025_Pagamento.csv",  "tabela_raw": "raw_pagamento"},
}

# Caracteristicas dos arquivos CSV (iguais aos do Portal da Transparencia):
CSV_SEPARADOR = ";"
CSV_ENCODING = "latin-1"   # acentuacao no padrao ISO-8859-1
