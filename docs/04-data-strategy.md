# Estratégia de Dados

## Objetivo

Criar um dataset supervisionado confiável sem expor desnecessariamente informações privadas.

## Unidade de classificação

Cada registro deverá representar uma mensagem de e-mail.

Campos candidatos:

- identificador interno anonimizado;
- remetente ou domínio, quando apropriado;
- assunto;
- corpo textual normalizado;
- label de spam;
- categoria;
- data de coleta opcional;
- origem da rotulagem;
- indicador de revisão humana.

## Dados que não devem ser versionados

- tokens OAuth;
- senhas;
- cookies;
- mensagens reais contendo informações sensíveis;
- anexos privados;
- endereços pessoais desnecessários;
- datasets brutos exportados de caixas reais.

## Estratégias de obtenção

1. dataset público de spam para baseline;
2. mensagens sintéticas para testes de pipeline;
3. amostras reais rotuladas localmente e mantidas fora do Git;
4. aproveitamento de labels existentes do Gmail, após definição de critérios.

## Split

O dataset deverá ser separado em treino, validação e teste, evitando vazamento de exemplos muito semelhantes entre os conjuntos.

## Risco de vazamento

Threads, mensagens duplicadas e templates podem produzir métricas artificialmente altas se versões quase idênticas aparecerem simultaneamente em treino e teste.
