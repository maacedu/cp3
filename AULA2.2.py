
from pymongo import MongoClient
from datetime import datetime
from pprint import pprint

# CONEXAO COM MONGODB
client = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=5000
)

db = client["seguranca"]
eventos = db["eventos"]

client.admin.command("ping")
print("Conectado ao MongoDB!")


# FUNCAO DE CONSULTA
def consultar(fonte=None, tipo=None, ip=None, desde=None):

    # FILTRO INICIAL VAZIO
    filtro = {}

    # ADICIONAR FONTE
    if fonte is not None:
        filtro["fonte"] = fonte

    # ADICIONAR TIPO
    if tipo is not None:
        filtro["tipo"] = tipo

    # ADICIONAR IP
    if ip is not None:
        filtro["ip"] = ip

    # ADICIONAR DATA
    if desde is not None:
        filtro["timestamp"] = {
            "$gte": desde
        }

    # CONSULTAR E ORDENAR
    resultados = eventos.find(
        filtro,
        {"_id": 0}
    ).sort("timestamp", -1)

    return list(resultados)


# TESTE 1: FALHAS DE UM IP ESPECIFICO
print("\n=== FALHAS DO IP ===")

resultado = consultar(
    tipo="FAIL",
    ip="185.220.101.1"
)

for evento in resultado:
    pprint(evento)


# TESTE 2: TODOS OS EVENTOS AUTH
print("\n=== EVENTOS AUTH ===")

resultado = consultar(fonte="auth")

for evento in resultado:
    pprint(evento)


# TESTE 3: EVENTOS A PARTIR DE UMA DATA
print("\n=== EVENTOS A PARTIR DE 20/02/2025 ===")

resultado = consultar(
    desde=datetime(2025, 2, 20)
)

for evento in resultado:
    pprint(evento)


client.close()
