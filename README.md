# Gmail Email Classifier

Projeto experimental para construir um classificador de e-mails integrado ao Gmail, usando Machine Learning em Python.

> **Estado atual:** Gmail somente leitura e primeiro experimento privado com rótulos do ChatGPT treinado/testado em 2026-10-27. Avaliação humana independente e automação Gmail permanecem pendentes.

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

O pacote Python fica em `src/gmail_classifier/`; testes em `tests/`, exemplos públicos em `data/examples/`. O adaptador Gmail é separado do ML e só permite leitura.

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
A CLI não modifica mensagens; as operações concluídas produzem JSON. Texto totalmente fora do vocabulário
vai para revisão, mas esse filtro não detecta toda mudança de domínio.

O dataset contém 80 mensagens inventadas (40 treino, 20 validação, 20 teste):
por split, respectivamente 4/2/2 exemplos de cada categoria e de spam. É uma amostra
pequena para verificar o pipeline, insuficiente para avaliar qualidade real ou calibrar
probabilidades. Não reduza os thresholds apenas para obter mais labels automáticas.

Carregue apenas modelos treinados por você em ambiente confiável: o formato joblib
pode executar código ao ser aberto. Retreine ao trocar a versão do scikit-learn.
Não forneça mensagens privadas nos argumentos da CLI, pois podem ficar no histórico
do terminal. O treino padrão aceita apenas datasets declarados como `synthetic`; essa
validação não consegue provar que um texto foi realmente inventado. O fluxo privado
exige revisão e `--allow-private`, com arquivos fora do repositório. O experimento
explicitamente autorizado com rótulos de IA usa source próprio e também `--allow-ai-labels`.

Resultado inicial: a política padrão encaminhou 100% dos exemplos para revisão.
Consulte [o registro do experimento](docs/experiments/README.md) antes de interpretar
as métricas isoladas dos modelos.

## Próxima etapa: Gmail somente leitura

O [guia de configuração e coleta](docs/12-gmail-readonly-setup.md) explica como criar
o cliente OAuth no Google Cloud, autenticar e preparar uma amostra rotulada local.
Instale as dependências opcionais com `python -m pip install -e ".[dev,gmail]"`.

Comandos disponíveis: `gmail-auth`, `gmail-collect`, `review`, `prepare-dataset` e `predict-batch`.
Credenciais, tokens, coletas e artefatos privados ficam por padrão em
`%LOCALAPPDATA%\GmailEmailClassifier`, fora do Git. A coleta é limitada e o filtro
de dados pessoais exige revisão humana complementar. A primeira autenticação e coleta
real foram concluídas em 2026-10-27. A primeira simulação com o baseline sintético
encaminhou as 50 mensagens para revisão. Posteriormente, por solicitação explícita,
o ChatGPT rotulou a amostra e um novo categorizador foi treinado/testado localmente.
O estágio de spam anterior foi preservado por falta de exemplos positivos. A política
continua conservadora e nenhuma alteração foi feita no Gmail.

Para rotular a amostra no navegador local, execute
`.\.venv\Scripts\email-classifier review`. A tela salva o progresso e mostra a
cobertura das classes por split. Esse é o fluxo para referência humana; o experimento
com supervisão da IA é separado e suas métricas não representam acurácia validada por pessoas.

### Treinamento experimental com rótulos de IA

O source `gmail_ai_labeled` requer opt-in explícito e todos os arquivos fora do Git:

```powershell
$privateDir = Join-Path $env:LOCALAPPDATA "GmailEmailClassifier"
.\.venv\Scripts\email-classifier train --allow-private --allow-ai-labels --dataset "$privateDir\dataset-ai-v1.json" --spam-reference models/baseline.joblib --model "$privateDir\baseline-ai-v1.joblib" --report "$privateDir\baseline-ai-v1-report.json"
```

Não há chamada a LLM no treinamento: os rótulos foram atribuídos pelo ChatGPT durante
a tarefa autorizada. O relatório indica supervisão da IA, fontes por estágio e limites
de cobertura. `--spam-reference` preserva um detector confiável quando a amostra tem
uma única classe de spam. O modelo experimental deve ser selecionado explicitamente
em `predict`/`predict-batch`; o baseline original continua disponível.

## Experimento multilíngue SpamShield

O pipeline separado `spamshield` usa o corpus de SMS [M-Arjun/SpamShield-Datasets](https://huggingface.co/datasets/M-Arjun/SpamShield-Datasets), que informa 149.359 mensagens em 23 idiomas e licença CC-BY-4.0. O acesso aos arquivos é gated: entre na sua conta Hugging Face, aceite as condições na página do dataset e autentique a CLI localmente. O código não envia credenciais a terceiros.

```powershell
python -m pip install -e ".[multilingual,dashboard]"
hf auth login
python -m gmail_classifier.cli download-spamshield
python -m gmail_classifier.cli train-spamshield
streamlit run src/gmail_classifier/dashboard.py
```

`train-spamshield` baixa o parquet para o cache Hugging Face se `--dataset` não for informado. O treino remove duplicatas exatas normalizadas e faz divisão estratificada 70/15/15 por idioma e rótulo, com seed 42. Usa TF-IDF de caracteres (n-gramas 2–5) e Logistic Regression; o relatório inclui métricas globais e por idioma nos três splits. O painel permite testar texto localmente, consultar métricas/matriz de confusão e inspecionar a distribuição.

Os artefatos ficam em `models/spamshield-multilingual.joblib` e `reports/spamshield-multilingual.json`, ambos ignorados pelo Git; os dados permanecem no cache Hugging Face. Atribuição CC-BY-4.0: M-Arjun, SpamShield-Datasets, [licença CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/); o dataset é transformado por deduplicação e separação em splits. Este classificador é binário (spam/ham) e o corpus é de SMS, não de Gmail. Dutch e Italian não têm exemplos ham; métricas nesses idiomas não medem capacidade de separar spam e ham. A avaliação do dataset não deve ser interpretada como desempenho em e-mails.
