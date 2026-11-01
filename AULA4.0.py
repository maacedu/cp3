
import numpy as np

from sklearn.ensemble import IsolationForest

# Features:
# [hora do dia, tentativas de login, bytes baixados]

acessos = np.array([
    [9, 1, 200],
    [10, 1, 500],
    [14, 2, 300],
    [11, 1, 250],
    [16, 1, 400],
    [3, 40, 900000],
    [10, 1, 350],
    [15, 2, 280],
    [2, 55, 800000],
])

# Criar detector

detector = IsolationForest(
    contamination=0.25,
    random_state=42
)

# Treinar e detectar

resultados = detector.fit_predict(acessos)

print("\n===== ACESSOS ANALISADOS =====")

for i, (amostra, resultado) in enumerate(zip(acessos, resultados)):

    if resultado == -1:
        print(f"Amostra {i}: {amostra} -> ANOMALIA")
    else:
        print(f"Amostra {i}: {amostra} -> Normal")
