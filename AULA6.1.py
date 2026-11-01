
from flask import Flask, jsonify, request

app = Flask(__name__)


def verificar_senha(senha):
    criterios = {
        "tamanho_min": len(senha) >= 8,
        "maiuscula": any(c.isupper() for c in senha),
        "minuscula": any(c.islower() for c in senha),
        "numero": any(c.isdigit() for c in senha),
        "especial": any(not c.isalnum() for c in senha)
    }

    quantidade = sum(criterios.values())

    if quantidade == 5:
        forca = "Muito forte"
    elif quantidade == 4:
        forca = "Forte"
    elif quantidade == 3:
        forca = "Media"
    else:
        forca = "Fraca"

    return forca, criterios


@app.route("/api/analisar-senha", methods=["POST"])
def analisar_senha():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um JSON valido"}), 400

    if "senha" not in dados:
        return jsonify({
            "erro": "campo 'senha' obrigatorio"
        }), 400

    senha = dados["senha"]

    if not isinstance(senha, str) or not senha:
        return jsonify({"erro": "Senha invalida"}), 400

    forca, criterios = verificar_senha(senha)

    return jsonify({
        "forca": forca,
        "criterios": criterios
    }), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=False)
