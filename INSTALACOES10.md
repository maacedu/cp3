# Aula 10 — APIs RESTful

## Objetivos

Consumir APIs externas, trabalhar com autenticação,
paginação, rate limiting e cache.

## Bibliotecas

- requests
- ipaddress
- json
- os
- time

## Exercícios

### 10.1 — NVD

Consulta vulnerabilidades CVE e apresenta descrição,
pontuação CVSS e severidade.

### 10.2 — GitHub

Busca usuários, lista repositórios, consulta detalhes
e salva os resultados em JSON.

### 10.3 — Enriquecimento de IPs

Consulta informações externas, identifica IPs
não globais, utiliza cache e trata rate limiting.

## Segurança

- Timeout nas requisições.
- Tokens por variável de ambiente.
- Tratamento de erros HTTP.
- Backoff para HTTP 429.
- Cache para reduzir chamadas externas.
- Evita enviar IPs privados ao serviço externo.

## Conclusão

Os exercícios demonstram como integrar aplicações
Python com APIs externas e utilizar informações
de threat intelligence em atividades de segurança.