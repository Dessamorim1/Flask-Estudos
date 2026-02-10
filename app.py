import email
from flask import Flask,render_template,request,redirect, session,flash,url_for

app = Flask(__name__)
app.secret_key = '2013289'

class Animes:
    def __init__(self,nome,categoria):
        self.nome = nome
        self.categoria = categoria

class Usuarios:
    def __init__(self,email,senha):
        self.email = email
        self.senha = senha

usuario1 = Usuarios('Ananda','1234')
usuario2 = Usuarios('Bia', '@2020')

usuarios = { usuario1.email : usuario1, 
            usuario2.email : usuario2}

Anime1 = Animes('Naruto','Shounen')
Anime2 = Animes('One Piece', 'Shounen')
Anime3 = Animes('Jujutsu Kaisen', 'Shounen')
lista = [Anime1,Anime2,Anime3]
       
@app.route('/')
def home():
    return render_template('index.html',lista=lista,titulo="Animes")

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect (url_for('login',proxima=url_for('novo')))
    return render_template('novo.html',titulo='Novo anime')

@app.route('/criar',methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    anime = Animes(nome,categoria)
    lista.append(anime)
    return redirect(url_for('home'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html',titulo='Faça seu login',proxima=proxima)

@app.route('/autenticar',methods=['POST'])
def autenticar():
    if request.form['email'] in usuarios:
        user = usuarios[request.form['email']]
        if request.form['senha'] == user.senha:
            session['usuario_logado'] = user.email
            flash(user.email + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário ou senha informado incorreto!')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)