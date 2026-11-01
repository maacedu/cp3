
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# 1. Características do tráfego:
# [bytes transferidos, porta de destino, duração em segundos]

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
])

# 2. Respostas:
# 0 = normal
# 1 = malicioso

y = np.array([0, 0, 0, 1, 1, 1, 0, 0, 1, 0])

# 3. Separar os dados para treinamento e teste

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)

# 4. Criar o modelo

modelo = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# 5. Treinar

modelo.fit(X_train, y_train)

# 6. Fazer previsões

previsoes = modelo.predict(X_test)

# 7. Avaliar o modelo

print("\n===== RESULTADOS DO MODELO =====")

print("Acurácia:", accuracy_score(y_test, previsoes))

print("\nRelatório de classificação:")
print(classification_report(y_test, previsoes, zero_division=0))

print("\nMatriz de confusão:")
print(confusion_matrix(y_test, previsoes))

# 8. Testar uma nova conexão

novo_trafego = [[58000, 4444, 16.0]]

resultado = modelo.predict(novo_trafego)[0]

print("\n===== NOVA CONEXÃO =====")

if resultado == 1:
    print("ALERTA: tráfego potencialmente malicioso!")
else:
    print("Tráfego classificado como normal.")
