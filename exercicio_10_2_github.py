import requests
import json
import time


BASE_URL = "https://api.github.com"

sessao = requests.Session()

sessao.headers.update({
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
})

resultados = {}


def requisitar(url, params=None):
    for tentativa in range(3):

        try:
            resposta = sessao.get(
                url,
                params=params,
                timeout=20
            )

            if resposta.status_code in (403, 429):
                restante = resposta.headers.get("X-RateLimit-Remaining")
                retry = resposta.headers.get("Retry-After")

                if restante == "0":
                    reset = resposta.headers.get("X-RateLimit-Reset")

                    if reset and reset.isdigit():
                        espera = max(1, int(reset) - int(time.time()))
                    else:
                        espera = 2 ** tentativa

                elif retry and retry.isdigit():
                    espera = int(retry)

                else:
                    espera = 2 ** tentativa

                if tentativa < 2:
                    print(f"Limite atingido. Aguardando {espera} segundos...")
                    time.sleep(min(espera, 60))
                    continue

            resposta.raise_for_status()
            return resposta.json()

        except requests.exceptions.Timeout:
            print("Tempo limite excedido.")

        except requests.exceptions.ConnectionError:
            print("Erro de conexão.")

        except requests.exceptions.HTTPError:
            if resposta.status_code in (403, 429):
                print("Limite de requisições do GitHub atingido.")
            elif resposta.status_code == 404:
                print("Recurso não encontrado.")
            else:
                print("Erro HTTP:", resposta.status_code)

            return None

    return None


def buscar_usuario():
    usuario = input("Nome do usuário GitHub: ").strip()

    if not usuario:
        print("Informe um usuário.")
        return

    dados = requisitar(f"{BASE_URL}/users/{usuario}")

    if dados is None:
        return

    perfil = {
        "login": dados.get("login"),
        "nome": dados.get("name"),
        "repos_publicos": dados.get("public_repos"),
        "seguidores": dados.get("followers"),
        "perfil": dados.get("html_url")
    }

    resultados["perfil"] = perfil

    print("\n=== Perfil:", usuario, "===")
    print("Nome:", perfil["nome"])
    print("Repos públicos:", perfil["repos_publicos"])
    print("Seguidores:", perfil["seguidores"])
    print("Perfil:", perfil["perfil"])


def listar_repositorios():
    usuario = input("Nome do usuário: ").strip()

    if not usuario:
        print("Informe um usuário.")
        return

    repositorios = []
    pagina = 1

    while True:
        dados = requisitar(
            f"{BASE_URL}/users/{usuario}/repos",
            params={
                "page": pagina,
                "per_page": 100,
                "sort": "updated"
            }
        )

        if dados is None:
            return

        if not dados:
            break

        repositorios.extend(dados)

        if len(dados) < 100:
            break

        pagina += 1

    resultados["repositorios"] = repositorios

    print("\n=== Repositórios:", usuario, "===")

    for i, repo in enumerate(repositorios, start=1):
        print(
            f"{i}. {repo['name']} | "
            f"Estrelas: {repo['stargazers_count']} | "
            f"Linguagem: {repo['language']}"
        )

    print("\nTotal:", len(repositorios))


def detalhar_repositorio():
    usuario = input("Dono do repositório: ").strip()
    repositorio = input("Nome do repositório: ").strip()

    if not usuario or not repositorio:
        print("Preencha os dois campos.")
        return

    dados = requisitar(
        f"{BASE_URL}/repos/{usuario}/{repositorio}"
    )

    if dados is None:
        return

    detalhes = {
        "nome": dados.get("name"),
        "descricao": dados.get("description"),
        "linguagem": dados.get("language"),
        "estrelas": dados.get("stargazers_count"),
        "forks": dados.get("forks_count"),
        "url": dados.get("html_url")
    }

    resultados["detalhe_repositorio"] = detalhes

    print("\n=== Detalhes do repositório ===")

    for chave, valor in detalhes.items():
        print(f"{chave}: {valor}")


def salvar_json():
    if not resultados:
        print("Nenhum resultado para salvar.")
        return

    nome = input("Nome do arquivo (ex: github_resultado.json): ").strip()

    if not nome:
        print("Nome inválido.")
        return

    if not nome.endswith(".json"):
        nome += ".json"

    with open(nome, "w", encoding="utf-8") as arquivo:
        json.dump(
            resultados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )

    print("Resultados salvos em:", nome)


def menu():
    while True:
        print("\n==============================")
        print(" EXPLORADOR DA API DO GITHUB")
        print("==============================")
        print("1 - Buscar usuário")
        print("2 - Listar repositórios")
        print("3 - Detalhar repositório")
        print("4 - Salvar resultados em JSON")
        print("0 - Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            buscar_usuario()

        elif opcao == "2":
            listar_repositorios()

        elif opcao == "3":
            detalhar_repositorio()

        elif opcao == "4":
            salvar_json()

        elif opcao == "0":
            print("Encerrando programa.")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()