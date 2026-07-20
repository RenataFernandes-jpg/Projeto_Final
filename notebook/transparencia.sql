
SHOW VARIABLES LIKE 'secure_file_priv';

-- Faz nomes de mes e dia da semana sairem em portugues nas funcoes de data:
SET lc_time_names = 'pt_BR';


/* ----------------------------------------------------------------------------
   PASSO 1 - CRIAR O BANCO DE DADOS
   ---------------------------------------------------------------------------- */
DROP DATABASE IF EXISTS transparencia;
CREATE DATABASE transparencia
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE transparencia;


/* ============================================================================
   PASSO 2 - CAMADA RAW
   ----------------------------------------------------------------------------
   Recebe o dado exatamente como veio do CSV (data ainda como TEXTO).
   ============================================================================ */
   
DROP TABLE IF EXISTS raw_viagem;
CREATE TABLE raw_viagem (    
    identificador_do_processo_de_viagem     VARCHAR(20),
    numero_da_proposta_PCDP                 VARCHAR(20),
    situacao                                VARCHAR(50),
    viagem_urgente                          VARCHAR(5),
    justificativa_urgencia_viagem           VARCHAR(4000),
    codigo_do_orgao_superior                VARCHAR(20),
    nome_do_orgao_superior                  VARCHAR(255),
    codigo_orgao_solicitante                VARCHAR(20),
    nome_orgao_solicitante                  VARCHAR(255),
    cpf_viajante                            VARCHAR(20),
    nome                                    VARCHAR(255),
    cargo                                   VARCHAR(255),
    funcao                                  VARCHAR(255),
    descricao_funcao                        VARCHAR(255),
    periodo_data_de_inicio                  VARCHAR(50),
    periodo_data_de_fim                     VARCHAR(50),
    destinos                                VARCHAR(4000),
    motivo                                  VARCHAR(4000),
    valor_diarias                           VARCHAR(40),
    valor_passagens                         VARCHAR(40),
    valor_devolucao                         VARCHAR(40),
    valor_outros_gastos                     VARCHAR(40)    
)ENGINE=InnoDB;

DROP TABLE IF EXISTS raw_trecho;
CREATE TABLE raw_trecho (
    
    identificador_do_processo_de_viagem     VARCHAR(20),
    numero_da_Proposta_PCDP                 VARCHAR(20),
    sequencia_trecho                        VARCHAR(20),
    origem_data                       		VARCHAR(50),
    origem_pais                             VARCHAR(255),
    origem_UF                               VARCHAR(40),
    origem_cidade                           VARCHAR(80),
    destino_data              			    VARCHAR(50),
    destino_pais                            VARCHAR(80),
    destino_UF                              VARCHAR(40),
    destino_cidade                          VARCHAR(80),
    meio_de_transporte                      VARCHAR(50),
    Numero_diarias                          VARCHAR(100),
    missao                                  VARCHAR(255)   
)ENGINE=InnoDB;

DROP TABLE IF EXISTS raw_passagem;
CREATE TABLE raw_passagem (
    
    identificador_do_processo_de_viagem     VARCHAR(20),
    numero_da_proposta_PCDP                 VARCHAR(20),
    meio_de_transporte                      VARCHAR(50),
    pais_origem_ida                         VARCHAR(60),
    UF_origem_ida                           VARCHAR(40),
    cidade_origem_ida                       VARCHAR(80),
    pais_destino_ida                        VARCHAR(60),
    UF_destino_ida                          VARCHAR(40),
    cidade_destino_ida                      VARCHAR(80),
    pais_origem_volta                       VARCHAR(60),
    UF_origem_volta                         VARCHAR(40),
    cidade_origem_volta                     VARCHAR(80),
    pais_destino_volta                      VARCHAR(60),
    UF_destino_volta                        VARCHAR(40),
    cidade_destino_volta                    VARCHAR(80),
    valor_da_passagem                       VARCHAR(40),
    taxa_de_servico                         VARCHAR(40),
    data_da_emissao_compra                  VARCHAR(50),
    hora_da_emissão_compra                  VARCHAR(50)   
)ENGINE=InnoDB;

