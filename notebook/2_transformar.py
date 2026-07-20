"""
2_transformar.py  -  FASE 2: Transformacao e Camada SILVER
----------------------------------------------------------
Pega os dados "sujos" da camada RAW (tudo texto) e preenche as tabelas SILVER
(ja criadas, com PK/FK, pelo 0_criar_banco.txt) com os dados limpos e tipados.

A receita e simples: rodamos alguns comandos SQL, em ordem.
  1. Esvaziamos as tabelas SILVER (para nao duplicar se rodar de novo).
  2. Copiamos da RAW para a SILVER, convertendo os tipos.
  3. Calculamos as colunas derivadas (valor_total, prazo_dias, subtotal).

------------------------------------------------------------------------------
COMO CONVERTEMOS O TEXTO DA CAMADA RAW (esse padrao se repete no SQL abaixo):

  - Dinheiro: "1.234,50" (texto)  ->  1234.50 (numero DECIMAL)
      tira o ponto de milhar, troca a virgula por ponto e faz CAST:
      CAST(REPLACE(REPLACE(NULLIF(TRIM(coluna), ''), '.', ''), ',', '.') AS DECIMAL(10,2))

  - Data: "30/06/2025" (texto)  ->  2025-06-30 (tipo DATE)
      STR_TO_DATE(NULLIF(TRIM(coluna), ''), '%d/%m/%Y')

  Obs.: NULLIF(coluna, '') transforma um campo vazio em NULL (vazio no banco).
------------------------------------------------------------------------------
"""

import banco


# 1) Esvaziar as tabelas SILVER (idempotencia).
#    A ordem importa por causa da FK: apagamos a filha (itens) antes da principal.
LIMPAR_SILVER = [
    "DELETE FROM silver_pagamento",
    "DELETE FROM silver_passagem",
    "DELETE FROM silver_trecho",
    "DELETE FROM silver_viagem",
]


# 2) Copiar RAW -> SILVER convertendo os tipos.
#    (silver_vendas e a tabela principal; carregamos ela primeiro.)
SQL_VIAGEM = """
INSERT INTO silver_viagem (

    id_viagem, num_proposta, situacao, viagem_urgente, justificativa_urgencia_viagem, cod_orgao_superior, nome_orgao_superior, 
    codigo_orgao_solicitante, nome_orgao_solicitante, cpf_viajante, nome_viajante, cargo, funcao, descricao_funcao, data_inicio, 
    data_fim, destinos, motivo, valor_diarias, valor_passagens, valor_devolucao, valor_outros_gastos
)
SELECT
    identificador_do_processo_de_viagem, numero_da_proposta_PCDP, situacao, viagem_urgente, justificativa_urgencia_viagem, 
    codigo_do_orgao_superior, 
    UPPER(TRIM(nome_do_orgao_superior)) AS nome_orgao_superior, 
    codigo_orgao_solicitante, nome_orgao_solicitante, 
    REPLACE(REPLACE(NULLIF(TRIM(cpf_viajante), ''), '.', ''), ',', '') AS cpf_viajante,
    nome, cargo, funcao, descricao_funcao,
    STR_TO_DATE(NULLIF(TRIM(periodo_data_de_inicio),  ''), '%d/%m/%Y'),
    STR_TO_DATE(NULLIF(TRIM(periodo_data_de_fim ),     ''), '%d/%m/%Y'), 
    UPPER(TRIM(destinos)) AS destinos,
    Motivo, 
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_diarias),    ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_passagens), ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_devolucao),    ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_outros_gastos), ''), '.', ''), ',', '.') AS DECIMAL(10,2))

FROM raw_viagem;
"""

SQL_TRECHO = """
INSERT INTO silver_trecho (
    id_viagem, num_Proposta, sequencia_trecho, origem_data, origem_pais, origem_UF, origem_cidade, destino_data, 
    destino_pais, destino_UF, destino_cidade, meio_transporte, numero_diarias, missao
)
SELECT
    identificador_do_processo_de_viagem, numero_da_Proposta_PCDP, sequencia_trecho, 
    STR_TO_DATE(NULLIF(TRIM(origem_data),  ''), '%d/%m/%Y'), 
    origem_pais, origem_UF, origem_cidade,
    STR_TO_DATE(NULLIF(TRIM(destino_data),  ''), '%d/%m/%Y'), 
    destino_pais, 
    UPPER(TRIM(destino_UF)), 
    destino_cidade, 
    UPPER(TRIM(meio_de_transporte)) AS meio_de_transporte, 
    CAST(REPLACE(REPLACE(NULLIF(TRIM(numero_diarias),    ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    missao
    
FROM raw_trecho;
"""

