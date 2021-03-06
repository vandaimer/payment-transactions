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
- Rodar `docker-compose up -d db` para iniciar o PostgreSQL
- Rocker `docker-compose up dev` para iniciar o projecto em modo de desenvolvimento
- Rodar no terminal para adicionar um restaurante **(Rota implementada para auxilar no teste)**
```bash
curl -X POST "http://localhost:8000/api/v1/restaurant"  -H  "accept: application/json" -H  "Content-Type: application/json" -d '{"name":"Restaurante da esquina","cnpj":"45283163000167","owner":"Luiz Filipe","phone":"32132132121"}'
```
- Para acessar a documentação da API, basta usar o seguinte link: `http://localhost:8000/docs`

### Rotas da API
- `POST /api/v1/transacao` - Rota solicitada - Exemplo de paylod

```json
{
	"estabelecimento": "45.283.163/0001-67",
	"cliente": "094.214.930-01",
	"valor": 1000.01,
	"descricao": "Almoço em restaurante chique pago via Shipay!"
}
```

- `GET /api/v1/transacoes/estabelecimento?cnpj=CNPJ` - Rota solicitada
- `GET /api/v1/healthcheck` - Rota adicional
- `POST /api/v1/restaurant` - Rota adicional - **Não há nenhuma validação nesta rota** - Examplo de payload

```json
{
	"name": "string",
	"cnpj": "45283163000167", # CNPJ precisa ser somente números
	"owner": "string",
	"phone": "string"
}
```

### Outros comandos

- Rodar `docker-compose up tests`
- Rodar `docker-compose up flake8` - Irá mostrar algo caso tiver algo a ser corrigido
- Rodar `docker-compose up coverage` - Irá gerar um relatório da cobertura de teste. Após isso é só abrir no navegador o arquivo `htmlcov/index.html`.

### Decisões
- Clientes não precisam estar adicionados previamente
- Clientes não precisavam ser adicionados em nenhum momento
- Restaurante já estaria adicionado, tanto que fiz uma rota para adicionar um e simular essa situação
- Chamei o estabaleciomento de **Restaurante**, mas poderia ser algo mais genérico
- Implementação simples, funcional e flexivél para extensão
- Os retornos de CPF and CNPJ não retornam formatados. Eu julgo como boa prática salvar somente os números e retonar somente números para cada frontend tratar como preferir. Obs: O retorno com a formatação poderia ser feito, mas decidi não implementar dada a justificativa anterior.

### Melhorias
##### A primeira verão da API dado os requisitos estão OK, porém há melhorias na mesma, segue a lista:

- Garantir 100% de cobertura de teste.
- Melhorar os testes para usar fixture do pytest.
- Fazer validações a nível de [schema](https://github.com/vandaimer/payment-transactions/blob/master/payments/schemas.py).
- Organizar as mensagens de errors para padronizar as mesmas.
- CNPJ e CPF foram validados apenas em número de caracteres e formatação, mas dependo do caso é necessário fazer os cálculos corretos para validar os mesmo.
- Criar um Dockerfile que não instale as dependencias de desenvolvimento.
- Criar uma entrada no docker-compose para gerar o relatório da cobertura de teste.
- Implementar migrations usando [sqlalchemy-migrate](https://pypi.org/project/sqlalchemy-migrate/)
- Adicionar mais logs em parte importantes do sistema. Essa lib parece interesante (https://github.com/Delgan/loguru)