DROP TABLE IF EXISTS raw_pagamento;
CREATE TABLE raw_pagamento (
    
    identificador_do_processo_de_viagem     VARCHAR(20),
    numero_da_proposta_PCDP                 VARCHAR(20),
    codigo_do_orgao_superior                VARCHAR(20),
    nome_do_orgao_superior                  VARCHAR(255),
    codigo_do_orgao_pagador                 VARCHAR(20),
    nome_do_orgao_pagador                   VARCHAR(255),
    codigo_da_unidade_gestora_pagadora      VARCHAR(20),
    nome_da_unidade_gestora_pagadora        VARCHAR(255),
    tipo_de_pagamento                       VARCHAR(50),
    valor                                   VARCHAR(50)
)ENGINE=InnoDB;   


/* ============================================================================
     PASSO 3 - CAMADA SILVER
   ----------------------------------------------------------------------------
   A silver e o dado "confiavel": tipos corretos, data convertida para DATE
   de verdade, e novas colunas calculadas a partir da raw.
   ============================================================================ */

DROP TABLE IF EXISTS silver_viagem;
CREATE TABLE silver_viagem (
    
    id_viagem                               VARCHAR(20)     NOT NULL,
    num_proposta                            VARCHAR(20),
    situacao                                VARCHAR(50),
    viagem_urgente                          VARCHAR(5),
    justificativa_urgencia_viagem           VARCHAR(4000),
    cod_orgao_superior                      VARCHAR(20),
    nome_orgao_superior                     VARCHAR(255)    NOT NULL,
    codigo_orgao_solicitante                VARCHAR(20),
    nome_orgao_solicitante                  VARCHAR(255),
    cpf_viajante                            VARCHAR(20),
    nome_viajante                           VARCHAR(255),
    cargo                                   VARCHAR(255),
    funcao                                  VARCHAR(255),
    descricao_funcao                        VARCHAR(255),
    data_inicio                             DATE,
    data_fim                                DATE,
    destinos                                VARCHAR(4000),
    Motivo                                  VARCHAR(4000),
    valor_diarias                           DECIMAL(10,2),
    valor_passagens                         DECIMAL(10,2),
    valor_devolucao                         DECIMAL(10,2),
    valor_outros_gastos                     DECIMAL(10,2),  
    valor_total                             DECIMAL(10,2),
    duracao_dias                            INT,
    
    
    PRIMARY KEY (id_viagem),
    CONSTRAINT chk_valor_diarias CHECK (valor_diarias >= 0)
   
)ENGINE=InnoDB;

DROP TABLE IF EXISTS silver_trecho;
CREATE TABLE silver_trecho (
    
    id_trecho                               INT NOT NULL AUTO_INCREMENT,
    id_viagem                               VARCHAR(20) NOT NULL,
    num_Proposta                            VARCHAR(20),
    sequencia_trecho                        INT,
    origem_data                       		DATE,
    origem_pais                             VARCHAR(255),
    origem_UF                               VARCHAR(40),
    origem_cidade                           VARCHAR(80),
    destino_data              			    DATE,
    destino_pais                            VARCHAR(80),
    destino_UF                              VARCHAR(40),
    destino_cidade                          VARCHAR(80),
    meio_transporte                         VARCHAR(50),
    numero_diarias                          DECIMAL(10,2),
    missao                                  VARCHAR(255),
    
    PRIMARY KEY (id_trecho),
    FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem),
    CONSTRAINT chk_numero_diarias_ CHECK (numero_diarias >= 0)
    
)ENGINE=InnoDB;

DROP TABLE IF EXISTS silver_passagem;
CREATE TABLE silver_passagem (
    
    id_passagem                             INT NOT NULL AUTO_INCREMENT,
    id_viagem                               VARCHAR(20)     NOT NULL,
    num_proposta                            VARCHAR(20),
    meio_transporte                         VARCHAR(50),
    pais_origem_ida                         VARCHAR(60),
    UF_origem_ida                           VARCHAR(40),
    cidade_origem_ida                       VARCHAR(80),
    pais_destino_ida                        VARCHAR(60),
    UF_destino_ida                          VARCHAR(40),
    cidade_destino_ida                      VARCHAR(80),
    pais_origem_volta                       VARCHAR(60),
    UF_origem_volta                         VARCHAR(40),
    cidade_origem_volta                     VARCHAR(80),
    pais_destino_volta                      VARCHAR(60),
    UF_destino_volta                        VARCHAR(40),
    cidade_destino_volta                    VARCHAR(80),
    valor_passagem                          DECIMAL(10,2),
    taxa_servico                            DECIMAL(10,2),
    data_emissao                            DATE,
    hora_emissão                            TIME,
    
	PRIMARY KEY (id_passagem),
    FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem),
    CONSTRAINT chk_valor_passagem CHECK (valor_passagem >= 0),
    CONSTRAINT chk_taxa_servico CHECK (taxa_servico >= 0)

)ENGINE=InnoDB;

