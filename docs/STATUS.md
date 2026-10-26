# Status do Projeto

## Fase atual

**Implementação iniciada em 2026-10-26 — Etapas 1 a 3, exclusivamente com dados sintéticos.**
O usuário autorizou sair da Etapa 0. Python está autorizado. A integração Gmail permanece futura.

## Escopo desta entrega

Taxonomia v1, schema validado, estrutura Python, baseline TF-IDF + Logistic Regression
em dois estágios, política de revisão, CLI local, testes e instruções de execução.

## Validação concluída

- 41 testes automatizados de schema, isolamento, política, persistência e CLI.
- Treinamento e previsão executados em Python 3.13.14.
- Métricas e ambiente registrados em `docs/experiments/baseline-v1.json`.
- Política padrão encaminhou 100% dos exemplos de validação e teste para revisão.
- CI adicionada para Python 3.11 e 3.13; resultado remoto deve ser consultado no GitHub.

## Limites

Nenhum acesso a Gmail, credenciais ou mensagens reais. Resultados sintéticos verificam
engenharia do pipeline; não demonstram qualidade em uma caixa real. Thresholds provisórios.

## Próxima etapa

Revisar resultados locais e planejar, separadamente, coleta autorizada, anonimização,
rotulagem humana e avaliação com dados representativos antes de qualquer automação Gmail.
