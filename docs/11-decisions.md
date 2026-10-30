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

## D009 — Gmail OAuth somente leitura e preparação privada (2026-10-27)

**Status:** implementação autorizada pelo usuário, que escolheu OAuth somente leitura.
Configuração Google Cloud e consentimento real concluídos em 2026-10-27, após o
usuário salvar o cliente e concluir o login. Primeira coleta limitada e simulação
concluídas: 50 mensagens, todas encaminhadas para revisão, nenhuma alteração na caixa.
Revisão humana, treino com dados reais e avaliação representativa continuam pendentes.

Usar cliente Desktop dedicado, escopo exclusivo `gmail.readonly` e callback loopback
com PKCE. Adaptador de coleta separado do ML, consulta explícita e limite de 1–500.
Não implementar escrita, criação de labels ou ações sobre mensagens nesta etapa.

Coletar somente assunto/corpo necessários, ignorar anexos e usar IDs aleatórios locais.
Filtros automáticos são minimização, não garantia de anonimização. Exigir revisão
humana de privacidade e rótulos antes de preparar dataset, com isolamento por grupo.
Threads entre coletas e templates exigem agrupamento manual. Campos têm limite de texto.

Aceitar `gmail_reviewed` somente com opt-in para treino/avaliação, sem misturar dados
sintéticos e reais; relatórios indicam a origem correta. Credenciais, tokens, coletas,
datasets, modelos e relatórios privados devem ficar fora do checkout e de árvores Git.
Preservar o baseline e thresholds até medir resultados representativos. Não afirmar
coleta, calibração ou qualidade real com base nos testes simulados.

## D010 — Rotulagem humana antes do treino real (2026-10-27)

**Status:** implementado para viabilizar o treinamento solicitado. A inspeção inicial
da coleta encontrou 50 mensagens sem rótulos, revisão de privacidade ou splits.
O treinamento supervisionado aguarda esses dados; não usar previsões do baseline
como referência humana nem marcar revisões automaticamente.

Disponibilizar o comando `review`, com formulário em loopback e salvamento local,
para revisar texto, categoria, privacidade e grupos/splits. Preservar backup, rejeitar
edições desatualizadas e impedir vazamento do conteúdo via HTML ou logs. Treinar
somente depois de validar revisão, integridade e cobertura das classes. A revisão
inicial pode indicar necessidade de mais coleta para cobrir classes ausentes.

## D011 — Experimento com rótulos do ChatGPT por solicitação explícita (2026-10-27)

**Status:** autorizado pelo usuário e executado. O usuário pediu que o ChatGPT
classificasse as mensagens pendentes e então treinasse/testasse, substituindo a
exigência de rotulagem humana para este experimento. D010 continua válida para o
fluxo de referência humana; esta exceção não permite fingir revisão por uma pessoa.

Usar source `gmail_ai_labeled` e opt-in separado, manter anotações e artefatos privados,
relatar concordância com os rótulos da IA e preservar um teste isolado por grupos.
Permitir cobertura parcial no experimento, explicitando classes não avaliadas. Não
classificar promoções como spam apenas por serem comerciais. Sem ambas as classes de
spam, preservar estágio de referência explicitamente selecionado e não afirmar novo fit.

O categorizador da amostra foi treinado/testado sem alterar algoritmo ou thresholds,
com comparação ao baseline original. O fluxo Gmail continua somente leitura; nenhuma
label foi aplicada. Generalização e automação confiável exigem amostra maior e revisão
independente. Resultados detalhados ficam no relatório privado do experimento.

## D012 — Experimento binário com SpamShield multilíngue (2026-10-28)

**Status:** implementação autorizada pelo pedido do usuário. Usar o corpus gated
`M-Arjun/SpamShield-Datasets` em fluxo Python isolado, mantendo os dados no cache
local e citando a licença CC-BY-4.0. A aquisição exige que o usuário aceite os termos
do dataset no Hugging Face e autentique localmente.

Treinar TF-IDF de caracteres + Logistic Regression para spam/ham, com deduplicação
textual exata e split 70/15/15 estratificado por idioma e label. Criar dashboard local
para métricas por idioma e inferência de texto. O corpus é de SMS e não substitui a
avaliação de e-mail, não treina as categorias da taxonomia existente e não autoriza
alterar Gmail. Dutch/Italian são spam-only. Atribuir a fonte e registrar transformação.
