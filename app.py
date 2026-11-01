
from flask import Flask, jsonify, request

app = Flask(__name__)

# Banco de dados temporario em memoria
alertas = []
proximo_id = 1

SEVERIDADES = ("baixa", "media", "alta", "critica")


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensagem": "API de Seguranca SecuraPy",
        "status": "online",
        "versao": "1.0"
    }), 200


# READ - Listar alertas
@app.route("/api/alertas", methods=["GET"])
def listar_alertas():
    return jsonify(alertas), 200


# READ - Buscar alerta por ID
@app.route("/api/alertas/<int:id>", methods=["GET"])
def obter_alerta(id):
    alerta = next(
        (a for a in alertas if a["id"] == id),
        None
    )

    if alerta is None:
        return jsonify({"erro": "Alerta nao encontrado"}), 404

    return jsonify(alerta), 200


# CREATE - Criar alerta
@app.route("/api/alertas", methods=["POST"])
def criar_alerta():
    global proximo_id

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um objeto JSON valido"}), 400

    if "tipo" not in dados or "severidade" not in dados:
        return jsonify({
            "erro": "Campos tipo e severidade sao obrigatorios"
        }), 400

    tipo = dados["tipo"]
    severidade = dados["severidade"]
    descricao = dados.get("descricao", "")

    if not isinstance(tipo, str) or not tipo.strip():
        return jsonify({"erro": "Tipo invalido"}), 400

    if not isinstance(descricao, str):
        return jsonify({"erro": "Descricao invalida"}), 400

    if severidade not in SEVERIDADES:
        return jsonify({"erro": "Severidade invalida"}), 400

    alerta = {
        "id": proximo_id,
        "tipo": tipo.strip(),
        "descricao": descricao,
        "severidade": severidade
    }

    alertas.append(alerta)
    proximo_id += 1

    return jsonify(alerta), 201


# UPDATE - Atualizar alerta
@app.route("/api/alertas/<int:id>", methods=["PUT"])
def atualizar_alerta(id):
    alerta = next(
        (a for a in alertas if a["id"] == id),
        None
    )

    if alerta is None:
        return jsonify({"erro": "Alerta nao encontrado"}), 404

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict) or not dados:
        return jsonify({"erro": "Envie dados validos"}), 400

    campos = ("tipo", "descricao", "severidade")

    if any(chave not in campos for chave in dados):
        return jsonify({"erro": "Campo desconhecido"}), 400

    novo_tipo = dados.get("tipo", alerta["tipo"])
    nova_descricao = dados.get("descricao", alerta["descricao"])
    nova_severidade = dados.get("severidade", alerta["severidade"])

    if not isinstance(novo_tipo, str) or not novo_tipo.strip():
        return jsonify({"erro": "Tipo invalido"}), 400

    if not isinstance(nova_descricao, str):
        return jsonify({"erro": "Descricao invalida"}), 400

    if nova_severidade not in SEVERIDADES:
        return jsonify({"erro": "Severidade invalida"}), 400

    alerta.update({
        "tipo": novo_tipo.strip(),
        "descricao": nova_descricao,
        "severidade": nova_severidade
    })

    return jsonify(alerta), 200


# DELETE - Excluir alerta
@app.route("/api/alertas/<int:id>", methods=["DELETE"])
def deletar_alerta(id):
    global alertas

    alerta = next(
        (a for a in alertas if a["id"] == id),
        None
    )

    if alerta is None:
        return jsonify({"erro": "Alerta nao encontrado"}), 404

    alertas = [a for a in alertas if a["id"] != id]

    return jsonify({"mensagem": "Removido"}), 200


# Tratamento de rotas inexistentes
@app.errorhandler(404)
def rota_nao_encontrada(erro):
    return jsonify({"erro": "Rota nao existe"}), 404


if __name__ == "__main__":
    # Servidor local para laboratorio.
    # Nao disponibilize o servidor de desenvolvimento na internet.
    app.run(host="127.0.0.1", port=5000, debug=False)
