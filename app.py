#configuração pasica até a linha 13

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///livros.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#definir modelo de dados ---> criar a classe livros até a linha 35

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    editora = db.Column(db.String(200), default="Sem Editora")
    ativo = db.Column(db.Boolean, default=False)

    def __init__(self, titulo, autor, categoria, ano, editora="Sem Editora", ativo=False):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.ano = ano
        self.editora = editora
        self.ativo = ativo

    def __repr__(self):
        return f"<Livro {self.titulo}>"
    
    #criar tabela e inserir dados iniciais 

with app.app_context():
    db.create_all()

    # Ler o arquivo CSV para um DataFrame
    df = pd.read_csv("tabela - livros.csv")

    # Adicionar cada livro à base de dados, se ainda não estiverem presentes até a linha 57

    for index, row in df.iterrows():
        if not Livro.query.filter_by(titulo=row["Titulo do Livro"]).first():
            livro = Livro(
                titulo=row["Titulo do Livro"],
                autor=row["Autor"],
                categoria=row["Categoria"],
                ano=row["Ano de Publicação"],
                ativo=row["Ativo"] == "TRUE",
            )
            db.session.add(livro)
    db.session.commit()

#### Criar as Rotas para o Site ----> 1. **Rota `/inicio`:** 

@app.route("/inicio")
def inicio():
    livros = Livro.query.all()
    return render_template("lista.html", lista_de_livros=livros)

# 2. **Rota `/curriculo`:** -----> Crie uma rota para a página de currículo:   

@app.route("/curriculo")
def curriculo():
    return render_template("curriculo.html")

# 3. **Rota `/novo`:** ---> Crie uma rota para a página de adicionar novos livros:

@app.route("/novo")
def novo():
    return render_template("novo.html", titulo="Novo Livro")

# 4. **Rota `/criar`:**-----> Crie uma rota para processar o formulário e salvar o novo livro:

@app.route("/criar", methods=["POST"])
def criar():
    titulo = request.form["titulo"]
    autor = request.form["autor"]
    categoria = request.form["categoria"]
    ano = request.form["ano"]
    editora = request.form["editora"]

    livro = Livro(
        titulo=titulo, autor=autor, categoria=categoria, ano=ano, editora=editora
    )

    db.session.add(livro)
    db.session.commit()

    return redirect(url_for("inicio"))

# 2. **Adicionar a Rota para Deletar Livros:** -----> Adicione o seguinte código no `app.py` para criar a rota de deleção:

@app.route("/deletar/<int:id>")
def deletar(id):
    # Buscar o livro pelo ID
    livro = Livro.query.get(id)
    if livro:
        # Remover o livro do banco de dados
        db.session.delete(livro)
        db.session.commit()
    # Redirecionar de volta para a página inicial
    return redirect(url_for("inicio"))

#  Adicionar uma Rota para Exibir o Formulário de Edição para atualizar livros 

@app.route("/editar/<int:id>")
def editar(id):
    # Buscar o livro pelo ID
    livro = Livro.query.get(id)
    if livro:
        return render_template("editar.html", livro=livro)
    return redirect(url_for("inicio"))

### 3. **Adicionar a Rota para Processar a Atualização** 1. **Adicionar a Rota `/atualizar/<int:id>` no `app.py`:**
@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar(id):
    # Buscar o livro pelo ID
    livro = Livro.query.get(id)
    if livro:
        # Atualizar os dados do livro
        livro.titulo = request.form["titulo"]
        livro.autor = request.form["autor"]
        livro.categoria = request.form["categoria"]
        livro.ano = request.form["ano"]
        livro.editora = request.form["editora"]
        db.session.commit()
    return redirect(url_for("inicio"))




#### 4.5 Iniciar o Servidor Flask ---> 1. **Adicionar o Código para Rodar o Servidor:**
    # No final do `app.py`, adicione o seguinte código para iniciar o servidor Flask:

if __name__ == "__main__":
    app.run(debug=True)
