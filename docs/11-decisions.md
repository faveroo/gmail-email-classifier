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
