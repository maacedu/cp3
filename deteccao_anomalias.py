
import numpy as np

from sklearn.ensemble import IsolationForest

# Dados:
# [requisicoes por minuto, conexoes simultaneas]

trafego = np.array([
    [100, 5],
    [120, 6],
    [110, 5],
    [105, 4],
    [50000, 500],
    [109, 5],
    [111, 6],
    [45000, 450],
])

# Criar detector de anomalias

detector = IsolationForest(
    contamination=0.25,
    random_state=42
)

# Treinar e identificar comportamentos

resultados = detector.fit_predict(trafego)

print("\n===== DETECCAO DE ANOMALIAS =====")

for i, (amostra, resultado) in enumerate(zip(trafego, resultados)):

    if resultado == -1:
        status = "ANOMALIA"
    else:
        status = "Normal"

    print(f"Amostra {i}: {amostra} -> {status}")
