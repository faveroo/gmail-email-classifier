# Testes

Execute `python -m pytest` após instalar `.[dev]`.
Cobertura de schema, duplicatas e grupos entre splits, isolamento do treino,
limites da política, vocabulário desconhecido, persistência, relatórios e CLI.
Não se exige acurácia em frases de treino nem se confunde desempenho sintético
com qualidade em mensagens reais. A CI executa testes e treino em Python 3.11 e 3.13.
