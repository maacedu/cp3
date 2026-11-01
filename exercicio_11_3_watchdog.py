import docker
import time

from datetime import datetime


NOME_CONTAINER = "web_lab"

INTERVALO = 10
ITERACOES = 6


def horario_atual():
    return datetime.now().strftime("%H:%M:%S")


def iniciar_watchdog():

    try:
        client = docker.from_env()

        print("================================")
        print("        WATCHDOG DOCKER")
        print("================================")

        print("Monitorando:", NOME_CONTAINER)

        for i in range(ITERACOES):

            try:
                container = client.containers.get(NOME_CONTAINER)

                # Atualiza as informações.
                container.reload()

                status = container.status

                if status == "running":

                    print(
                        f"[{horario_atual()}] "
                        f"{NOME_CONTAINER}: running — OK"
                    )

                else:

                    print(
                        f"[{horario_atual()}] "
                        f"{NOME_CONTAINER}: {status} — "
                        "ALERTA! Tentando reiniciar..."
                    )

                    container.restart(timeout=10)

                    container.reload()

                    if container.status == "running":

                        print(
                            f"[{horario_atual()}] "
                            f"{NOME_CONTAINER} reiniciado com sucesso."
                        )

                    else:

                        print(
                            f"[{horario_atual()}] "
                            "Não foi possível confirmar a reinicialização."
                        )

            except docker.errors.NotFound:

                print(
                    f"[{horario_atual()}] "
                    f"ERRO: contêiner {NOME_CONTAINER} não encontrado."
                )

            except docker.errors.APIError as erro:

                print(
                    f"[{horario_atual()}] "
                    f"Erro na operação Docker: {erro}"
                )

            # Não espera depois da última verificação.
            if i < ITERACOES - 1:
                time.sleep(INTERVALO)

        print("\nMonitoramento finalizado.")

        client.close()

    except docker.errors.DockerException as erro:
        print("Não foi possível acessar o Docker:", erro)


if __name__ == "__main__":
    iniciar_watchdog()