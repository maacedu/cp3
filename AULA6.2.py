
from flask import Flask, jsonify
import ipaddress

app = Flask(__name__)

# Lista de IPs bloqueados para o laboratorio
blacklist = {
    "185.220.101.1",
    "45.33.32.156",
    "91.240.118.172"
}


@app.route("/api/checar-ip/<ip>", methods=["GET"])
def checar_ip(ip):

    try:
        endereco = ipaddress.ip_address(ip)

    except ValueError:
        return jsonify({"erro": "IP invalido"}), 400

    resultado = {
        "ip": str(endereco),
        "na_blacklist": str(endereco) in blacklist,
        "tipo": "privado" if endereco.is_private else "publico"
    }

    return jsonify(resultado), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5003, debug=False)
