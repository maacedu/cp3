import docker
import requests
import time

from docker.errors import APIError, DockerException
from requests.exceptions import RequestException


NOME_CONTAINER = "nginx_deploy_aula11"
PORTA = 8080


def fazer_deploy():

    client = docker.from_env()
    container = None

    try:
        # Verifica se já existe um contêiner com esse nome.
        try:
            antigo = client.containers.get(NOME_CONTAINER)

            antigo.remove(force=True)

            print("Contêiner anterior removido.")

        except docker.errors.NotFound:
            pass

        print("Subindo Nginx...")

        container = client.containers.run(
            "nginx:latest",
            detach=True,
            name=NOME_CONTAINER,
            ports={"80/tcp": PORTA}
        )

        # Aguarda o Nginx ficar disponível.
        resposta = None

        for tentativa in range(15):

            time.sleep(2)

            try:
                resposta = requests.get(
                    f"http://localhost:{PORTA}",
                    timeout=3
                )

                if resposta.status_code == 200:
                    break

            except RequestException:
                continue

        if resposta is not None and resposta.status_code == 200:
            print("Nginx respondeu:", resposta.status_code, "OK")

        else:
            print("Nginx não respondeu corretamente.")

            if container:
                print(container.logs().decode(errors="replace")[-2000:])

    except APIError as erro:

        mensagem = str(erro).lower()

        if (
            "port is already allocated" in mensagem
            or "address already in use" in mensagem
            or "bind for" in mensagem
        ):
            print("Erro: porta 8080 em uso")

        else:
            print("Erro ao criar contêiner:", erro)

    except DockerException as erro:
        print("Erro de conexão com Docker:", erro)

    finally:

        if container is not None:

            print("Derrubando e removendo contêiner...")

            try:
                container.stop()
            except docker.errors.APIError:
                pass

            try:
                container.remove()
            except docker.errors.APIError:
                pass

            print("Concluído. Ambiente limpo.")

        client.close()


if __name__ == "__main__":
    fazer_deploy()