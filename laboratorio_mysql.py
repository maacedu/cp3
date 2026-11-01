
import mysql.connector
from mysql.connector import Error
from getpass import getpass

# CONEXAO
senha = getpass("Senha do MySQL: ")

try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password=senha,
        database="seguranca"
    )

    cursor = conexao.cursor(dictionary=True)

    print("Conectado ao MySQL!")

except Error as erro:
    print("Erro:", erro)
    raise SystemExit


# CRIAR TABELA DE EVENTOS
cursor.execute("""
CREATE TABLE IF NOT EXISTS eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50),
    ip VARCHAR(45),
    descricao TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conexao.commit()


# FUNCAO PARA REGISTRAR EVENTOS
def registrar_evento(tipo, ip, descricao):

    try:
        cursor.execute("""
            INSERT INTO eventos
            (tipo, ip, descricao)
            VALUES (%s, %s, %s)
        """, (tipo, ip, descricao))

        conexao.commit()

        print("Evento registrado!")

    except Error as erro:
        conexao.rollback()
        print("Erro ao registrar:", erro)


# REGISTRANDO EVENTOS
registrar_evento(
    "LOGIN",
    "192.168.1.10",
    "Login realizado com sucesso"
)

registrar_evento(
    "BRUTE_FORCE",
    "185.220.101.1",
    "Multiplas tentativas de senha"
)


# CONSULTAR EVENTOS
print("\n=== EVENTOS REGISTRADOS ===")

cursor.execute("""
    SELECT * FROM eventos
    ORDER BY criado_em DESC
""")

for evento in cursor.fetchall():
    print(
        evento["tipo"],
        "|",
        evento["ip"],
        "|",
        evento["descricao"]
    )


# DEMONSTRACAO DE ROLLBACK
print("\n=== TESTE DE ROLLBACK ===")

try:
    cursor.execute("""
        INSERT INTO eventos
        (tipo, ip, descricao)
        VALUES (%s, %s, %s)
    """, (
        "TESTE",
        "127.0.0.1",
        "Este registro sera cancelado"
    ))

    # DESFAZ A INSERCAO
    conexao.rollback()

    print("Operacao desfeita com rollback!")

except Error as erro:
    conexao.rollback()
    print("Erro:", erro)


cursor.close()
conexao.close()

print("\nConexao encerrada!")
