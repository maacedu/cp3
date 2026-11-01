
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
        password=senha,
        database="seguranca"
    )

    cursor = conexao.cursor(dictionary=True)

    print("Conectado ao MySQL!")

except Error as erro:
    print("Erro:", erro)
    raise SystemExit


# =====================================
# CRIAR TABELA
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS alertas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50),
    descricao TEXT,
    ip_origem VARCHAR(45),
    severidade ENUM(
        'baixa', 'media', 'alta', 'critica'
    ),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conexao.commit()


# =====================================
# INSERIR 10 ALERTAS DE TESTE
# =====================================

dados = [
    ("BRUTE_FORCE", "Tentativas de senha", "185.220.101.1", "critica"),
    ("BRUTE_FORCE", "Ataque de login", "185.220.101.1", "critica"),
    ("BRUTE_FORCE", "Acesso suspeito", "185.220.101.1", "alta"),
    ("BRUTE_FORCE", "Tentativas repetidas", "185.220.101.1", "alta"),
    ("PORT_SCAN", "Varredura de portas", "45.33.32.156", "critica"),
    ("PORT_SCAN", "Portas abertas", "45.33.32.156", "alta"),
    ("PORT_SCAN", "Scan de rede", "45.33.32.156", "media"),
    ("XSS", "Script malicioso", "45.33.32.156", "alta"),
    ("XSS", "Tentativa de XSS", "192.168.1.50", "media"),
    ("SQLI", "Tentativa de SQL Injection", "10.0.0.5", "baixa")
]

# LIMPAR DADOS ANTIGOS DO EXERCICIO
cursor.execute("DELETE FROM alertas")

# INSERIR OS 10 REGISTROS
cursor.executemany("""
    INSERT INTO alertas
    (tipo, descricao, ip_origem, severidade)
    VALUES (%s, %s, %s, %s)
""", dados)

conexao.commit()

print("10 alertas inseridos com sucesso!")


# =====================================
# A) CONTAGEM POR SEVERIDADE
# =====================================

print("\n=== POR SEVERIDADE ===")

cursor.execute("""
    SELECT severidade, COUNT(*) AS total
    FROM alertas
    GROUP BY severidade
    ORDER BY FIELD(
        severidade,
        'critica', 'alta', 'media', 'baixa'
    )
""")

for linha in cursor.fetchall():
    print(f"{linha['severidade']}: {linha['total']}")


# =====================================
# B) CONTAGEM POR TIPO
# =====================================

print("\n=== POR TIPO ===")

cursor.execute("""
    SELECT tipo, COUNT(*) AS total
    FROM alertas
    GROUP BY tipo
    ORDER BY total DESC
""")

for linha in cursor.fetchall():
    print(f"{linha['tipo']}: {linha['total']}")


# =====================================
# C) TOP 5 IPS
# =====================================

print("\n=== TOP IPS DE ORIGEM ===")

cursor.execute("""
    SELECT ip_origem, COUNT(*) AS total
    FROM alertas
    GROUP BY ip_origem
    ORDER BY total DESC
    LIMIT 5
""")

for linha in cursor.fetchall():
    print(
        f"{linha['ip_origem']} -> "
        f"{linha['total']} alertas"
    )


cursor.close()
conexao.close()
