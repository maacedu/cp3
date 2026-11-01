
from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import IntegrityError, Error
from getpass import getpass
import os

app = Flask(__name__)

# Configuracao do banco
# A senha sera lida por variavel de ambiente.
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "database": "seguranca",
    "connection_timeout": 3
}


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


def validar_usuario(dados, criacao=True):

    if not isinstance(dados, dict):
        return "Envie um objeto JSON valido"

    campos = ("nome", "email", "nivel_acesso")

    if criacao:
        for campo in ("nome", "email"):
            if campo not in dados:
                return f"Campo '{campo}' obrigatorio"

    if any(chave not in campos for chave in dados):
        return "Campo desconhecido"

    if "nome" in dados:
        if not isinstance(dados["nome"], str) or not dados["nome"].strip():
            return "Nome invalido"

    if "email" in dados:
        email = dados["email"]

        if not isinstance(email, str) or "@" not in email:
            return "Email invalido"

    if "nivel_acesso" in dados:
        nivel = dados["nivel_acesso"]

        if (
            not isinstance(nivel, int)
            or isinstance(nivel, bool)
            or nivel < 1
            or nivel > 5
        ):
            return "Nivel de acesso deve estar entre 1 e 5"

    return None


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensagem": "API de Usuarios MySQL",
        "status": "online"
    }), 200


# READ - Listar usuarios
@app.route("/api/usuarios", methods=["GET"])
def listar_usuarios():

    conexao = None
    cursor = None

    try:
        conexao = get_db()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, nome, email, nivel_acesso
            FROM usuarios
            ORDER BY id
            """
        )

        usuarios = cursor.fetchall()

        return jsonify(usuarios), 200

    except Error:
        return jsonify({"erro": "servico indisponivel"}), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None:
            conexao.close()


# READ - Buscar usuario por ID
@app.route("/api/usuarios/<int:id>", methods=["GET"])
def obter_usuario(id):

    conexao = None
    cursor = None

    try:
        conexao = get_db()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, nome, email, nivel_acesso
            FROM usuarios
            WHERE id = %s
            """,
            (id,)
        )

        usuario = cursor.fetchone()

        if usuario is None:
            return jsonify({"erro": "usuario nao encontrado"}), 404

        return jsonify(usuario), 200

    except Error:
        return jsonify({"erro": "servico indisponivel"}), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None:
            conexao.close()


# CREATE - Cadastrar usuario
@app.route("/api/usuarios", methods=["POST"])
def criar_usuario():

    dados = request.get_json(silent=True)

    erro = validar_usuario(dados)

    if erro:
        return jsonify({"erro": erro}), 400

    conexao = None
    cursor = None

    try:
        conexao = get_db()
        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO usuarios (nome, email, nivel_acesso)
            VALUES (%s, %s, %s)
            """,
            (
                dados["nome"].strip(),
                dados["email"].strip(),
                dados.get("nivel_acesso", 1)
            )
        )

        conexao.commit()

        return jsonify({
            "id": cursor.lastrowid,
            "mensagem": "Usuario criado"
        }), 201

    except IntegrityError:
        if conexao is not None:
            conexao.rollback()

        return jsonify({"erro": "email ja cadastrado"}), 409

    except Error:
        if conexao is not None:
            conexao.rollback()

        return jsonify({"erro": "servico indisponivel"}), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None:
            conexao.close()


# UPDATE - Atualizar usuario
@app.route("/api/usuarios/<int:id>", methods=["PUT"])
def atualizar_usuario(id):

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict) or not dados:
        return jsonify({"erro": "Envie dados JSON validos"}), 400

    erro = validar_usuario(dados, criacao=False)

    if erro:
        return jsonify({"erro": erro}), 400

    conexao = None
    cursor = None

    try:
        conexao = get_db()
        cursor = conexao.cursor()

        # Verificar se o usuario existe
        cursor.execute(
            "SELECT id FROM usuarios WHERE id = %s",
            (id,)
        )

        if cursor.fetchone() is None:
            return jsonify({"erro": "usuario nao encontrado"}), 404

        campos = []
        valores = []

        for campo in ("nome", "email", "nivel_acesso"):
            if campo in dados:
                valor = dados[campo]

                if campo in ("nome", "email"):
                    valor = valor.strip()

                campos.append(f"{campo} = %s")
                valores.append(valor)

        valores.append(id)

        comando = (
            "UPDATE usuarios SET "
            + ", ".join(campos)
            + " WHERE id = %s"
        )

        cursor.execute(comando, tuple(valores))
        conexao.commit()

        return jsonify({"mensagem": "Usuario atualizado"}), 200

    except IntegrityError:
        if conexao is not None:
            conexao.rollback()

        return jsonify({"erro": "email ja cadastrado"}), 409

    except Error:
        if conexao is not None:
            conexao.rollback()

        return jsonify({"erro": "servico indisponivel"}), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None:
            conexao.close()


# DELETE - Excluir usuario
@app.route("/api/usuarios/<int:id>", methods=["DELETE"])
def deletar_usuario(id):

    conexao = None
    cursor = None

    try:
        conexao = get_db()
        cursor = conexao.cursor()

        cursor.execute(
            "DELETE FROM usuarios WHERE id = %s",
            (id,)
        )

        if cursor.rowcount == 0:
            return jsonify({"erro": "usuario nao encontrado"}), 404

        conexao.commit()

        return jsonify({"mensagem": "Removido"}), 200

    except Error:
        if conexao is not None:
            conexao.rollback()

        return jsonify({"erro": "servico indisponivel"}), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None:
            conexao.close()


if __name__ == "__main__":

    if not DB_CONFIG["password"]:
        DB_CONFIG["password"] = getpass("Digite a senha do MySQL: ")

    app.run(host="127.0.0.1", port=5001, debug=False)
