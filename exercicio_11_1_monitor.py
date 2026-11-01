import docker


def monitorar_containers():

    try:
        client = docker.from_env()

        containers = client.containers.list(all=True)

        print("\n==============================================")
        print("        MONITOR DE CONTÊINERES")
        print("==============================================")

        print(f"{'NOME':<20} {'STATUS':<12} {'IMAGEM':<25}")
        print("-" * 60)

        total = 0
        rodando = 0
        parados = 0

        for container in containers:

            # Atualiza as informações do contêiner.
            container.reload()

            nome = container.name
            status = container.status

            imagem = (
                container.image.tags[0]
                if container.image.tags
                else container.image.short_id
            )

            total += 1

            if status == "running":
                rodando += 1
                observacao = ""

            else:
                parados += 1
                observacao = "<- ALERTA: PARADO"

            print(
                f"{nome:<20} "
                f"{status:<12} "
                f"{imagem:<25} "
                f"{observacao}"
            )

        print("-" * 60)

        print(f"Total: {total}")
        print(f"Rodando: {rodando}")
        print(f"Parados: {parados}")

        client.close()

    except docker.errors.DockerException as erro:
        print("Não foi possível acessar o Docker.")
        print("Detalhes:", erro)


if __name__ == "__main__":
    monitorar_containers()