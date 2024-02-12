# Task Manager

## Funcionamento

Esse é um projeto de uma API de uma lista de tarefas (to-do list).
Essa API fornece endpoints para operações de CRUD de usuários e tarefas.
Os usuários podem ser criados por qualquer pessoa, mas as operações sobre as tarefas exigem autenticação utilizando jwt.

Todas as rotas da API estão documentadas com swagger no endereço: `http://localhost:5000/swagger-ui`

## Solução adotada

A solução adotada utiliza as seguintes tecnologias:

- Python 3.10
- Flask
- Postgres
- Docker e Docker Compose

## Rodando o projeto

Crie um ambiente virtual:

```
$ python -m venv .venv
```

Ative esse ambiente:

```
$ source .venv/bin/activate
```

Instale as dependências do projeto:

```
$ pip install -r requirements.txt
```

Dentro da pasta taskmanager, crie o arquivo .flaskenv a partir do .flaskenv.example:

```
$ cp .flaskenv.example .flaskenv
```

Inicialize o banco de dados utilizando o docker compose:

```
$ docker compose up -d
```

Rode as migrations do projeto para criar as tabelas:

```
$ flask db upgrade
```

Inicie a API:

```
$ flask run
```