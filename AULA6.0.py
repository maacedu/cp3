
from flask import Flask, jsonify, request

app = Flask(__name__)

usuarios = []
proximo_id = 1


def buscar_usuario(id):
    return next(
        (u for u in usuarios if u["id"] == id),
        None
    )


def email_existe(email, ignorar_id=None):
    return any(
        u["email"].lower() == email.lower()
        and u["id"] != ignorar_id
        for u in usuarios
    )


def validar_usuario(dados):
    if not isinstance(dados, dict):
        return "Envie um objeto JSON valido"

    nome = dados.get("nome")
    email = dados.get("email")
    nivel = dados.get("nivel")

    if not isinstance(nome, str) or not nome.strip():
        return "Nome obrigatorio"

    if not isinstance(email, str) or "@" not in email:
        return "Email invalido"

    if not isinstance(nivel, int) or isinstance(nivel, bool):
        return "Nivel deve ser um numero inteiro"

    if nivel < 1 or nivel > 5:
        return "Nivel invalido: use valores de 1 a 5"

    return None


# Listar usuarios
@app.route("/api/usuarios", methods=["GET"])
def listar_usuarios():
    return jsonify(usuarios), 200


# Buscar usuario
@app.route("/api/usuarios/<int:id>", methods=["GET"])
def obter_usuario(id):
    usuario = buscar_usuario(id)

    if usuario is None:
        return jsonify({"erro": "Usuario nao encontrado"}), 404

    return jsonify(usuario), 200


# Cadastrar usuario
@app.route("/api/usuarios", methods=["POST"])
def criar_usuario():
    global proximo_id

    dados = request.get_json(silent=True)

    erro = validar_usuario(dados)

    if erro:
        return jsonify({"erro": erro}), 400

    email = dados["email"].strip()

    if email_existe(email):
        return jsonify({"erro": "Email ja existe"}), 400

    usuario = {
        "id": proximo_id,
        "nome": dados["nome"].strip(),
        "email": email,
        "nivel": dados["nivel"]
    }

    usuarios.append(usuario)
    proximo_id += 1

    return jsonify(usuario), 201


# Atualizar usuario
@app.route("/api/usuarios/<int:id>", methods=["PUT"])
def atualizar_usuario(id):
    usuario = buscar_usuario(id)

    if usuario is None:
        return jsonify({"erro": "Usuario nao encontrado"}), 404

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict) or not dados:
        return jsonify({"erro": "Envie dados validos"}), 400

    if any(campo not in ("nome", "email", "nivel") for campo in dados):
        return jsonify({"erro": "Campo desconhecido"}), 400

    atualizado = {
        "nome": dados.get("nome", usuario["nome"]),
        "email": dados.get("email", usuario["email"]),
        "nivel": dados.get("nivel", usuario["nivel"])
    }

    erro = validar_usuario(atualizado)

    if erro:
        return jsonify({"erro": erro}), 400

    email = atualizado["email"].strip()

    if email_existe(email, ignorar_id=id):
        return jsonify({"erro": "Email ja existe"}), 400

    usuario.update({
        "nome": atualizado["nome"].strip(),
        "email": email,
        "nivel": atualizado["nivel"]
    })

    return jsonify(usuario), 200


# Excluir usuario
@app.route("/api/usuarios/<int:id>", methods=["DELETE"])
def deletar_usuario(id):
    global usuarios

    usuario = buscar_usuario(id)

    if usuario is None:
        return jsonify({"erro": "Usuario nao encontrado"}), 404

    usuarios = [u for u in usuarios if u["id"] != id]

    return jsonify({"mensagem": "Removido"}), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
