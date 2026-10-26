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

## Relatório local implementado

O JSON em reports/baseline.json distingue os três splits; apresenta métricas de spam
em 0.5 e na política operacional, falsos positivos, precision de spam (null quando
nenhuma sugestão), categorias avaliadas sobre legítimos verdadeiros, distribuição
de confiança, taxa de revisão e acerto da label no fluxo completo. A matriz de confusão
usa linhas verdadeiras e colunas previstas na ordem labels. Revisão conta como abstenção,
não como classificação correta. O diagnóstico de categorias isolado não mede erros
propagados do primeiro estágio. Não há seleção de parâmetros usando o teste.
80 exemplos sintéticos verificam execução e isolamento, não generalização real.
