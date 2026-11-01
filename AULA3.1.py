
import mysql.connector
from mysql.connector import Error
from getpass import getpass

# =====================================
# CONEXAO
# =====================================

senha = getpass("Senha do MySQL: ")

try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password=senha
    )

    cursor = conexao.cursor()

    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS seguranca"
    )

    cursor.execute("USE seguranca")

    print("Conectado ao MySQL!")

except Error as erro:
    print("Erro:", erro)
    raise SystemExit


# =====================================
# CRIAR TABELA
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    nivel_acesso INT NOT NULL
)
""")

conexao.commit()


# =====================================
# INSERIR 3 USUARIOS DE TESTE
# =====================================

dados = [
    ("Carlos Silva", "carlos@empresa.com", 3),
    ("Ana Costa", "ana@empresa.com", 5),
    ("Bruno Lima", "bruno@empresa.com", 1)
]

for usuario in dados:

    cursor.execute("""
        INSERT INTO usuarios
        (nome, email, nivel_acesso)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE nome = nome
    """, usuario)

conexao.commit()


# =====================================
# BUSCA INSEGURA
# =====================================

def buscar_inseguro(nome):

    consulta = (
        "SELECT * FROM usuarios WHERE nome = '"
        + nome + "'"
    )

    cursor.execute(consulta)

    return cursor.fetchall()


# =====================================
# BUSCA SEGURA
# =====================================

def buscar_seguro(nome):

    consulta = """
        SELECT * FROM usuarios
        WHERE nome = %s
    """

    cursor.execute(consulta, (nome,))

    return cursor.fetchall()


# =====================================
# TESTE DE SQL INJECTION
# =====================================

entrada_maliciosa = "' OR '1'='1"

print("\n=== TESTE SQL INJECTION ===")

resultado_inseguro = buscar_inseguro(
    entrada_maliciosa
)

print(
    "[INSEGURO] entrada:",
    entrada_maliciosa,
    "->",
    len(resultado_inseguro),
    "usuarios retornados (VAZAMENTO!)"
)

resultado_seguro = buscar_seguro(
    entrada_maliciosa
)

print(
    "[SEGURO] entrada:",
    entrada_maliciosa,
    "->",
    len(resultado_seguro),
    "usuarios retornados (DEFESA OK)"
)

print("\nCONCLUSAO:")
print("A query parametrizada tratou a entrada como texto literal.")

cursor.close()
conexao.close()
