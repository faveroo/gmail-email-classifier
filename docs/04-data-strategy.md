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

## Schema v1 implementado

Arquivo JSON UTF-8: lista não vazia de objetos, sem campos extras:

| Campo | Tipo e regra |
|---|---|
| id | string não vazia e única; identificador sintético |
| group_id | string não vazia; thread/template e variações pertencem ao mesmo grupo |
| subject | string; assunto ou corpo deve conter texto |
| body | string; texto simples, sem anexos |
| is_spam | booleano JSON estrito |
| category | null para spam, categoria v1 para legítimos |
| source | nesta fase somente `synthetic` |
| split | `train`, `validation` ou `test` |

O loader rejeita IDs duplicados, conteúdo normalizado idêntico e grupos em splits
diferentes. A detecção automática não identifica todas as paráfrases: agrupar templates
é responsabilidade de quem prepara o dataset. Cada split deve conter spam e todas
as categorias legítimas. Features: somente assunto + corpo. IDs, grupos e labels não
entram no modelo. Sem remetentes, domínios ou outros metadados privados nesta fase.
Validação serve para diagnósticos; teste fica reservado ao relatório final. Thresholds
iniciais são provisórios, não otimizados no teste. Exemplos em `data/examples/` são
inteiramente inventados e não medem generalização real.
