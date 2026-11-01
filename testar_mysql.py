
import requests

BASE = "http://127.0.0.1:5001"

print("===== TESTES DA API MYSQL =====")

# 1. Cadastrar usuario
dados = {
    "nome": "Usuario Aula 7",
    "email": "usuario.aula7@teste.com",
    "nivel_acesso": 3
}

resposta = requests.post(
    BASE + "/api/usuarios",
    json=dados
)

print("\n1. Cadastro:", resposta.status_code)
print(resposta.json())

if resposta.status_code == 201:
    id_usuario = resposta.json()["id"]

elif resposta.status_code == 409:
    print("Email ja cadastrado. Use outro email para repetir o teste.")
    raise SystemExit

else:
    raise SystemExit("Falha no cadastro. Confira o MySQL.")


# 2. Listar usuarios
resposta = requests.get(BASE + "/api/usuarios")

print("\n2. Listagem:", resposta.status_code)
print(resposta.json())


# 3. Buscar usuario
resposta = requests.get(
    BASE + f"/api/usuarios/{id_usuario}"
)

print("\n3. Consulta:", resposta.status_code)
print(resposta.json())


# 4. Atualizar usuario
resposta = requests.put(
    BASE + f"/api/usuarios/{id_usuario}",
    json={"nivel_acesso": 5}
)

print("\n4. Atualizacao:", resposta.status_code)
print(resposta.json())


# 5. Testar email duplicado
resposta = requests.post(
    BASE + "/api/usuarios",
    json={
        "nome": "Outro Usuario",
        "email": "usuario.aula7@teste.com",
        "nivel_acesso": 2
    }
)

print("\n5. Email duplicado:", resposta.status_code)
print(resposta.json())


# 6. Testar usuario inexistente
resposta = requests.get(
    BASE + "/api/usuarios/999999"
)

print("\n6. Usuario inexistente:", resposta.status_code)
print(resposta.json())


# 7. Excluir usuario
resposta = requests.delete(
    BASE + f"/api/usuarios/{id_usuario}"
)

print("\n7. Exclusao:", resposta.status_code)
print(resposta.json())


print("\n===== TESTES FINALIZADOS =====")
