
import hashlib
from pathlib import Path

import joblib
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score

# ---------------------------------
# 1. Dados de treinamento
# ---------------------------------

X = np.array([
    [500, 80, 0.1],
    [1200, 80, 0.5],
    [64, 22, 0.02],
    [64000, 4444, 10.0],
    [45000, 8080, 15.0],
    [60000, 31337, 20.0],
    [800, 443, 0.3],
    [300, 53, 0.05],
    [55000, 9999, 18.0],
    [200, 25, 0.2],
    [700, 443, 0.2],
    [52000, 6666, 17.0],
    [150, 53, 0.03],
    [58000, 4444, 19.0],
    [900, 80, 0.4],
])

y = np.array([
    0, 0, 0, 1, 1,
    1, 0, 0, 1, 0,
    0, 1, 0, 1, 0
])

# ---------------------------------
# 2. Comparação dos algoritmos
# ---------------------------------

modelos = {
    "RandomForest": RandomForestClassifier(random_state=42),
    "SVM": SVC(),
    "KNN": KNeighborsClassifier()
}

pipelines = {}
resultados = {}

for nome, classificador in modelos.items():

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", classificador)
    ])

    scores = cross_val_score(
        pipeline, X, y, cv=5, scoring="accuracy"
    )

    pipelines[nome] = pipeline
    resultados[nome] = scores.mean()

    print(f"{nome}: {scores.mean():.3f}")

vencedor = max(resultados, key=resultados.get)
print(f"\nVencedor: {vencedor}")

# ---------------------------------
# 3. GridSearch do vencedor
# ---------------------------------

grades = {
    "RandomForest": {
        "clf__n_estimators": [50, 100, 200],
        "clf__max_depth": [None, 5, 10]
    },
    "SVM": {
        "clf__C": [0.1, 1, 10],
        "clf__kernel": ["linear", "rbf"]
    },
    "KNN": {
        "clf__n_neighbors": [3, 5, 7],
        "clf__weights": ["uniform", "distance"]
    }
}

busca = GridSearchCV(
    pipelines[vencedor],
    grades[vencedor],
    cv=5,
    scoring="accuracy"
)

busca.fit(X, y)

melhor_modelo = busca.best_estimator_

print(f"Melhores parâmetros: {busca.best_params_}")
print(f"Melhor score: {busca.best_score_:.3f}")

# ---------------------------------
# 4. Preparação dos arquivos
# ---------------------------------

pasta_modelos = Path("modelos")
pasta_modelos.mkdir(exist_ok=True)

arquivo_modelo = pasta_modelos / "modelo_seguranca.pkl"
arquivo_hash = pasta_modelos / "modelo_seguranca.sha256"

# ---------------------------------
# 5. Função para calcular SHA-256
# ---------------------------------

def calcular_hash(caminho):

    sha256 = hashlib.sha256()

    with open(caminho, "rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(4096), b""):
            sha256.update(bloco)

    return sha256.hexdigest()

# ---------------------------------
# 6. Salvar modelo e hash
# ---------------------------------

joblib.dump(melhor_modelo, arquivo_modelo)

hash_original = calcular_hash(arquivo_modelo)

arquivo_hash.write_text(
    hash_original,
    encoding="utf-8"
)

print("\nModelo salvo:", arquivo_modelo)
print("Hash SHA-256:", hash_original)

# ---------------------------------
# 7. Verificar antes de carregar
# ---------------------------------

print("\nRecarregando e verificando integridade...")

hash_armazenado = arquivo_hash.read_text(
    encoding="utf-8"
).strip()

hash_atual = calcular_hash(arquivo_modelo)

if hash_atual == hash_armazenado:

    print("Hash confere: modelo íntegro.")

    # Só carregamos depois da verificação
    modelo_carregado = joblib.load(arquivo_modelo)

    # Nova conexão para classificação
    novo_trafego = np.array([
        [60000, 8080, 12.0]
    ])

    previsao = modelo_carregado.predict(novo_trafego)

    print("Previsão de teste:", previsao)

else:

    print("ALERTA: arquivo do modelo foi modificado!")
    print("O modelo não será carregado.")
