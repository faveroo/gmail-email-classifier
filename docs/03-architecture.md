# Arquitetura Conceitual

## Fluxo previsto

```text
Gmail
  |
  v
Leitura e normalização
  |
  v
Pré-processamento
  |
  +--------------------+
  |                    |
  v                    v
Modelo de Spam     Modelo de Categoria
  |                    |
  +----------+---------+
             |
             v
       Política de decisão
             |
      +------+------+
      |             |
      v             v
Aplicar label    IA/Revisar
```

## Componentes futuros

### Gmail Adapter

Responsável exclusivamente pela comunicação com Gmail.

### Preprocessor

Responsável por transformar uma mensagem em uma representação textual consistente.

### Spam Classifier

Modelo binário independente.

### Category Classifier

Modelo multiclasse aplicado a mensagens consideradas legítimas.

### Decision Policy

Converte previsões e níveis de confiança em ações permitidas.

### Training Pipeline

Responsável pelo treinamento, avaliação e persistência dos modelos.

## Separação importante

O código de integração com Gmail não deverá conhecer detalhes internos do algoritmo de treinamento. Da mesma forma, o modelo não deverá depender diretamente da Gmail API.

## Implementação local

Na inferência, spam é avaliado primeiro; apenas probabilidade <= 0.20 habilita o
modelo de categoria. O intervalo incerto vai diretamente para revisão, e >= 0.90
sugere IA/SPAM. O vocabulário totalmente desconhecido também exige revisão.
A saída é sugestão local; o adaptador Gmail/OAuth opcional permite exclusivamente leitura.
Treinamento e avaliação ficam separados da política e do loader de dados.

`gmail.py` cuida de OAuth, paginação e extração de texto, sem importar ML.
`review.py` valida revisão humana e prepara arquivos; a simulação offline carrega
um modelo já treinado, sem conectar ao Gmail. `private_storage.py` bloqueia caminhos
privados dentro do checkout e de árvores Git. Coleta, revisão, treino e inferência
são comandos separados; o dataset nunca depende da caixa de produção durante o fit.
