
import requests

BASE = "http://127.0.0.1:5000"

print("===== TESTES DA API MONGODB =====")

# 1. Cadastrar incidente
dados = {
    "titulo": "Brute force SSH",
    "severidade": "alta",
    "ip_origem": "185.220.101.1"
}

resposta = requests.post(
    BASE + "/api/incidentes",
    json=dados
)

print("\n1. Cadastro:", resposta.status_code)
print(resposta.json())

if resposta.status_code != 201:
    raise SystemExit("Falha no cadastro. Confira o MongoDB.")

id_incidente = resposta.json()["id"]

# 2. Listar incidentes
resposta = requests.get(BASE + "/api/incidentes")

print("\n2. Listagem:", resposta.status_code)
print(resposta.json())

# 3. Buscar por ID
resposta = requests.get(
    BASE + f"/api/incidentes/{id_incidente}"
)

print("\n3. Consulta:", resposta.status_code)
print(resposta.json())

# 4. Atualizar
resposta = requests.put(
    BASE + f"/api/incidentes/{id_incidente}",
    json={"status": "resolvido"}
)

print("\n4. Atualizacao:", resposta.status_code)
print(resposta.json())

# 5. Filtrar criticos
resposta = requests.get(
    BASE + "/api/incidentes",
    params={"severidade": "critica", "tamanho": 5}
)

print("\n5. Filtro:", resposta.status_code)
print(resposta.json())

# 6. Testar ID invalido
resposta = requests.get(
    BASE + "/api/incidentes/id_invalido"
)

print("\n6. ID invalido:", resposta.status_code)
print(resposta.json())

# 7. Excluir
resposta = requests.delete(
    BASE + f"/api/incidentes/{id_incidente}"
)

print("\n7. Exclusao:", resposta.status_code)
print(resposta.json())

print("\n===== TESTES FINALIZADOS =====")
