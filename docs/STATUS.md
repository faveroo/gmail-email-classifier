# Status do Projeto

## Fase atual

**Baseline local, Gmail somente leitura e primeiro experimento privado com supervisão do ChatGPT treinado/testado em 2026-10-27.**
O usuário escolheu OAuth somente leitura para coleta de amostras reais privadas.
Adaptador e fluxo local implementados; configuração Cloud, consentimento e coleta inicial concluídos.

## Escopo desta entrega

Taxonomia v1, schema validado, estrutura Python, baseline TF-IDF + Logistic Regression
em dois estágios, política de revisão, CLI local, testes e instruções de execução.
Agora também: OAuth somente leitura opcional, coleta limitada com minimização de dados,
rotulagem/revisão manual, preparação de dataset privado e simulação offline em lote.
Guia: `docs/12-gmail-readonly-setup.md`.
O comando `review` oferece formulário de rotulagem no navegador local, com backup
e salvamento por mensagem; nenhum rótulo ou confirmação humana é gerado automaticamente.
Por solicitação explícita posterior, o ChatGPT classificou a amostra em um fluxo
experimental separado (`gmail_ai_labeled`), sem marcar revisão humana.

## Validação concluída

- 41 testes automatizados de schema, isolamento, política, persistência e CLI.
- Treinamento e previsão executados em Python 3.13.14.
- Métricas e ambiente registrados em `docs/experiments/baseline-v1.json`.
- Política padrão encaminhou 100% dos exemplos de validação e teste para revisão.
- CI adicionada para Python 3.11 e 3.13; resultado remoto deve ser consultado no GitHub.
- Em 2026-10-27: 59 testes passaram com Python 3.13.14, incluindo OAuth e API simulados,
  extração MIME, paginação, minimização, revisão, caminhos privados, treino e simulação.
- Após adicionar o formulário local: 65 testes passaram, incluindo escape de HTML,
  proteção de origem/CSRF, backup, rejeição de edição desatualizada e preservação de grupos.
- Dependências opcionais Gmail instaladas no ambiente local.
- Autenticação real concluída com `gmail.readonly` em 2026-10-27.
- Primeira coleta: 50 mensagens dos últimos 30 dias, sem Spam/Lixeira; 50 consultadas,
  50 salvas localmente fora do Git, nenhuma descartada na extração.
- Simulação offline com o baseline sintético: 50 previsões, todas `IA/Revisar`, zero
  alterações na caixa. Sem rótulos humanos, não há métricas de acurácia nesta amostra.
- Experimento autorizado: 50 rótulos atribuídos pelo ChatGPT, 32 mensagens em treino,
  9 em validação e 9 em teste; conversas/templates agrupados antes da separação.
- Novo categorizador treinado exclusivamente no split de treino e comparado ao baseline
  nos mesmos splits. Detector de spam anterior preservado por falta de positivos.
- 71 testes passaram após adicionar opt-in de IA, cobertura parcial explícita,
  isolamento de treino, procedência e preservação do detector de spam.
- Modelo, manifesto de rótulos, relatórios e comparação permanecem em armazenamento
  privado. Nenhum parâmetro/threshold foi alterado usando o teste.

## Limites

As 50 mensagens reais e seus derivados permanecem privados. Revisão humana de conteúdo
e rótulos continua pendente; o experimento usa rótulos de IA conforme autorização explícita.
Filtros e minimização assistida não garantem anonimização. As métricas são concordância
com o ChatGPT, não acurácia validada por pessoas. A amostra tem cobertura parcial e não
inclui exemplos positivos de spam. O fluxo completo permanece em revisão para todas
as mensagens, com thresholds provisórios preservados.
Nenhuma escrita Gmail implementada ou realizada.

## Próxima etapa

Ampliar amostra com grupos independentes, categorias raras e spam confirmado; obter
referência humana independente para medir qualidade. Usar validação para futuros ajustes
e reservar novo teste final. Calibração e escrita no Gmail continuam pendentes de etapas
posteriores. Resultado detalhado: `resultado-ai-v1.md` no armazenamento privado local.

## Experimento SpamShield multilíngue (2026-10-28)

Implementado um pipeline paralelo para `M-Arjun/SpamShield-Datasets`: download gated
da HF, deduplicação de textos idênticos, divisão estratificada por idioma/rótulo,
baseline TF-IDF de caracteres + Logistic Regression, métricas globais e por idioma,
e dashboard Streamlit para métricas e classificação local. O corpus declarado contém
23 idiomas e é SMS binário; não altera o baseline de e-mail nem integra Gmail.

Os arquivos do dataset continuam fora do Git; atribuição CC-BY-4.0 registrada na UI e
documentação. Os arquivos do modelo/relatório só serão gerados após aceite dos termos
do dataset na conta HF e execução local. Dutch/Italian não contêm ham. Neste ambiente,
não há sessão/token Hugging Face ativo; por isso, o corpus real ainda não foi baixado,
e o treino/teste oficial não foram executados. O pipeline teve smoke test com dados
sintéticos temporários, fora do repositório.
