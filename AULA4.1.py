
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# Respostas reais:
# 0 = normal
# 1 = ataque

y_verdadeiro = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]

# Respostas previstas pelo modelo

y_previsto = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

# Calcular matriz de confusao

matriz = confusion_matrix(y_verdadeiro, y_previsto)

# Calcular metricas

acuracia = accuracy_score(y_verdadeiro, y_previsto)

precisao = precision_score(y_verdadeiro, y_previsto, zero_division=0)

recall = recall_score(y_verdadeiro, y_previsto, zero_division=0)

f1 = f1_score(y_verdadeiro, y_previsto, zero_division=0)

# Mostrar resultados

print("\n===== MATRIZ DE CONFUSAO =====")
print(matriz)

print("\n===== METRICAS =====")

print(f"Acuracia: {acuracia:.2f}")
print(f"Precisao: {precisao:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-score: {f1:.2f}")

print("\n===== INTERPRETACAO =====")

print("O modelo acertou 90% das previsoes.")

print("Entretanto, deixou passar metade dos ataques reais.")

print("Por isso, o recall e muito importante na seguranca.")
