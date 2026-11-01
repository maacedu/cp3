import os
import time
import ipaddress
import requests


URL_BASE = "https://ipinfo.io"

TOKEN = os.getenv("IPINFO_TOKEN")

sessao = requests.Session()

cache = {}

consultas_http = 0
cache_hits = 0
internos = 0


def consultar_ip(ip):
    global consultas_http

    for tentativa in range(3):

        try:
            parametros = {}

            if TOKEN:
                parametros["token"] = TOKEN

            resposta = sessao.get(
                f"{URL_BASE}/{ip}/json",
                params=parametros,
                timeout=15
            )

            consultas_http += 1

            if resposta.status_code == 429:
                retry = resposta.headers.get("Retry-After")

                if retry and retry.isdigit():
                    espera = int(retry)
                else:
                    espera = 2 ** tentativa

                if tentativa < 2:
                    print(
                        f"Rate limit. Aguardando {espera} segundos..."
                    )

                    time.sleep(min(espera, 60))
                    continue

                print("Limite de consultas atingido.")
                return None

            resposta.raise_for_status()

            return resposta.json()

        except requests.exceptions.Timeout:
            print("Timeout na consulta do IP.")
            return None

        except requests.exceptions.ConnectionError:
            print("Erro de conexão com IPinfo.")
            return None

        except requests.exceptions.HTTPError as erro:
            print("Erro HTTP:", erro)
            return None

    return None


def enriquecer_ip(valor):
    global cache_hits, internos

    try:
        endereco = ipaddress.ip_address(valor)

    except ValueError:
        print(f"{valor}: IP inválido.")
        return

    ip = str(endereco)

    print(f"\n{ip}")

    # Evita consultar IP privado, reservado ou local.
    if not endereco.is_global:
        internos += 1
        print("-> Rede interna ou endereço não global (não consultado)")
        return

    # Verifica se o resultado já está no cache.
    if ip in cache:
        cache_hits += 1
        dados = cache[ip]

        print("-> [CACHE] Resultado reutilizado.")
        exibir_dados(dados)
        return

    dados = consultar_ip(ip)

    if dados is None:
        print("-> Não foi possível obter informações.")
        return

    cache[ip] = dados

    exibir_dados(dados)


def exibir_dados(dados):
    cidade = dados.get("city", "Desconhecida")
    pais = dados.get("country", "Desconhecido")
    organizacao = dados.get("org", "Desconhecida")

    print("-> Cidade:", cidade)
    print("-> País:", pais)
    print("-> Organização:", organizacao)
    print("-> Classificação: EXTERNO")


def gerar_relatorio():
    ips = [
        "8.8.8.8",
        "1.1.1.1",
        "185.220.101.1",
        "192.168.1.10",
        "8.8.8.8"
    ]

    print("================================")
    print(" RELATÓRIO DE ENRIQUECIMENTO IP")
    print("================================")

    for ip in ips:
        enriquecer_ip(ip)

    print("\n================================")
    print(" RESUMO")
    print("================================")

    print("Consultas HTTP:", consultas_http)
    print("Cache hits:", cache_hits)
    print("Internos/não globais:", internos)


if __name__ == "__main__":
    gerar_relatorio()