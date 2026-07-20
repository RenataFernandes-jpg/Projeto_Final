"""
1_extrair.py  -  FASE 1: Extracao e Camada RAW
----------------------------------------------
Passo a passo simples:
  1. Localiza o arquivo cafeteria.zip que foi baixado para a pasta data/.
  2. Le os 2 CSVs de dentro do .zip (vendas, itens).
  3. Insere os dados, SEM nenhuma alteracao, nas 2 tabelas RAW do MySQL.

A camada RAW e uma copia fiel do CSV: todas as colunas sao texto (VARCHAR).

"""

import zipfile

import pandas as pd

import config
import banco


# ---------------------------------------------------------------------------
# Passo 1 - Localizar o arquivo .zip na pasta data/
# ---------------------------------------------------------------------------
def localizar_zip():
    """Aponta para o viagens_2025_6meses.zip que voce colocou na pasta data/."""
    caminho = config.PASTA_DADOS / "viagens_2025_6meses.zip"
    if not caminho.exists():
        raise FileNotFoundError(
            "Arquivo nao encontrado: baixe o 'viagens_2025_6meses.zip' do Drive e "
            f"coloque-o na pasta '{config.PASTA_DADOS}' antes de rodar este script."
        )
    print("[1/3] Usando o arquivo local:", caminho.name)
    return caminho


# ---------------------------------------------------------------------------
# Passo 2 - Carregar um CSV dentro da sua tabela RAW
# ---------------------------------------------------------------------------
def carregar_csv(conexao, zip_aberto, nome_csv, tabela):
    """Le um CSV de dentro do zip e insere todas as linhas na tabela do MySQL.

    """
    print("      Carregando", tabela, "...")

    # esvazia a tabela antes de carregar (assim, rodar de novo nao duplica dados)
    banco.executar(conexao, f"TRUNCATE TABLE {tabela}")

    total = 0
    with zip_aberto.open(nome_csv) as arquivo:
        # le o CSV em pedacos, para nao encher a memoria do PC em bases grandes
        pedacos = pd.read_csv(
            arquivo,
            sep=config.CSV_SEPARADOR,    # colunas separadas por ponto-e-virgula
            encoding=config.CSV_ENCODING,  # acentuacao em latin-1
            dtype=str,                   # tudo como texto (camada RAW)
            keep_default_na=False,       # campo vazio continua "" (nao vira "NaN")
            chunksize=config.TAMANHO_BLOCO,
        )
        for pedaco in pedacos:
            linhas = pedaco.values.tolist()
            # um "%s" para cada coluna do CSV
            marcadores = ", ".join(["%s"] * len(pedaco.columns))
            comando = f"INSERT INTO {tabela} VALUES ({marcadores})"
            banco.inserir_em_lote(conexao, comando, linhas)
            total += len(linhas)

    print("      ->", total, "linhas em", tabela)


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
def main():
    print("=== FASE 1: EXTRACAO + CAMADA RAW ===")
    try:
        conexao = banco.conectar()

        caminho_zip = localizar_zip()
        print("[2/3] Abrindo o arquivo zip...")
        print("[3/3] Carregando as tabelas RAW...")
        with zipfile.ZipFile(caminho_zip) as zip_aberto:
            for arquivo in config.ARQUIVOS.values():
                carregar_csv(conexao, zip_aberto, arquivo["csv"], arquivo["tabela_raw"])

        conexao.close()
        print("=== Camada RAW concluida com sucesso! ===")
    except Exception as erro:
        print("[ERRO] Algo deu errado:", erro)
        raise


if __name__ == "__main__":
    main()
