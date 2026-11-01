
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError
from pprint import pprint

# CONEXAO COM MONGODB
client = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=5000
)

db = client["seguranca"]
ativos = db["ativos"]

# TESTAR CONEXAO
try:
    client.admin.command("ping")
    print("Conectado ao MongoDB!")
except ServerSelectionTimeoutError:
    print("Erro: MongoDB nao esta funcionando.")
    raise SystemExit

# IMPEDIR IP DUPLICADO
ativos.create_index("ip", unique=True)

# DADOS INICIAIS
dados_iniciais = [
    {
        "nome": "SRV-WEB01",
        "tipo": "servidor",
        "ip": "192.168.1.10",
        "status": "ativo"
    },
    {
        "nome": "PC-RH03",
        "tipo": "estacao",
        "ip": "192.168.1.45",
        "status": "ativo"
    },
    {
        "nome": "SW-CORE01",
        "tipo": "switch",
        "ip": "192.168.1.1",
        "status": "inativo"
    }
]

# POPULAR BANCO SEM DUPLICAR OS DADOS
for ativo in dados_iniciais:
    ativos.update_one(
        {"ip": ativo["ip"]},
        {"$setOnInsert": ativo},
        upsert=True
    )


# 1. CADASTRAR ATIVO
def cadastrar():
    print("\n--- CADASTRAR ATIVO ---")

    nome = input("Nome: ")
    tipo = input("Tipo: ")
    ip = input("IP: ")

    novo_ativo = {
        "nome": nome,
        "tipo": tipo,
        "ip": ip,
        "status": "ativo"
    }

    try:
        ativos.insert_one(novo_ativo)
        print("Ativo cadastrado!")

    except DuplicateKeyError:
        print("Erro: IP ja cadastrado!")


# 2. LISTAR ATIVOS
def listar():
    print("\n--- LISTA DE ATIVOS ---")

    for ativo in ativos.find({}, {"_id": 0}):
        print("-----------------------")
        pprint(ativo)


# 3. BUSCAR POR IP
def buscar():
    print("\n--- BUSCAR ATIVO ---")

    ip = input("Digite o IP: ")

    ativo = ativos.find_one(
        {"ip": ip},
        {"_id": 0}
    )

    if ativo:
        pprint(ativo)
    else:
        print("Ativo nao encontrado!")


# 4. ATUALIZAR STATUS
def atualizar():
    print("\n--- ATUALIZAR STATUS ---")

    ip = input("Digite o IP: ")
    status = input("Novo status (ativo/inativo): ").lower()

    if status not in ["ativo", "inativo"]:
        print("Status invalido!")
        return

    resultado = ativos.update_one(
        {"ip": ip},
        {"$set": {"status": status}}
    )

    if resultado.matched_count > 0:
        print("Status atualizado!")
    else:
        print("Ativo nao encontrado!")


# 5. REMOVER ATIVO
def remover():
    print("\n--- REMOVER ATIVO ---")

    ip = input("Digite o IP: ")

    resultado = ativos.delete_one({"ip": ip})

    if resultado.deleted_count > 0:
        print("Ativo removido!")
    else:
        print("Ativo nao encontrado!")


# MENU PRINCIPAL
while True:

    print("\n==============================")
    print(" SISTEMA DE INVENTARIO")
    print("==============================")
    print("[1] Cadastrar ativo")
    print("[2] Listar ativos")
    print("[3] Buscar por IP")
    print("[4] Atualizar status")
    print("[5] Remover ativo")
    print("[6] Sair")

    opcao = input("Escolha uma opcao: ")

    if opcao == "1":
        cadastrar()

    elif opcao == "2":
        listar()

    elif opcao == "3":
        buscar()

    elif opcao == "4":
        atualizar()

    elif opcao == "5":
        remover()

    elif opcao == "6":
        print("Sistema encerrado!")
        break

    else:
        print("Opcao invalida!")

client.close()
