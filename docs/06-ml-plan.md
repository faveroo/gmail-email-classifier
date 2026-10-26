# Plano de Machine Learning

## Tipo de problema

Classificação supervisionada de texto.

## Baseline planejado

### Representação

TF-IDF.

### Classificador

Logistic Regression.

### Motivos

- implementação simples;
- treinamento rápido;
- boa referência para classificação textual;
- suporte a probabilidades;
- facilidade de interpretação e depuração;
- funciona bem com matrizes esparsas.

## Experimentos posteriores

Somente após o baseline:

- Linear SVM;
- Naive Bayes;
- combinações de word n-grams e character n-grams;
- embeddings;
- Sentence Transformers;
- modelos Transformer em português/multilíngues.

## Features candidatas

Conteúdo textual:

- assunto;
- corpo;
- remetente/domínio;
- combinação ponderada dos campos.

Metadados poderão ser avaliados separadamente.

## Hierarquia prevista

1. classificador de spam;
2. caso não seja spam, classificador de categoria.

Isso permite métricas, thresholds e ciclos de treinamento independentes.

## Baseline local v0.1 implementado

Dois pipelines independentes: TF-IDF de palavras (unigramas e bigramas,
acentos normalizados), LogisticRegression com class_weight=balanced,
random_state=42 e max_iter=1000. Assunto + corpo; sem features de metadados.
Fit exclusivamente no split train; categorizador treinado somente com legítimos.
Thresholds provisórios conforme D008; não ajustados pelo conjunto de teste.
Artefato joblib contém versão de formato, pacote, sklearn e política. CLI e setup no README.