SQL_PASSAGEM = """
INSERT INTO silver_passagem (
    id_viagem, num_proposta, meio_transporte, pais_origem_ida, UF_origem_ida, cidade_origem_ida, pais_destino_ida, 
    UF_destino_ida, cidade_destino_ida, pais_origem_volta, UF_origem_volta, cidade_origem_volta, pais_destino_volta, 
    UF_destino_volta, cidade_destino_volta, valor_passagem, taxa_servico, data_emissao, hora_emissão
       
)
SELECT

    identificador_do_processo_de_viagem, numero_da_proposta_PCDP, 
    UPPER(TRIM(meio_de_transporte)) AS meio_de_transporte, 
    pais_origem_ida, UF_origem_ida, cidade_origem_ida, pais_destino_ida, UF_destino_ida, cidade_destino_ida, pais_origem_volta, 
    UF_origem_volta, cidade_origem_volta, pais_destino_volta, UF_destino_volta, cidade_destino_volta, 
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_da_passagem),    ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(taxa_de_servico),    ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    STR_TO_DATE(NULLIF(TRIM(data_da_emissao_compra),  ''), '%d/%m/%Y'),
    STR_TO_DATE(NULLIF(TRIM(hora_da_emissão_compra),  ''), '%H:%i')
    
FROM raw_passagem;
"""

SQL_PAGAMENTO = """
INSERT INTO silver_pagamento (

    id_viagem, num_proposta, cod_orgao_superior, nome_orgao_superior, codigo_orgao_pagador, nome_orgao_pagador, 
    codigo_da_unidade_gestora_pagadora, nome_ug_pagadora, tipo_de_pagamento, valor
      
)
SELECT

    identificador_do_processo_de_viagem, numero_da_proposta_PCDP, codigo_do_orgao_superior, nome_do_orgao_superior, codigo_do_orgao_pagador, nome_do_orgao_pagador, 
    codigo_da_unidade_gestora_pagadora, nome_da_unidade_gestora_pagadora, 
    UPPER(TRIM(tipo_de_pagamento)) AS tipo_de_pagamento, 
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor),    ''), '.', ''), ',', '.') AS DECIMAL(10,2))

    
FROM raw_pagamento;
"""

# 3) Calcular as colunas derivadas.
#    Agora que os valores ja sao numeros e as datas ja sao DATE, a conta fica facil.
#    COALESCE(coluna, 0) usa 0 quando o valor for NULL (vazio), para nao quebrar a soma.
SQL_CALC_VIAGEM = """
UPDATE silver_viagem
SET duracao_dias  = DATEDIFF(data_fim, data_inicio),
    valor_total = COALESCE(valor_diarias, 0) + COALESCE(valor_passagens, 0) + COALESCE(valor_devolucao, 0) + COALESCE(valor_outros_gastos, 0)
"""


def main():
    print("=== FASE 2: TRANSFORMACAO + CAMADA SILVER ===")
    try:
        conexao = banco.conectar()

        print("[1/3] Esvaziando as tabelas SILVER...")
        for comando in LIMPAR_SILVER:
            banco.executar(conexao, comando)

        print("[2/3] Copiando e convertendo RAW -> SILVER...")
        banco.executar(conexao, SQL_VIAGEM)
        print("      silver_viagem  OK")
        banco.executar(conexao, SQL_TRECHO)
        print("      silver_trecho  OK")
        banco.executar(conexao, SQL_PASSAGEM)
        print("      silver_passagem  OK")
        banco.executar(conexao, SQL_PAGAMENTO)
        print("      silver_pagamento  OK")

        print("[3/3] Calculando valor_total e duracao_dias ...")
        banco.executar(conexao, SQL_CALC_VIAGEM)

        conexao.close()
        print("=== Camada SILVER concluida com sucesso! ===")
    except Exception as erro:
        print("[ERRO] Algo deu errado:", erro)
        raise


if __name__ == "__main__":
    main()
