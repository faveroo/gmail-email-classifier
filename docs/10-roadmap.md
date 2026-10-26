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

## Entrega local de 2026-10-26

- [x] encerrar bloqueio de implementação da Etapa 0 por autorização do usuário;
- [x] taxonomia v1 com critérios e ambiguidade (validação real pendente);
- [x] schema e validação de integridade;
- [x] dataset público sintético e splits explícitos, com distribuição documentada;
- [x] baseline de spam e categorização, treinamento e inferência separados;
- [x] política provisória de revisão humana, métricas e registro do experimento;
- [x] CLI local, testes, CI e documentação de execução;
- [ ] coleta real autorizada, anonimização e revisão da taxonomia com dados representativos;
- [ ] calibração e escolha de thresholds na validação, antes de avaliação final;
- [ ] integração Gmail em etapa futura explícita.

Os itens anteriores do roadmap referentes a dados representativos continuam pendentes.
O baseline sintético cobre a engenharia das Etapas 1–3, sem afirmar conclusão empírica
dessas etapas em produção.
