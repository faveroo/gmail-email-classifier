# Gmail Email Classifier

Projeto experimental para construir um classificador de e-mails integrado ao Gmail, usando Machine Learning em Python.

> **Estado atual:** baseline local executável com dados exclusivamente sintéticos. Implementação iniciada em 2026-10-26.

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

## Estrutura

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

O pacote Python fica em `src/gmail_classifier/`; testes em `tests/`, exemplos públicos em `data/examples/`. Não há integração Gmail implementada.

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

## Executar localmente

Requer Python 3.11 ou superior. No PowerShell, na raiz do repositório:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev]"
.\.venv\Scripts\python -m pytest
.\.venv\Scripts\email-classifier train --dataset data/examples/synthetic-v1.json
.\.venv\Scripts\email-classifier predict --model models/baseline.joblib --subject "Fatura disponível" --body "Pagamento do boleto da mensalidade"
```

No Linux/macOS use `.venv/bin/python` e `.venv/bin/email-classifier`.
O treinamento cria `models/baseline.joblib` e `reports/baseline.json`, ignorados pelo Git.
O relatório inclui distribuição, precision/recall/F1, matrizes de confusão, F1 macro,
confiança por categoria, taxa de revisão e acerto de labels no fluxo completo.
`category_on_true_legitimate` avalia o segundo modelo isoladamente; não representa a
qualidade do fluxo completo. `spam_policy_precision: null` significa nenhuma sugestão
de spam, não precision perfeita. Treino é diagnóstico, validação apoia decisões futuras
e teste é reservado à avaliação final; nenhum dos dois últimos entra no fit do TF-IDF.

A política sugere `IA/SPAM` a partir de 0.90. Até 0.20 de probabilidade de spam,
a categoria precisa de confiança >= 0.60. Os demais casos vão para `IA/Revisar`.
Esses valores são provisórios e configuráveis no treinamento com `--spam-threshold`,
`--legitimate-threshold` e `--category-threshold`. Não são garantias de precisão.
A CLI só produz JSON; não modifica mensagens. Texto totalmente fora do vocabulário
vai para revisão, mas esse filtro não detecta toda mudança de domínio.

O dataset contém 80 mensagens inventadas (40 treino, 20 validação, 20 teste):
por split, respectivamente 4/2/2 exemplos de cada categoria e de spam. É uma amostra
pequena para verificar o pipeline, insuficiente para avaliar qualidade real ou calibrar
probabilidades. Não reduza os thresholds apenas para obter mais labels automáticas.

Carregue apenas modelos treinados por você em ambiente confiável: o formato joblib
pode executar código ao ser aberto. Retreine ao trocar a versão do scikit-learn.
Não forneça mensagens privadas nos argumentos da CLI, pois podem ficar no histórico
do terminal. A fase atual aceita apenas datasets declarados como `synthetic`; essa
validação não consegue provar que um texto foi realmente inventado.

Resultado inicial: a política padrão encaminhou 100% dos exemplos para revisão.
Consulte [o registro do experimento](docs/experiments/README.md) antes de interpretar
as métricas isoladas dos modelos.
