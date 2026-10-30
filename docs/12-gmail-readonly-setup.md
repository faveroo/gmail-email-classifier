# Gmail somente leitura: configuração e primeira amostra

Implementação autorizada em 2026-10-27. Primeira autenticação, coleta de 50 mensagens
e simulação concluídas nessa data. Todas as previsões exigiram revisão; nenhum e-mail
foi alterado. O login e o consentimento são feitos por você no navegador.
A aplicação solicita exclusivamente `gmail.readonly`.

## 1. Preparar o Google Cloud

Siga a [configuração oficial da Gmail API para Python](https://developers.google.com/workspace/gmail/api/quickstart/python):

1. Crie ou selecione um projeto no [Google Cloud Console](https://console.cloud.google.com/).
2. Habilite a **Gmail API** nesse projeto.
3. Configure a **Google Auth Platform** (nome da aplicação e contato).
   Para uma conta Gmail pessoal, use público **External**, mantenha o aplicativo
   em teste e adicione seu próprio endereço como usuário de teste. **Internal**
   só se aplica quando disponível para a organização Workspace.
4. Em **Data Access**, inclua somente
   `https://www.googleapis.com/auth/gmail.readonly`.
5. Em **Clients**, crie um cliente OAuth do tipo **Desktop app / Aplicativo para computador**.
   Use um cliente dedicado a este projeto, sem permissões anteriores de escrita.
6. Baixe o JSON do cliente e salve-o como
   `%LOCALAPPDATA%\GmailEmailClassifier\credentials.json`.
   Não envie o conteúdo do arquivo pelo chat nem o coloque no repositório.

Para detalhes de público e usuários de teste, consulte a
[configuração oficial do consentimento OAuth](https://developers.google.com/workspace/guides/configure-oauth-consent).
Ter o arquivo do cliente não conclui a autenticação: o consentimento é realizado na etapa seguinte.

## 2. Autenticar localmente

No PowerShell, na raiz do repositório:

```powershell
.\.venv\Scripts\python -m pip install -e ".[dev,gmail]"
$privateDir = Join-Path $env:LOCALAPPDATA "GmailEmailClassifier"
New-Item -ItemType Directory -Force -Path $privateDir | Out-Null
.\.venv\Scripts\email-classifier gmail-auth
```

O navegador abrirá a página de consentimento. Confira a conta e a permissão de leitura.
O callback usa apenas `127.0.0.1`, porta temporária, com espera máxima de três minutos.
Não copie URLs de callback ou tokens para o terminal/chat. Se o navegador não abrir,
execute novamente em uma sessão local com navegador padrão configurado.

O token é salvo em `$privateDir\token.json`; a coleta pode renová-lo sem abrir um
novo consentimento. Se estiver revogado/expirado e não puder ser renovado, remova apenas
esse token local e execute `gmail-auth` novamente. Tokens com escopos diferentes ou
mais amplos são rejeitados. Para encerrar o acesso, revogue a autorização nas
[conexões da sua Conta Google](https://myaccount.google.com/connections) e remova o token local.

## 3. Coletar uma pequena amostra

```powershell
.\.venv\Scripts\email-classifier gmail-collect --query "newer_than:30d -in:trash" --limit 50
```

O resultado fica em `$privateDir\review.json`. O terminal mostra apenas contagens.
O padrão não inclui Spam/Lixeira. Para uma coleta que inclua spam, com outro arquivo:

```powershell
.\.venv\Scripts\email-classifier gmail-collect --query "in:spam newer_than:90d" --include-spam --limit 30 --output "$privateDir\review-spam.json"
```

`--include-spam` permite resultados de Spam **e Lixeira** na API; a consulta ainda
delimita quais mensagens são candidatas. Labels existentes não viram rótulos de treino.
Os limites aceitos vão de 1 a 500 mensagens consultadas por execução. A API retorna
mensagens em páginas; a coleta não garante aleatoriedade ou representatividade.
Arquivos existentes não são substituídos. Use outro `--output` para repetir.

Somente assunto e corpo textual são persistidos, após filtros de minimização:
URLs, endereços de e-mail e alguns números são substituídos. IDs de mensagens e
conversas recebem identificadores aleatórios locais. Não são salvos remetentes,
destinatários, labels originais, consulta ou IDs Gmail. Anexos e mensagens anexadas
não são baixados separadamente nem incorporados ao texto. HTML é convertido em texto,
sem executar scripts ou carregar recursos externos. Assunto e corpo são limitados
a 20 mil caracteres cada; isso pode remover contexto e deve ser considerado na revisão.

**O arquivo ainda é privado:** nomes, endereços físicos, segredos e informações
confidenciais podem permanecer. Os filtros não garantem anonimização. O conteúdo
bruto é processado em memória; não é salvo como dump nem enviado a modelos externos.
O armazenamento local herda as permissões da sua conta Windows; não há criptografia
adicional implementada. Não use uma pasta compartilhada ou sincronizada publicamente.

## 4. Revisar e rotular

Para revisar no navegador local, sem editar JSON manualmente:

```powershell
.\.venv\Scripts\email-classifier review
```

O comando abre uma tela em `http://127.0.0.1` numa porta temporária. Ela não conecta
ao Gmail e não usa recursos externos. Mantenha o processo aberto durante a revisão;
Ctrl+C o encerra. O progresso é salvo por mensagem no próprio `review.json`, e a
primeira edição cria `review.before-review.json` no mesmo armazenamento privado.
Essa cópia também contém dados privados e deve seguir a mesma política de retenção.
Para retomar, execute o comando novamente e navegue até a mensagem desejada.
Se o arquivo mudar em outra janela, recarregue a página antes de salvar.

A tela permite editar assunto/corpo, escolher Spam ou categoria, confirmar as duas
revisões e excluir registros. Em **Separação de dados e agrupamento**, defina o split
e una templates quando necessário. A divisão se aplica ao grupo inteiro. Ao unir um
grupo a outro, toda a conversa original é movida junto, evitando quebrar threads.
O painel inferior mostra as classes que faltam em cada divisão e a prontidão do dataset.
A confirmação de revisão não inicia treino automaticamente.

Também é possível abrir `review.json` em um editor local, sem compartilhá-lo. Para cada registro:

- remova manualmente nomes, assinaturas, endereços e demais detalhes desnecessários;
- defina `is_spam` como `true` ou `false`;
- para spam, deixe `category: null`; para legítimos, escolha uma das
  [nove categorias](05-label-taxonomy.md);
- ajuste `group_id` para unir templates semelhantes, mesmo que sejam conversas distintas;
- atribua `split`: `train`, `validation` ou `test`, mantendo cada grupo em um único split;
- marque `human_reviewed: true` e `privacy_reviewed: true` apenas após realizar as revisões;
- use `exclude: true` para descartar mensagens ambíguas, sensíveis ou inadequadas.

Não altere os IDs aleatórios nem use informações pessoais neles. Os flags são
declarações humanas; o programa não consegue comprovar a qualidade dessa revisão.
`source: gmail_reviewed` identifica o fluxo de origem, e não uma revisão automática.

Uma amostra inicial de 50 mensagens serve para testar a coleta. Para avaliação,
planeje amostras de períodos e categorias variados, incluindo spam, sem selecionar
somente casos fáceis. Como ponto de partida, distribua grupos aproximadamente em
60% treino, 20% validação e 20% teste, verificando a distribuição por classe.
O validador exige spam e as nove categorias em **cada split**. Se faltarem classes,
colete e rotule mais exemplos; não invente rótulos para completar a distribuição.
Três grupos independentes por classe são apenas um mínimo estrutural, não suficiência estatística.

Antes de combinar coletas, revise IDs, threads, templates e duplicatas manualmente:
os pseudônimos são específicos de cada execução e não reconhecem conversas entre arquivos.
Faça a união dos registros em um arquivo de revisão local com os mesmos campos.
O validador rejeita texto idêntico após normalização; remova duplicatas e confira
paráfrases/templates manualmente para impedir vazamento entre splits.

## 5. Preparar dataset, treinar e avaliar

```powershell
.\.venv\Scripts\email-classifier prepare-dataset
.\.venv\Scripts\email-classifier train --allow-private --dataset "$privateDir\dataset.json" --model "$privateDir\baseline-private.joblib" --report "$privateDir\baseline-private-report.json"
```

`prepare-dataset` rejeita registros incluídos que não tenham as duas revisões,
rótulos válidos, cobertura de classes e isolamento de grupos. O dataset preparado
usa o contrato do baseline, com `source: gmail_reviewed`. Treinar com esse source exige
`--allow-private`; nesse modo, dataset, modelo e relatório devem estar fora do checkout
e de qualquer árvore Git detectável. Datasets sintéticos e reais não são misturados.

O treino continua usando só o split `train`. Use validação para decidir parâmetros e
thresholds; reserve o teste para a avaliação final. O comando atual gera métricas dos
três splits a cada execução: não use os números de teste para ajustar o modelo.
O relatório distingue origem sintética de privada. Uma amostra real pequena não
comprova qualidade, e este fluxo não calibra probabilidades automaticamente.

## 6. Simular previsões sem alterar o Gmail

Depois de coletar, já é possível testar o baseline sintético para diagnóstico:

```powershell
.\.venv\Scripts\email-classifier predict-batch --input "$privateDir\review.json" --model models/baseline.joblib
```

Ou, após revisão e treinamento, use `--model "$privateDir\baseline-private.joblib"`.
O arquivo `$privateDir\predictions.json` contém IDs locais e previsões, sem assunto/corpo;
o terminal mostra somente contagens. Escolha outro `--output` se ele já existir.
Previsões não substituem os rótulos humanos. Inferência usa somente arquivos locais,
não conecta ao Gmail e não aplica labels.

Não há comandos para enviar, excluir, arquivar, marcar lido ou alterar labels.
A habilitação de escrita e o uso automático continuam fora desta etapa.
