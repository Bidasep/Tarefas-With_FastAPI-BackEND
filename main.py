#Objetivo
#O objetivo do desafio é implementar a persistência dos dados no SQLite e conectar os endpoints 
# existentes para que eles interajam com o banco de dados, ao invés de armazenar as informações na 
# memória. Isso envolve:

#Substituir o dicionário que atualmente guarda as tarefas por um banco de dados SQLite.

#Criar a estrutura do banco de dados e implementar as operações necessárias 
# (inserir, listar, atualizar e remover tarefas).

#Adaptar os endpoints existentes para realizar operações de CRUD no banco de dados SQLite.

#Com isso, sua aplicação será capaz de armazenar e recuperar tarefas de forma persistente, permitindo
# que os dados não se percam quando o servidor for reiniciado. O banco de dados será o responsável 
# por armazenar as informações de maneira mais eficiente e segura.

#Passo a passo para implementar:
#Substituir o dicionário pelo SQLite: Crie um banco de dados SQLite e configure o modelo para as tarefas.

#Endpoints GET, POST, PUT e DELETE: Alterar os endpoints para fazer requisições no
# banco de dados, realizando as operações de CRUD de forma persistente.

#Testar os endpoints: Realizar testes para garantir que a integração com o banco de dados está 
# funcionando corretamente.

#Esse desafio ajudará a consolidar a integração entre o FastAPI e um banco de dados real, 
# proporcionando mais aprendizado sobre como trabalhar com bancos de dados em um contexto de 
# aplicações web.


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
    concluida:bool = False
    
class Tarefa(BaseModel):
    nome_tarefa: str
    descricao_tarefa: str
    concluida: bool = False  
    
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
    
    #Função ja para trazer organizado os itens do DB , substitui a antigas função 
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
        "tarefas": [{"id": tarefa.id, "nome_tarefa": tarefa.nome_tarefa, "descricao_tarefa":tarefa.descricao_tarefa, "Tarefa_concluida":tarefa.concluida } for tarefa in Tarefas]
        
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
    
    nova_tarefa = TarefaDB(nome_tarefa = tarefa.nome_tarefa, descricao_tarefa = tarefa.descricao_tarefa, concluida = tarefa.concluida )
    
    # atualizar no banco de dados os novos dados
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    
    return { "Mensagem" : "Tarefa adicionada com sucesso!"}

@app.put("/atualiza/{id_tarefa}")

#recebe os parametros para atualizar as tarefas : id da tarefa ja definido direto quando cria no Banco
# tarefa, us aa referencia da Tarefa classe (base model), db session para "Abrir o Banco de dados" chama função sessão DB
def put_tarefas(id_tarefa:int, tarefa:Tarefa , db:Session = Depends(sessao_db)):
    
    #faz uma query no banco de dados db.query, e já filtra pelo ID , 
    #verifica se tem a tarefa no DB TarefaDB.id == id_tarefa
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.id == id_tarefa).first()

    # se nao tiver no DB lança uma a exception.
    if not db_tarefa:
        return HTTPException( status_code=400 , detail= "Está tarefa nao foi encontrada.")
    
    # atualiza os dados no Banco de dados
    db_tarefa.nome_tarefa == tarefa.nome_tarefa     
    db_tarefa.descricao_tarefa == tarefa.descricao_tarefa
    db_tarefa.concluida == tarefa.concluida
    
    # atualizar no banco de dados os novos dados
    db.commit()
    db.refresh(db_tarefa)
    
    return {"message" : f"A tarefa {db_tarefa.nome_tarefa} foi atualizada comn sucesso"}

    



