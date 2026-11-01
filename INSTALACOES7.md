
# Aula 07 — Flask com Bancos de Dados

## Objetivo

Integrar APIs Flask com MongoDB e MySQL,
permitindo persistencia de dados.

## Tecnologias utilizadas

- Python
- Flask
- MongoDB
- PyMongo
- MySQL
- MySQL Connector
- Requests

## Instalacao

Criar ambiente virtual:

    py -m venv .venv

Ativar ambiente:

    .\.venv\Scripts\Activate.ps1

Instalar dependencias:

    pip install -r requirements.txt

## Arquivos

- api_mongodb.py
- api_mysql.py
- popular_incidentes.py
- testar_mongodb.py
- testar_mysql.py

## MongoDB

Banco: seguranca

Colecao: incidentes

Funcionalidades:
- Cadastro de incidentes
- Consulta de incidentes
- Atualizacao de incidentes
- Exclusao de incidentes
- Paginacao
- Filtros
- Ordenacao
- Serializacao de ObjectId

## MySQL

Banco: seguranca

Tabela: usuarios

Funcionalidades:
- Cadastro de usuarios
- Consulta de usuarios
- Atualizacao de usuarios
- Exclusao de usuarios
- Queries parametrizadas
- Tratamento de erros
- Transacoes

## Portas

API MongoDB: 5000
API MySQL: 5001

## Conclusao

A aula demonstrou como integrar APIs Flask com
bancos de dados reais, permitindo armazenar,
consultar, atualizar e excluir informacoes
de forma persistente.
