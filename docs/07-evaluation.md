# Avaliação

## Spam

Métricas prioritárias:

- Precision;
- Recall;
- F1-score;
- matriz de confusão.

## Principal risco

Falso positivo:

```text
email legítimo -> classificado como spam
```

Por isso, a decisão automática deverá usar threshold conservador.

## Categorias

Métricas prioritárias:

- F1 macro;
- F1 por categoria;
- matriz de confusão;
- distribuição de confiança.

## Baseline

Toda alteração relevante no modelo deverá ser comparada ao baseline anterior no mesmo conjunto de teste.

## Critério de adoção

Um modelo mais complexo só deverá substituir o atual se demonstrar ganho mensurável e relevante, sem aumentar desnecessariamente custo, latência ou dificuldade operacional.
