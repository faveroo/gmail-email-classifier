# Gmail Email Classifier

Projeto experimental para construir um classificador de e-mails integrado ao Gmail, usando Machine Learning em Python.

> **Estado atual:** planejamento e documentação. Ainda não existe código Python neste repositório.

## Objetivo

Criar um sistema capaz de:

1. identificar e-mails potencialmente classificados como spam;
2. categorizar e-mails legítimos em categorias úteis;
3. aplicar labels no Gmail de forma segura e reversível;
4. aprender com correções humanas ao longo do tempo;
5. permitir comparar abordagens clássicas de Machine Learning com modelos mais avançados no futuro.

A primeira abordagem planejada utiliza **TF-IDF + Logistic Regression** como baseline.

## Princípios do projeto

- começar simples antes de utilizar redes neurais ou Transformers;
- separar a detecção de spam da categorização;
- priorizar a redução de falsos positivos de spam;
- não executar ações destrutivas durante as primeiras fases;
- utilizar labels `IA/*` durante testes;
- manter dados de e-mail e credenciais fora do repositório público;
- medir o desempenho antes de aumentar a complexidade do modelo;
- manter revisão humana para previsões com baixa confiança.

## Documentação

A especificação do projeto está em [`docs/`](docs/).

Leitura recomendada:

1. [`docs/01-vision.md`](docs/01-vision.md)
2. [`docs/02-scope.md`](docs/02-scope.md)
3. [`docs/03-architecture.md`](docs/03-architecture.md)
4. [`docs/04-data-strategy.md`](docs/04-data-strategy.md)
5. [`docs/05-label-taxonomy.md`](docs/05-label-taxonomy.md)
6. [`docs/06-ml-plan.md`](docs/06-ml-plan.md)
7. [`docs/07-evaluation.md`](docs/07-evaluation.md)
8. [`docs/08-gmail-integration.md`](docs/08-gmail-integration.md)
9. [`docs/09-privacy-security.md`](docs/09-privacy-security.md)
10. [`docs/10-roadmap.md`](docs/10-roadmap.md)
11. [`docs/11-decisions.md`](docs/11-decisions.md)

O andamento atual está em [`docs/STATUS.md`](docs/STATUS.md).

## Estrutura planejada

```text
gmail-email-classifier/
├── data/
├── docs/
├── models/
├── src/
├── tests/
├── AGENTS.md
└── README.md
```

As pastas de implementação existem inicialmente apenas com documentação. Código deve ser introduzido somente quando a etapa correspondente do roadmap for iniciada.

## Segurança

Este é um repositório público. Portanto, nunca devem ser versionados:

- e-mails reais;
- nomes ou endereços pessoais extraídos dos e-mails;
- anexos;
- tokens OAuth;
- `credentials.json`;
- `token.json`;
- datasets contendo informações confidenciais;
- modelos treinados que possam memorizar informações sensíveis sem revisão prévia.

Consulte [`docs/09-privacy-security.md`](docs/09-privacy-security.md).
