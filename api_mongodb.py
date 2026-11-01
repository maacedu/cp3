
from flask import Flask, jsonify, request
from pymongo import MongoClient, DESCENDING
from pymongo.errors import PyMongoError
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime, timezone

app = Flask(__name__)

# Conexao com MongoDB
cliente = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=3000
)

db = cliente["seguranca"]
colecao = db["incidentes"]

SEVERIDADES = ("baixa", "media", "alta", "critica")
STATUS_VALIDOS = ("aberto", "em_analise", "resolvido")


# Converter ObjectId e datas para JSON
def serializar(documento):
    documento["_id"] = str(documento["_id"])

    if isinstance(documento.get("criado_em"), datetime):
        documento["criado_em"] = (
            documento["criado_em"]
            .isoformat()
        )

    return documento


# Validar campos de um incidente
def validar_incidente(dados, criacao=True):

    if not isinstance(dados, dict):
        return "Envie um objeto JSON valido"

    if criacao:
        obrigatorios = ("titulo", "severidade", "ip_origem")

        for campo in obrigatorios:
            if campo not in dados:
                return f"Campo '{campo}' obrigatorio"

    campos_permitidos = {
        "titulo",
        "severidade",
        "status",
        "ip_origem"
    }

    if any(campo not in campos_permitidos for campo in dados):
        return "Campo desconhecido"

    if "titulo" in dados:
        if not isinstance(dados["titulo"], str) or not dados["titulo"].strip():
            return "Titulo invalido"

    if "ip_origem" in dados:
        if not isinstance(dados["ip_origem"], str) or not dados["ip_origem"].strip():
            return "IP de origem invalido"

    if "severidade" in dados:
        if dados["severidade"] not in SEVERIDADES:
            return "Severidade invalida"

    if "status" in dados:
        if dados["status"] not in STATUS_VALIDOS:
            return "Status invalido"

    return None


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensagem": "API de Incidentes SecuraPy",
        "status": "online"
    }), 200


# CREATE - Cadastrar incidente
@app.route("/api/incidentes", methods=["POST"])
def criar_incidente():

    dados = request.get_json(silent=True)

    erro = validar_incidente(dados)

    if erro:
        return jsonify({"erro": erro}), 400

    incidente = {
        "titulo": dados["titulo"].strip(),
        "severidade": dados["severidade"],
        "status": dados.get("status", "aberto"),
        "ip_origem": dados["ip_origem"].strip(),
        "criado_em": datetime.now(timezone.utc)
    }

    try:
        resultado = colecao.insert_one(incidente)

        return jsonify({
            "id": str(resultado.inserted_id)
        }), 201

    except PyMongoError:
        return jsonify({"erro": "Servico de banco indisponivel"}), 500


# READ - Listar incidentes com filtros e paginacao
@app.route("/api/incidentes", methods=["GET"])
def listar_incidentes():

    try:
        pagina = request.args.get("pagina", default=1, type=int)
        tamanho = request.args.get("tamanho", default=10, type=int)

        if pagina is None or tamanho is None:
            return jsonify({"erro": "Paginacao invalida"}), 400

        if pagina < 1 or tamanho < 1 or tamanho > 100:
            return jsonify({
                "erro": "Pagina deve ser >= 1 e tamanho entre 1 e 100"
            }), 400

        filtro = {}

        severidade = request.args.get("severidade")
        status = request.args.get("status")

        if severidade:
            if severidade not in SEVERIDADES:
                return jsonify({"erro": "Severidade invalida"}), 400

            filtro["severidade"] = severidade

        if status:
            if status not in STATUS_VALIDOS:
                return jsonify({"erro": "Status invalido"}), 400

            filtro["status"] = status

        deslocamento = (pagina - 1) * tamanho

        cursor = (
            colecao.find(filtro)
            .sort("criado_em", DESCENDING)
            .skip(deslocamento)
            .limit(tamanho)
        )

        incidentes = [serializar(doc) for doc in cursor]

        total = colecao.count_documents(filtro)

        return jsonify({
            "pagina": pagina,
            "tamanho": tamanho,
            "total": total,
            "incidentes": incidentes
        }), 200

    except PyMongoError:
        return jsonify({"erro": "Servico de banco indisponivel"}), 500


# READ - Consultar um incidente
@app.route("/api/incidentes/<id>", methods=["GET"])
def obter_incidente(id):

    try:
        if not ObjectId.is_valid(id):
            return jsonify({"erro": "ID invalido"}), 400

        incidente = colecao.find_one({
            "_id": ObjectId(id)
        })

        if incidente is None:
            return jsonify({"erro": "Incidente nao encontrado"}), 404

        return jsonify(serializar(incidente)), 200

    except PyMongoError:
        return jsonify({"erro": "Servico de banco indisponivel"}), 500


# UPDATE - Atualizar incidente
@app.route("/api/incidentes/<id>", methods=["PUT"])
def atualizar_incidente(id):

    if not ObjectId.is_valid(id):
        return jsonify({"erro": "ID invalido"}), 400

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict) or not dados:
        return jsonify({"erro": "Envie dados JSON validos"}), 400

    erro = validar_incidente(dados, criacao=False)

    if erro:
        return jsonify({"erro": erro}), 400

    campos = {
        chave: (
            valor.strip()
            if chave in ("titulo", "ip_origem")
            else valor
        )
        for chave, valor in dados.items()
    }

    try:
        resultado = colecao.update_one(
            {"_id": ObjectId(id)},
            {"$set": campos}
        )

        if resultado.matched_count == 0:
            return jsonify({"erro": "Incidente nao encontrado"}), 404

        incidente = colecao.find_one({"_id": ObjectId(id)})

        return jsonify(serializar(incidente)), 200

    except PyMongoError:
        return jsonify({"erro": "Servico de banco indisponivel"}), 500


# DELETE - Excluir incidente
@app.route("/api/incidentes/<id>", methods=["DELETE"])
def deletar_incidente(id):

    if not ObjectId.is_valid(id):
        return jsonify({"erro": "ID invalido"}), 400

    try:
        resultado = colecao.delete_one({
            "_id": ObjectId(id)
        })

        if resultado.deleted_count == 0:
            return jsonify({"erro": "Incidente nao encontrado"}), 404

        return jsonify({"mensagem": "Removido"}), 200

    except PyMongoError:
        return jsonify({"erro": "Servico de banco indisponivel"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
