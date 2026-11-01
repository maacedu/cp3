# Aula 11 — Docker e automação via Python

## Objetivos

- Entender imagens e contêineres.
- Controlar o Docker com Python.
- Monitorar serviços.
- Automatizar deploy.
- Implementar watchdog.

## Tecnologias

- Python
- Docker Desktop
- Docker Engine
- Docker SDK for Python
- Requests
- Nginx
- Redis

## Arquivos

- exercicio_11_1_monitor.py
- exercicio_11_2_deploy.py
- exercicio_11_3_watchdog.py

## Exercício 11.1

Monitor de contêineres.

Lista todos os contêineres, apresenta nome, status,
imagem e quantidade de contêineres rodando ou parados.

## Exercício 11.2

Deploy automatizado.

Cria um contêiner Nginx na porta 8080,
verifica sua resposta HTTP e realiza a limpeza.

## Exercício 11.3

Watchdog.

Monitora o contêiner web_lab a cada 10 segundos
e tenta reiniciá-lo automaticamente quando necessário.

## Bibliotecas

- docker
- requests

## Conclusão

A aula demonstrou como automatizar operações
de infraestrutura utilizando Python e Docker.