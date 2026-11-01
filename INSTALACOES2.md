# Registro de Instalações — Aula 2: MongoDB com PyMongo

**Aluno:** João Vitor Macedo Gondim  
**Projeto:** Aula 2 — MongoDB com PyMongo  
**Sistema operacional:** Windows  
**Editor:** Visual Studio Code

---

## 1. Programas instalados

| Programa | Finalidade | Status |
|---|---|---|
| Python | Executar os códigos | [ ] |
| Visual Studio Code | Desenvolver o projeto | [ ] |
| MongoDB Community Server | Banco de dados NoSQL | [ ] |
| MongoDB Compass | Interface gráfica para visualizar o banco | [ ] |
| PyMongo | Conectar Python ao MongoDB | [ ] |

## 2. Bibliotecas Python

| Biblioteca | Instalação | Status |
|---|---|---|
| PyMongo | `pip install pymongo` | [ ] |

## 3. Configurações realizadas

- [ ] Instalação do Python.
- [ ] Instalação do VS Code.
- [ ] Instalação do MongoDB Community Server.
- [ ] Configuração do MongoDB como serviço do Windows.
- [ ] Instalação do PyMongo.
- [ ] Criação do ambiente virtual `.venv`.
- [ ] Configuração da conexão local MongoDB.
- [ ] Teste de conexão com o banco de dados.

## 4. Comandos utilizados

### Criar ambiente virtual
```powershell
py -m venv .venv
```

### Ativar ambiente virtual
```powershell
.\.venv\Scripts\Activate.ps1
```

### Instalar PyMongo
```powershell
pip install pymongo
```

### Verificar instalação
```powershell
python -c "import pymongo; print(pymongo.version)"
```

### Verificar serviço MongoDB
```powershell
Get-Service MongoDB
```

### Testar conexão
```powershell
python -c "from pymongo import MongoClient; c=MongoClient('mongodb://localhost:27017/'); print(c.admin.command('ping'))"
```


## 5. Observações

Espaço para registrar problemas encontrados durante as instalações, configurações realizadas e soluções aplicadas.

________________________________________________

________________________________________________

________________________________________________

## 6. Conclusão

Registro das ferramentas e dependências necessárias para desenvolver os exercícios da Aula 2 — MongoDB com PyMongo.

**Status geral:** Em andamento.