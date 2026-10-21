# Privacidade e Segurança

## Princípios

- minimização de dados;
- privilégio mínimo;
- credenciais fora do Git;
- ações reversíveis;
- logs sem conteúdo sensível;
- revisão humana em baixa confiança.

## Gmail

Tokens de acesso e refresh tokens são segredos e nunca devem aparecer no repositório.

## Dataset

Se e-mails reais forem utilizados para treinamento, o dataset deverá permanecer em armazenamento local ou privado apropriado, salvo quando estiver devidamente anonimizado e houver autorização para publicação.

## Logs

Evitar registrar corpo integral de mensagens. Preferir:

- ID interno;
- categoria prevista;
- confiança;
- ação tomada;
- versão do modelo;
- timestamp.

## Repositório público

Todo conteúdo versionado deve ser seguro para exposição pública.
