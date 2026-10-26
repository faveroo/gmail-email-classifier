# Baseline sintético v1 — 2026-10-26

Comando: `email-classifier train --dataset data/examples/synthetic-v1.json`.
Resultado completo em `baseline-v1.json`, com hash do dataset, ambiente, política e seed.
Somente métricas agregadas de dados inventados. Modelos e relatórios locais ficam ignorados.

| Medida | Validação (20) | Teste (20) |
|---|---:|---:|
| F1 macro de categorias, sobre legítimos verdadeiros | 0.8333 | 0.9407 |
| Taxa de revisão do fluxo completo | 100% | 100% |
| Sugestões automáticas de spam | 0 | 0 |
| Acerto de label no fluxo completo (abstenção não conta) | 0% | 0% |

Sem sugestões de spam, precision operacional é indefinida (`null`); zero falsos positivos
nessa situação não demonstra segurança de automação. O segundo modelo isolado pode
separar exemplos simples e ainda assim o fluxo completo se abster de todas as decisões.
Os quatro exemplos de treino por classe são insuficientes para confiança operacional.
Não ajustamos thresholds após observar o teste. O próximo passo é um plano separado
para dados representativos e autorizados, com rotulagem e validação de thresholds.

Métricas podem variar entre versões das bibliotecas; este registro preserva o ambiente
exato usado. Para comparar mudanças, manter dataset/splits e registrar novo relatório.
