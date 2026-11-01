
import mysql.connector
from mysql.connector import Error, IntegrityError
from getpass import getpass

# =====================================
# CONEXAO COM MYSQL
# =====================================

senha = getpass("Digite a senha do MySQL: ")

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
    print("Erro de conexao:", erro)
    raise SystemExit


# =====================================
# CRIAR TABELA
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    nivel_acesso INT NOT NULL,
    CHECK (nivel_acesso BETWEEN 1 AND 5)
)
""")

conexao.commit()


# =====================================
# DADOS INICIAIS
# =====================================

usuarios_iniciais = [
    ("Carlos Silva", "carlos@empresa.com", 3),
    ("Ana Costa", "ana@empresa.com", 5),
    ("Bruno Lima", "bruno@empresa.com", 1)
]

for usuario in usuarios_iniciais:
    try:
        cursor.execute("""
            INSERT INTO usuarios
            (nome, email, nivel_acesso)
            VALUES (%s, %s, %s)
        """, usuario)

    except IntegrityError:
        pass

conexao.commit()


# =====================================
# 1. CADASTRAR USUARIO
# =====================================

def cadastrar():

    nome = input("Nome: ")
    email = input("Email: ")

    try:
        nivel = int(input("Nivel de acesso (1 a 5): "))

        if nivel < 1 or nivel > 5:
            print("Erro: nivel deve estar entre 1 e 5!")
            return

        cursor.execute("""
            INSERT INTO usuarios
            (nome, email, nivel_acesso)
            VALUES (%s, %s, %s)
        """, (nome, email, nivel))

        conexao.commit()

        print("Usuario cadastrado!")

    except ValueError:
        print("Digite um nivel numerico!")

    except IntegrityError:
        conexao.rollback()
        print("Erro: email ja existe!")

    except Error as erro:
        conexao.rollback()
        print("Erro:", erro)


# =====================================
# 2. LISTAR USUARIOS
# =====================================

def listar():

    cursor.execute("""
        SELECT nome, email, nivel_acesso
        FROM usuarios
        ORDER BY id
    """)

    usuarios = cursor.fetchall()

    print("\n=== LISTA DE USUARIOS ===")

    for usuario in usuarios:
        print(
            f"{usuario[0]} | "
            f"{usuario[1]} | "
            f"nivel {usuario[2]}"
        )


# =====================================
# 3. BUSCAR POR EMAIL
# =====================================

def buscar():

    email = input("Digite o email: ")

    cursor.execute("""
        SELECT nome, email, nivel_acesso
        FROM usuarios
        WHERE email = %s
    """, (email,))

    usuario = cursor.fetchone()

    if usuario:
        print("\nUsuario encontrado:")
        print("Nome:", usuario[0])
        print("Email:", usuario[1])
        print("Nivel:", usuario[2])

    else:
        print("Usuario nao encontrado!")


# =====================================
# 4. ATUALIZAR NIVEL
# =====================================

def atualizar():

    email = input("Email do usuario: ")

    try:
        nivel = int(input("Novo nivel (1 a 5): "))

        if nivel < 1 or nivel > 5:
            print("Erro: nivel deve estar entre 1 e 5!")
            return

        cursor.execute("""
            UPDATE usuarios
            SET nivel_acesso = %s
            WHERE email = %s
        """, (nivel, email))

        conexao.commit()

        if cursor.rowcount > 0:
            print("Nivel atualizado!")
        else:
            print("Usuario nao encontrado!")

    except ValueError:
        print("Digite um nivel valido!")

    except Error as erro:
        conexao.rollback()
        print("Erro:", erro)


# =====================================
# 5. REMOVER USUARIO
# =====================================

def remover():

    email = input("Email do usuario: ")

    cursor.execute("""
        DELETE FROM usuarios
        WHERE email = %s
    """, (email,))

    conexao.commit()

    if cursor.rowcount > 0:
        print("Usuario removido!")
    else:
        print("Usuario nao encontrado!")


# =====================================
# MENU PRINCIPAL
# =====================================

while True:

    print("\n==========================")
    print(" SISTEMA DE USUARIOS")
    print("==========================")
    print("[1] Cadastrar usuario")
    print("[2] Listar usuarios")
    print("[3] Buscar por email")
    print("[4] Atualizar nivel")
    print("[5] Remover usuario")
    print("[6] Sair")

    opcao = input("Escolha: ")

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

cursor.close()
conexao.close()
