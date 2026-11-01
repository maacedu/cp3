
# Exercicio 1.3 — Decisao de Arquitetura com CAP

| Cenario | CP/AP | Justificativa |
|---|---|---|
| 1. Tabela de saldo bancario de clientes | CP | O saldo precisa ser consistente, evitando divergencias durante transferencias bancarias. |
| 2. Ingestao de 500 mil eventos de firewall por minuto | AP | A disponibilidade e essencial para receber grandes volumes de eventos, mesmo durante falhas de comunicacao. |
| 3. Cache de tokens de sessao de usuarios logados | AP | O sistema deve continuar disponivel para autenticar usuarios, tolerando pequenas inconsistencias temporarias. |
| 4. Registro de quem autorizou cada transferencia | CP | Os registros precisam manter consistencia e integridade para garantir auditorias confiaveis. |
| 5. Feed de indicadores de ameaca (IOCs) replicado em 5 regioes | AP | Os indicadores devem continuar disponiveis globalmente, mesmo que a sincronizacao entre regioes apresente atrasos. |

## Conclusao

O teorema CAP ajuda a escolher entre consistencia e disponibilidade em sistemas distribuidos durante falhas de comunicacao.
