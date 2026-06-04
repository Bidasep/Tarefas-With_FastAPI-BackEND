# 📋 API de Gerenciamento de Tarefas com FastAPI

API REST desenvolvida com FastAPI para gerenciamento de tarefas, utilizando SQLite para persistência dos dados, SQLAlchemy como ORM e autenticação HTTP Basic.

## 🚀 Tecnologias Utilizadas

* Python 3
* FastAPI
* Pydantic
* SQLAlchemy
* SQLite
* HTTP Basic Authentication
* Uvicorn

---

## 📌 Funcionalidades

* Adicionar tarefas
* Listar tarefas com paginação
* Atualizar tarefas
* Marcar tarefas como concluídas
* Remover tarefas
* Persistência em banco SQLite
* Autenticação HTTP Basic

---

## 📂 Estrutura da Tarefa

Cada tarefa possui os seguintes atributos:

| Campo            | Tipo    |
| ---------------- | ------- |
| id               | Integer |
| nome_tarefa      | String  |
| descricao_tarefa | String  |
| concluida        | Boolean |

---

## ⚙️ Instalação

### Clonar o repositório

bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git


### Acessar o diretório
bash
cd SEU-REPOSITORIO


### Instalar dependências com Poetry

bash
poetry install


### Ou utilizando pip

bash
pip install fastapi uvicorn sqlalchemy pydantic


---

## ▶️ Executando a Aplicação

Com FastAPI:

bash
fastapi dev app.py


Ou utilizando Uvicorn:
bash
uvicorn app:app --reload




## 🔐 Autenticação

A API utiliza autenticação HTTP Basic.

Credenciais padrão para testes:


Usuário: admin
Senha: admin




## 📬 Endpoints

### Listar Tarefas

```http
GET /tarefas
```

Parâmetros opcionais:

| Parâmetro | Tipo | Descrição               |
| --------- | ---- | ----------------------- |
| page      | int  | Página atual            |
| limit     | int  | Quantidade de registros |

Exemplo:

http
GET /tarefas?page=1&limit=10


---

### Adicionar Tarefa

http
POST /adiciona


Body:

json
{
    "nome_tarefa": "Aprender FastAPI",
    "descricao_tarefa": "Estudar CRUD e SQLAlchemy",
    "concluida": false
}


---

### Atualizar Tarefa

```http
PUT /atualiza/{id_tarefa}
```

Exemplo:

```http
PUT /atualiza/1
```

Body:

json
{
    "nome_tarefa": "Aprender FastAPI",
    "descricao_tarefa": "Estudar FastAPI e Banco de Dados",
    "concluida": false
}
```

---

### Concluir Tarefa

http
PUT /atualiza/{id_tarefa}/concluir


Exemplo:

http
PUT /atualiza/1/concluir


---

### Remover Tarefa

http
DELETE /delete/{id_tarefa}


Exemplo:

http
DELETE /delete/1


---

## 🗄️ Banco de Dados

A aplicação utiliza SQLite para armazenamento persistente.

Arquivo gerado automaticamente:

text
tarefas.db


As tabelas são criadas automaticamente pelo SQLAlchemy ao iniciar a aplicação.

---

## 📖 Documentação Interativa

Após iniciar a API, acesse:

Swagger UI:

text
http://localhost:8000/docs


ReDoc:

text
http://localhost:8000/redoc


---

## 📈 Próximas Melhorias

* Autenticação JWT
* Cadastro de usuários
* Hash de senhas com bcrypt
* Filtros de pesquisa
* Ordenação dinâmica
* Docker
* Testes automatizados
* PostgreSQL
* Deploy em nuvem

---

## 👨‍💻 Autor

Everton Felipe Silva de Jesus

Projeto desenvolvido para estudos de Backend com FastAPI, SQLAlchemy e SQLite.
