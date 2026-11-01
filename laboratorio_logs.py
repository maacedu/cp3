
from pymongo import MongoClient
from datetime import datetime

# CONEXAO
client = MongoClient("mongodb://localhost:27017/")
db = client["seguranca"]

eventos = db["laboratorio_eventos"]


# REGISTRAR EVENTO
def registrar_evento(
    colecao,
    tipo,
    ip,
    detalhes,
    severidade="INFO"
):
    return colecao.insert_one({
        "tipo": tipo,
        "ip": ip,
        "detalhes": detalhes,
        "severidade": severidade,
        "timestamp": datetime.now()
    })


# BUSCAR ALERTAS
def buscar_alertas(colecao, sev_min="WARNING"):

    ordem = {
        "INFO": 0,
        "WARNING": 1,
        "ERROR": 2,
        "CRITICAL": 3
    }

    niveis = [
        nome for nome, valor in ordem.items()
        if valor >= ordem[sev_min]
    ]

    return list(
        colecao.find({
            "severidade": {"$in": niveis}
        }).sort("timestamp", -1)
    )


# TESTANDO AS FUNCOES
registrar_evento(
    eventos,
    "LOGIN",
    "192.168.1.10",
    {"usuario": "admin"},
    "INFO"
)

registrar_evento(
    eventos,
    "ATAQUE",
    "185.220.101.1",
    {"tentativas": 10},
    "CRITICAL"
)

print("\n=== ALERTAS ENCONTRADOS ===")

for alerta in buscar_alertas(eventos):
    print(alerta)

client.close()
