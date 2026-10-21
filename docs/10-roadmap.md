# Roadmap

## Etapa 0 — Documentação

- [x] definir visão inicial;
- [x] definir arquitetura conceitual;
- [x] registrar estratégia de dados;
- [x] definir baseline de ML;
- [x] documentar segurança;
- [ ] revisar taxonomia com casos reais;
- [ ] definir dataset inicial.

## Etapa 1 — Dataset

- [ ] definir schema;
- [ ] coletar exemplos permitidos;
- [ ] criar processo de anonimização;
- [ ] criar splits de treino/validação/teste;
- [ ] documentar distribuição das classes.

## Etapa 2 — Baseline de spam

- [ ] implementar pré-processamento;
- [ ] implementar TF-IDF;
- [ ] treinar Logistic Regression;
- [ ] medir métricas;
- [ ] registrar baseline.

## Etapa 3 — Categorização

- [ ] treinar classificador multiclasse;
- [ ] avaliar categorias confundidas;
- [ ] ajustar taxonomia;
- [ ] definir threshold para revisão.

## Etapa 4 — Gmail em modo seguro

- [ ] configurar projeto Google Cloud;
- [ ] configurar OAuth;
- [ ] ler mensagens de teste;
- [ ] criar labels `IA/*`;
- [ ] classificar sem alterar mensagens;
- [ ] habilitar aplicação de labels.

## Etapa 5 — Human-in-the-loop

- [ ] identificar classificações incertas;
- [ ] registrar correções humanas;
- [ ] preparar exemplos corrigidos para retreinamento;
- [ ] versionar métricas e modelos.

## Etapa 6 — Experimentos avançados

- [ ] testar alternativas clássicas;
- [ ] avaliar embeddings;
- [ ] comparar Transformers com baseline;
- [ ] avaliar custo/benefício.
