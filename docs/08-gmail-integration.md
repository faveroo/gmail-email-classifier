# Integração com Gmail

## Objetivo

Usar a Gmail API oficial para ler mensagens necessárias à classificação e aplicar labels autorizadas.

## Autenticação

OAuth 2.0.

Nenhuma credencial deverá ser versionada no repositório.

## Permissões

A aplicação deverá solicitar somente os escopos estritamente necessários.

## Fluxo futuro

1. autenticar usuário;
2. buscar mensagens candidatas;
3. extrair remetente, assunto e corpo;
4. normalizar conteúdo;
5. executar classificadores;
6. aplicar política de confiança;
7. adicionar label apropriada;
8. registrar resultado sem armazenar conteúdo sensível desnecessariamente.

## Segurança operacional

Na fase inicial, não:

- excluir mensagens;
- marcar diretamente como spam oficial;
- remover labels existentes;
- arquivar automaticamente mensagens importantes.

Preferir labels `IA/*`, que tornam as decisões reversíveis e auditáveis.
