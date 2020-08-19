# PDV (ponto de venda)

### Tecnologias
- [FastAPI](fastapi.tiangolo.com) - REST API Framework (Tem suporte para GraphQL)
- [SQLAlchemy](https://www.sqlalchemy.org/) - Abstração para fazer queries SQL
- [Pytest](https://docs.pytest.org/en/stable/) - biblioteca para implementar testes unitários
- Docker
- PostgreSQL

### Rodar o projeto

- Clone do repositório
- Instalar docker e docker-compose
- Rodar `docker-compose up db` para iniciar o PostgreSQL
- Rocker `docker-compose up dev` para iniciar o projecto em modo de desenvolvimento
- Rodar no terminal para adicionar um restaurante **(Rota implementada para auxilar no teste)**
```bash
curl - X POST "http://localhost:8000/api/v1/restaurant" - H  "accept: application/json" - H  "Content-Type: application/json" - d "{\"name\":\"Restaurante da esquina\",\"cnpj\":\"20050627000164\",\"owner\":\"Luiz Filipe\",\"phone\":\"32132132121\"}"
```
- Acessa em `http://localhost:8000/docs` e usar a API como solocitado

### Rotas da API
- `POST /api/v1/transacao` - Rota solicitada
- `GET /api/v1/transacoes/estabelecimento?cnpj=CNPJ` - Rota solicitada
- `GET /api/v1/healthcheck` - Rota adicional
- `POST /api/v1/restaurant` - Rota adicional

### Outros comandos

- Rodar `docker-compose up tests`
- Rodar `docker-compose up flake8` - Irá mostrar algo caso tiver algo a ser corrigido
- Para gerar o relatório da cobertura de teste precisa ser rodado na manualmente, mas é possível adicionar no docker-compose também. `pytest - -cov - report html - -cov = .` Após isso é só abrir no navegador o arquivo `htmlcov/index.html`.

### Decições
- Clientes não precisam estar adicionados previamente
- Clientes não precisavam ser adicionados em nenhum momento
- Restaurante já estaria adicionar, tanto que fiz uma rota para adicionar um e simular essa situação
- Tentei fazer o mais simples possível para mostrar conhecimento e não ter overengineering

### Melhorias
##### A primeira verão da API dado os requisitos estão OK, porém há melhorias na mesma, segue a lista:

- Garantir 100% de cobertura de teste.
- Melhorar os testes para usar fixture do pytest.
- Fazer validações a nível de [schema](https://github.com/vandaimer/payment-transactions/blob/master/payments/schemas.py).
- Organizar as mensagens de errors para padronizar as mesmas.
- CNPJ e CPF foram validados apenas em número de caracteres e formatação, mas dependo do caso é necessário fazer os calculos corretos para validar os mesmo.
- Criar um Dockerfile que não instale as dependencias de desenvolvimento.
- Criar uma entrada no docker-compose para gerar o relatório da cobertura de teste.
