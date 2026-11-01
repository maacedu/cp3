
from pymongo import MongoClient
from datetime import datetime
from pathlib import Path

# CONEXAO COM MONGODB
client = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=5000
)

db = client["seguranca"]
eventos = db["eventos"]

client.admin.command("ping")
print("Conectado ao MongoDB!")

# LOCALIZAR ARQUIVO AUTH.LOG
arquivo = Path(__file__).with_name("auth.log")

if not arquivo.exists():
    print("Erro: arquivo auth.log nao encontrado!")
    client.close()
    raise SystemExit

# LISTA PARA ARMAZENAR OS DOCUMENTOS
documentos = []

# LER E TRANSFORMAR AS LINHAS
with open(arquivo, "r", encoding="utf-8") as f:

    for linha in f:

        partes = linha.strip().split()

        if len(partes) < 5:
            continue

        data_hora = partes[0] + " " + partes[1]
        tipo = partes[2]

        campos = {}

        for parte in partes[3:]:
            if "=" in parte:
                chave, valor = parte.split("=", 1)
                campos[chave] = valor

        if "ip" not in campos:
            continue

        documento = {
            "timestamp": datetime.strptime(
                data_hora,
                "%Y-%m-%d %H:%M:%S"
            ),
            "fonte": "auth",
            "tipo": tipo,
            "ip": campos["ip"],
            "detalhes": {
                "usuario": campos.get("usuario", "desconhecido")
            }
        }

        documentos.append(documento)

# INSERIR TODOS OS DOCUMENTOS
if documentos:
    resultado = eventos.insert_many(documentos)

    print("Total de eventos inseridos:", len(resultado.inserted_ids))
else:
    print("Nenhum evento valido encontrado.")

# PIPELINE DE AGREGACAO
pipeline = [
    {
        "$match": {
            "tipo": "FAIL"
        }
    },
    {
        "$group": {
            "_id": "$ip",
            "total": {
                "$sum": 1
            }
        }
    },
    {
        "$sort": {
            "total": -1
        }
    },
    {
        "$limit": 5
    }
]

# MOSTRAR TOP 5 IPS
print("\n=== Top IPs por falhas de login ===")

for resultado in eventos.aggregate(pipeline):
    print(
        f"{resultado['_id']} -> "
        f"{resultado['total']} falhas"
    )

client.close()
