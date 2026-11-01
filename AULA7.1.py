
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta

cliente = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=3000
)

db = cliente["seguranca"]
colecao = db["incidentes"]

dados = [
    ("Brute force SSH", "alta", "aberto", "185.220.101.1"),
    ("Tentativa de SQL Injection", "critica", "aberto", "45.33.32.156"),
    ("Varredura de portas", "media", "em_analise", "192.168.1.10"),
    ("Tentativa de phishing", "alta", "resolvido", "91.240.118.172"),
    ("Acesso suspeito", "critica", "aberto", "10.0.0.5"),
    ("Ataque XSS", "media", "resolvido", "192.168.1.20"),
    ("Login suspeito", "baixa", "aberto", "172.16.0.5"),
    ("Brute force FTP", "alta", "em_analise", "185.220.101.2"),
    ("DDoS detectado", "critica", "aberto", "45.33.32.10"),
    ("Malware identificado", "alta", "resolvido", "192.168.1.30"),
    ("Tentativa de acesso", "baixa", "aberto", "10.0.0.8"),
    ("Exploracao de vulnerabilidade", "critica", "em_analise", "91.240.118.10"),
    ("Scan de rede", "media", "aberto", "172.16.0.10"),
    ("Acesso administrativo suspeito", "alta", "aberto", "192.168.1.40"),
    ("Tentativa de invasao", "critica", "resolvido", "185.220.101.3")
]

try:
    # Limpa somente os dados de laboratorio desta colecao.
    colecao.delete_many({
        "origem_dados": "laboratorio_aula7"
    })

    agora = datetime.now(timezone.utc)

    documentos = []

    for i, item in enumerate(dados):
        titulo, severidade, status, ip = item

        documentos.append({
            "titulo": titulo,
            "severidade": severidade,
            "status": status,
            "ip_origem": ip,
            "criado_em": agora - timedelta(minutes=i),
            "origem_dados": "laboratorio_aula7"
        })

    resultado = colecao.insert_many(documentos)

    print(f"{len(resultado.inserted_ids)} incidentes inseridos!")

except Exception as erro:
    print("Nao foi possivel inserir os dados:", erro)

finally:
    cliente.close()
