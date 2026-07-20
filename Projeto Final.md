# Projeto Final SCTEC

####Contextualizando
Atualmente, a transparência pública permite a geração de grandes volumes de dados abertos. Um deles refere-se à base de Viagens a Serviço do Portal da Transparência do Governo Federal. Entretanto, estes dados são disponibilizados em sua forma bruta e, transformá-los em informação confiável é trabalho do Engenheiro de Dados, que, por sua vez, extrai, limpa, modela e analisa. Dominar um pipeline de dados (ETL) e a Arquitetura Medallion (camadas Raw, Silver e Gold) com Python e SQL é uma das competências mais valorizadas na área de dados atualmente, uma vez que permite uma utilização eficiente e segura. 

O desafio é construir, do zero, um pipeline de dados que baixe essas informações, preservando o histórico original, limpar a estrutura e transformar os dados brutos em métricas e gráficos claros.

#### Perguntas operacionais:

Os 5 órgãos com maior custo total? 

Os 3 destinos com maior custo médio por viagem? 

A viagem de maior duração e seu custo total? 

Qual o tipo de pagamento com maior valor médio? 

Qual o meio de transporte mais usado nos trechos?

Qual UF de destino aparece em mais trechos? 

Qual órgão pagou mais no total? 


#### Os 5 órgãos com o maior custo são:

MINISTÉRIO DA JUSTIÇA E SEGURANÇA PÚBLICA

MINISTÉRIO DA DEFESA

MINISTÉRIO DA EDUCAÇÃO

MINISTÉRIO DO MEIO AMBIENTE E MUDANÇA DO CLIM

MINISTÉRIO DA PREVIDÊNCIA SOCIAL


  <div>
    <img width="1389" height="890" alt="Image" src="https://github.com/user-attachments/assets/262760e7-6c6e-4aee-b6da-7371ebfc6f05" />
  </div>


#### Os 3 destinos com maior custo médio por viagem


|destinos	| custo_medio |
| :--- | :---: |
|ABU DABI/EMIRADOS ÁRABES, RIAD/ARÁBIA SAUDITA,... |	R$ 245.852,80|
|BRASÍLIA/DF, RIO BRANCO/AC, CRUZEIRO DO SUL/AC... |	R$ 216.729,36|
|BRASÍLIA/DF, RIO DE JANEIRO/RJ, ANGRA DOS REIS... |	R$ 207.220,14|


  
#### A viagem de maior duração e seu custo total?

|id_viagem |	nome_orgao_superior |	destinos |	duracao_dias |	valor_total
| :--- | :---: | :--- | :---: |:---: |
|0000000000020699856 |	MINISTÉRIO DA PREVIDÊNCIA SOCIAL |	MOGI MIRIM/SP |	383 |	R$ 0,00


  
#### Qual o tipo de pagamento com maior valor médio? 


 <div>
    <img width="989" height="690" alt="Image" src="https://github.com/user-attachments/assets/246d8592-5ace-4f50-96e9-d3a7bf8ba6dc" />
  </div>

#### Qual o meio de transporte mais usado nos trechos?


 <div>
    <img width="572" height="590" alt="Image" src="https://github.com/user-attachments/assets/03f408f8-1ae3-433b-aa94-be9a7f0f58f7" />
  </div>

  #### Qual UF de destino aparece em mais trechos? 


 <div>
    <img width="575" height="490" alt="Image" src="https://github.com/user-attachments/assets/26655f5d-69a6-49d5-8e31-3704c5703263" />
  </div>
  

   #### Qual órgão pagou mais no total?


 <div>
    <img width="775" height="490" alt="Image" src="https://github.com/user-attachments/assets/15bf04cf-25ac-41fd-8531-a962e7024870" />
  </div>