DROP TABLE IF EXISTS silver_pagamento;
CREATE TABLE silver_pagamento (
    
    id_pagamento                            INT NOT NULL AUTO_INCREMENT,
    id_viagem                               VARCHAR(20)     NOT NULL,
    num_proposta                            VARCHAR(20),
    cod_orgao_superior                      VARCHAR(20),
    nome_orgao_superior                     VARCHAR(255),
    codigo_orgao_pagador                    VARCHAR(20),
    nome_orgao_pagador                      VARCHAR(255),
    codigo_da_unidade_gestora_pagadora      VARCHAR(20),
    nome_ug_pagadora                        VARCHAR(255),
    tipo_de_pagamento                       VARCHAR(50)     NOT NULL,
    valor                                   DECIMAL(10,2),
    
	PRIMARY KEY (id_pagamento),
    FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem),
    CONSTRAINT chk_valor CHECK (valor >= 0)

)ENGINE=InnoDB;
  
 /* ============================================================================
   PASSO 4 - CAMADAS GOLD
   ----------------------------------------------------------------------------
   Cada tabela gold responde a UMA pergunta de negocio.

*/ 

/* Pergunta 1 - Os 5 órgãos com maior custo total?*/
 
 DROP TABLE IF EXISTS golden_maior_custo;
 create table golden_maior_custo as
 select
     nome_orgao_superior,
     ROUND(sum(valor_total), 2) as valor_total
 from silver_viagem
 group by nome_orgao_superior
 order by valor_total desc;
 

/* Pergunta 2 - Os 3 destinos com maior custo médio por viagem?*/

DROP TABLE IF EXISTS golden_custo_destino;
create TABLE golden_custo_destino as
 select
     destinos, 
     ROUND(avg(valor_total), 2) as custo_medio
 from silver_viagem
 group by destinos
 order by custo_medio desc;

/* Pergunta 3 - A viagem de maior duração e seu custo total?*/

DROP TABLE IF EXISTS golden_duracao_custo;
create TABLE golden_duracao_custo as
 select
     id_viagem,
     nome_orgao_superior,
     destinos,
     duracao_dias,
     round(valor_total, 2) as valor_total    
 from silver_viagem
 order by duracao_dias desc;
 
/* Pergunta 4 - Qual o tipo de pagamento com maior valor médio?*/

DROP TABLE IF EXISTS golden_pagamento_medio;
create TABLE golden_pagamento_medio as
 select
     tipo_de_pagamento,
     round(avg(valor), 2) as valor_medio    
 from silver_pagamento
 group by tipo_de_pagamento
 order by valor_medio desc;
 
/* Pergunta 5 - Qual o meio de transporte mais usado nos trechos?*/

DROP TABLE IF EXISTS golden_transporte_trechos;
create TABLE golden_transporte_trechos as
 select
     meio_transporte,
     count(*) as qtd_trechos    
 from silver_trecho
 group by meio_transporte
 order by qtd_trechos desc;
 
/* Pergunta 6 - Qual UF de destino aparece em mais trechos?*/

DROP VIEW IF EXISTS golden_UF_trechos;
create VIEW golden_UF_trechos as
 select
     destino_UF,
     count(*) as qtd_trechos    
 from silver_trecho
 group by destino_UF
 order by qtd_trechos desc;

/* Pergunta 7 - Qual órgão pagou mais no total?*/

 DROP VIEW IF EXISTS golden_orgao_custo;
 create view golden_orgao_custo as
 select
     nome_orgao_superior,
     sum(valor_total) as total_pago
 from silver_viagem
 group by nome_orgao_superior
 order by Percentual desc;

