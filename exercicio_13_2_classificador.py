
from pathlib import Path
from collections import Counter

from seguranca_llm import analisar_log


# Logs de laboratório
logs = [
    "GET /index.html ip=192.168.1.10 status=200",
    "GET /../../etc/passwd ip=91.240.118.172 status=400",
    "POST /login ip=185.220.101.1 status=401 (5x seguidas)",
    "Failed login for admin from 185.220.101.1 - 50 attempts/min",
    "GET /sobre.html ip=192.168.1.20 status=200"
]

contagem = Counter()

relatorio = []

print("=== CLASSIFICADOR DE LOGS ===\n")

for log in logs:

    classificacao, motivo = analisar_log(log)

    contagem[classificacao] += 1

    linha = f"[{classificacao}] {log}"

    print(linha)
    print("Motivo:", motivo)
    print()

    relatorio.append(
        f"{linha}\nMotivo: {motivo}\n"
    )

# Resumo
resumo = (
    "\n=== RESUMO ===\n"
    f"NORMAL: {contagem['NORMAL']}\n"
    f"SUSPEITO: {contagem['SUSPEITO']}\n"
    f"CRITICO: {contagem['CRITICO']}\n"
)

print(resumo)

relatorio.append(resumo)

# Salva o relatório
pasta = Path("relatorios")
pasta.mkdir(exist_ok=True)

arquivo = pasta / "relatorio_logs.txt"

arquivo.write_text(
    "\n".join(relatorio),
    encoding="utf-8"
)

print("Relatório salvo em:", arquivo)
