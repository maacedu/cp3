
import requests

BASE_URL = "http://127.0.0.1:5000"

print("\n===== TESTANDO API SECURAPY =====")

# 1. Testar inicio
resposta = requests.get(BASE_URL + "/")

print("\n1. Inicio:")
print("Status:", resposta.status_code)
print(resposta.json())

# 2. Criar alerta
dados = {
    "tipo": "BRUTE_FORCE",
    "descricao": "10 tentativas de login",
    "severidade": "critica"
}

resposta = requests.post(
    BASE_URL + "/api/alertas",
    json=dados
)

print("\n2. Criar alerta:")
print("Status:", resposta.status_code)
print(resposta.json())

# 3. Listar alertas
resposta = requests.get(BASE_URL + "/api/alertas")

print("\n3. Listar alertas:")
print("Status:", resposta.status_code)
print(resposta.json())

# 4. Buscar alerta
resposta = requests.get(BASE_URL + "/api/alertas/1")

print("\n4. Buscar alerta:")
print("Status:", resposta.status_code)
print(resposta.json())

# 5. Atualizar alerta
dados_atualizados = {
    "severidade": "alta",
    "descricao": "Alerta atualizado"
}

resposta = requests.put(
    BASE_URL + "/api/alertas/1",
    json=dados_atualizados
)

print("\n5. Atualizar alerta:")
print("Status:", resposta.status_code)
print(resposta.json())

# 6. Testar entrada invalida
resposta = requests.post(
    BASE_URL + "/api/alertas",
    json={
        "tipo": "XSS",
        "severidade": "urgente"
    }
)

print("\n6. Testar severidade invalida:")
print("Status:", resposta.status_code)
print(resposta.json())

# 7. Excluir alerta
resposta = requests.delete(
    BASE_URL + "/api/alertas/1"
)

print("\n7. Excluir alerta:")
print("Status:", resposta.status_code)
print(resposta.json())

print("\n===== TESTES FINALIZADOS =====")
