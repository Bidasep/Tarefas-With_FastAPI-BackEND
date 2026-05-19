#Objetivo
#Crie uma aplicação simples utilizando FastAPI para gerenciar um conjunto de tarefas. A aplicação deve permitir as seguintes operações:

#Adicionar uma nova tarefa com um nome e uma descrição.

#Listar todas as tarefas cadastradas.

#Marcar uma tarefa como concluída.

#Remover uma tarefa.

#Passo a Passo:
#Criação da Aplicação FastAPI
#Crie um arquivo Python chamado app.py e inicialize a aplicação FastAPI. Para isso, importe a classe FastAPI e crie uma instância da aplicação.

#Definindo uma Lista de Tarefas
#Crie uma lista de dicionários para armazenar as tarefas. Cada tarefa será representada como um dicionário com os campos "nome", "descrição" e "concluída" (inicialmente como False).

#Rota para Adicionar uma Tarefa
#Crie uma rota do tipo POST que permita adicionar uma nova tarefa. A rota deverá receber um corpo JSON com os campos "nome" e "descrição" e adicionar a tarefa à lista.

#rota para Listar as Tarefas
#Crie uma rota do tipo GET que exiba todas as tarefas. A resposta deve incluir o nome, a descrição e se a tarefa foi concluída ou não.

#Rota para Marcar uma Tarefa como Concluída
#Crie uma rota do tipo PUT que permita marcar uma tarefa como concluída. Para isso, a rota deve receber o nome da tarefa e alterar o valor do campo "concluída" para True se a tarefa existir.

#Rota para Remover uma Tarefa
#Crie uma rota do tipo DELETE que permita remover uma tarefa da lista. A rota deve receber o nome da tarefa e removê-la da lista se existir.

#Testando a Aplicação
#Após implementar as rotas, utilize o Insomnia ou Postman para testar as funcionalidades. Envie requisições POST para adicionar tarefas, GET para listar, PUT para marcar tarefas como concluídas e DELETE para remover tarefas.#

# 1 INSTALAR PACOTES E DEPENDENCIAS:
#1 - poetry init -> NOME DO PROJETO (sem espaços)
#2 - poetry shell -> iniciar o gerenciador de dependencias
#3 - para iniciar o servidor virtual : poetry add fastapi[standard]
#4 - em seguida fastapi dev "main.py" main sem aspas, é o nome do arquivo principal.
#INSTALANDO O SQL LITE
#poetry add sqlalchemy aiosqlite  //  SÃO DOIS ARQUIVOS ALCHEMY E SQLITE

#após podemos inicar o projeto

# 2 - importar as bibliotecas API, banco de dados
from fastapi import FastAPI, HTTPException,Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets

from sqlalchemy import create_engine,Column, Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

#3 -  iniciar nosso banco de dados e criar.
DATABASE_URL = "sqlite:///./tarefas.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread" : False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

minhas_tarefas = {}

#classes de referencia e classe do Banco de dados como será o nosso arquivo
#Definindo uma Lista de Tarefas

class TarefaDB(Base):
    __tablename__ = "tarefas"
    id =Column(Integer, primary_key = True, index = True)
    nome_tarefa= Column(String, index = True)
    descricao_tarefa = Column(String, index = True)
    concluida = False
    
class Tarefa(BaseModel):
    nome_tarefa: str
    descricao_tarefa: str
    concluida: bool   
    
Base.metadata.create_all(bind=engine)


#sessão para iniciar o BD sempre que for fazer algo nele
def sessao_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#4 - iniciar a variavel da fastAPI
app = FastAPI()




# Rotas e endpoints

#Rota para Adicionar uma Tarefa
@app.get("/tarefas")
def get_tarefas(page: int=1, limit: int = 10, db: Session = Depends(sessao_db)):
    
    #Função ja para trazer organizado os itens do DB , substitui a antigas função livros_paginados
    Tarefas = db.query(TarefaDB).offset((page - 1)* limit).limit(limit).all()
    # Se nao tiver nada em tarefas:
    if not Tarefas:
        return {"Message": "Não existe nenhuma tarefa a ser cumprida."}
    
    #Função para contar a quantidade de itens na tabela
    total_tarefas = db.query(TarefaDB).count()
    
    return {
        "page": page,
        "limit": limit,
        "total": total_tarefas,
        #Faz um for in (para cada livro ou item do Livro ( que é os arquivos do nosso DB))
        "tarefas": [{"id": tarefa.id, "nome_tarefa": tarefa.nome_tarefa, "descricao_tarefa":tarefa.descricao_tarefa } for tarefa in Tarefas]
        
        }
    
#Rota para Adicionar uma Tarefa

@app.post("/adiciona")
def post_tarefa(tarefa:Tarefa, db: Session = Depends(sessao_db)):
    #usar a referencia de classe Tarefa(basemodel) diferente da classe TarefaDB
    #faz uma query no DB para verificar se a tarefa já tem
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.nome_tarefa == tarefa.nome_tarefa).first()
    
    # se a tarefa ja existir ( true) lança uma exception.
    if db_tarefa:
        raise HTTPException(status_code = 400, detail = "Essa tarefa já existe !")
    
    #se nao existir preciso add no banco de dados.
    
    nova_tarefa = TarefaDB(nome_tarefa = tarefa.nome_tarefa, descricao_tarefa = tarefa.descricao_tarefa, concluida = False )
    
    # atualizar no banco de dados os novos dados
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    
    return { "Mensagem" : "Tarefa adicionada com sucesso!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}