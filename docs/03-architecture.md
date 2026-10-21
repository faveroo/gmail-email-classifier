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
