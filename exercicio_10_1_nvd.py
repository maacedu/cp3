import requests


BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def consultar_cve(cve):
    parametros = {
        "cveId": cve
    }

    try:
        resposta = requests.get(
            BASE_URL,
            params=parametros,
            timeout=30
        )

        if resposta.status_code == 404:
            print("CVE não encontrada.")
            return

        resposta.raise_for_status()

        dados = resposta.json()

        if dados.get("totalResults", 0) == 0:
            print("CVE não encontrada.")
            return

        vulnerabilidade = dados["vulnerabilities"][0]["cve"]

        print("\n================================")
        print("CVE:", vulnerabilidade["id"])
        print("================================")

        # Extrair a descrição em inglês.
        descricao = "Descrição indisponível."

        for item in vulnerabilidade.get("descriptions", []):
            if item.get("lang") == "en":
                descricao = item.get("value", descricao)
                break

        print("\nDescrição:")
        print(descricao)

        # Procurar pontuação CVSS.
        metricas = vulnerabilidade.get("metrics", {})

        chaves_cvss = [
            "cvssMetricV40",
            "cvssMetricV31",
            "cvssMetricV30",
            "cvssMetricV2"
        ]

        encontrado = False

        for chave in chaves_cvss:
            lista = metricas.get(chave, [])

            if lista:
                cvss = lista[0]["cvssData"]

                print("\nCVSS:", cvss.get("baseScore", "N/A"))
                print("Severidade:", cvss.get("baseSeverity", "N/A"))

                encontrado = True
                break

        if not encontrado:
            print("\nPontuação CVSS indisponível.")

    except requests.exceptions.Timeout:
        print("A consulta demorou demais. Tente novamente.")

    except requests.exceptions.ConnectionError:
        print("Não foi possível conectar ao NVD.")

    except requests.exceptions.HTTPError as erro:
        print("Erro HTTP:", erro)

    except (KeyError, IndexError, ValueError):
        print("A resposta da API veio em um formato inesperado.")


if __name__ == "__main__":
    cve = input("Digite uma CVE (ex: CVE-2021-44228): ").strip().upper()

    if not cve.startswith("CVE-"):
        print("Formato de CVE inválido.")
    else:
        consultar_cve(cve)