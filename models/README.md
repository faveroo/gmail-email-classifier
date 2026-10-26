# Modelos locais

`email-classifier train` grava dois pipelines e sua política em `baseline.joblib`.
Artefatos são ignorados pelo Git. Carregar joblib pode executar código: use somente
arquivos de origem confiável. A versão do pacote e do scikit-learn deve coincidir;
caso contrário retreine. Não publicar modelos treinados com dados privados.
