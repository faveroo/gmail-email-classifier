# Registro de Decisões

Este arquivo resume decisões arquiteturais e de produto relevantes.

## D001 — Repositório público sem código na fase inicial

**Status:** aceito.

O projeto começa com documentação e estrutura de pastas. Código Python será adicionado somente após a etapa de planejamento.

## D002 — Dois classificadores conceituais

**Status:** provisoriamente aceito.

Separar spam e categorização temática permite thresholds, datasets e métricas independentes.

## D003 — Baseline com TF-IDF + Logistic Regression

**Status:** aceito para o primeiro experimento.

Modelos mais complexos deverão ser comparados objetivamente a esse baseline.

## D004 — Labels reversíveis no Gmail

**Status:** aceito.

Durante testes, usar labels `IA/*` em vez de ações destrutivas.

## D005 — Human-in-the-loop

**Status:** planejado.

Casos de baixa confiança deverão ser encaminhados para revisão humana e poderão alimentar ciclos futuros de treinamento.

## D006 — Implementação local autorizada (2026-10-26)

**Status:** aceito. A restrição inicial de D001 foi cumprida e a implementação Python
está autorizada pelo usuário. Gmail e dados privados ficam para etapa explícita posterior.

## D007 — Taxonomia v1 e schema sintético

**Status:** aceito para o baseline local. Preservar as nove categorias documentadas,
com regras de finalidade/ambiguidade em 05. JSON estrito conforme 04, com grupo e split
explícitos. Nenhuma mensagem real ou metadado pessoal nos exemplos públicos.

## D008 — Política conservadora provisória

**Status:** aceito para demonstração. Spam com probabilidade >= 0.90 sugere IA/SPAM;
probabilidade <= 0.20 permite categorização. Intervalo intermediário exige IA/Revisar.
Categoria exige confiança >= 0.60; vocabulário totalmente desconhecido exige revisão.
Probabilidades não são calibradas e thresholds precisam de validação representativa.
Somente sugestões locais, sem ações externas.
