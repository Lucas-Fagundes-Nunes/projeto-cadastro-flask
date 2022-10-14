
import re  # PARA TRATAMENTOS
import secrets

import MySQLdb.cursors  # CONEXAO MYSQL
from flask import Flask, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL  # CONEXAO MYSQL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Para validar acesso
secret = secrets.token_urlsafe(32)
app.secret_key = secret

# Conectando no banco de dados
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

# Adiocionando ao banco
@app.route('/', methods=['GET', 'POST'])
def Logando():
 
  msg = ''
  if request.method == 'POST' and 'email' in request.form and 'senha' in request.form:
    email = request.form['email']
    senha = request.form['senha']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM flask.user WHERE email = % s AND senha = % s', (email, senha ))
    account = cursor.fetchone()
    if account:
      session['id'] = account['id']
      session['nome'] = account['nome']
      msg = 'Login Efetuado com sucesso !'
      curso = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      curso.execute('SELECT * FROM flask.user')
      dados = curso.fetchall()
      return render_template('index.html', account=dados)


  else:
    return redirect(url_for('login'))
  



mysql = MySQL(app)


@app.route('/login', methods =['GET', 'POST'])
def login():
 return render_template('login.html')

@app.route('/logout')
def logout():
 session.pop('logado', None)
 session.pop('id', None)
 session.pop('nome', None)
 return redirect(url_for('login'))



@app.route('/cadastro', methods =['GET', 'POST'])
def register():
 msg = ''
 if request.method == 'POST' and 'nome' in request.form and 'senha' in request.form and 'email' in request.form :
  nome = request.form['nome']
  sobrenome = request.form['sobrenome']
  telefone = request.form['telefone']
  email = request.form['email']
  senha = request.form['senha']
  
  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  cursor.execute('SELECT * FROM flask.user WHERE nome = % s', (nome,)) # Precisa da ,
  account = cursor.fetchone()
  if account:
   msg = 'Essa conta já existe!'
  elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
   msg = 'Endereço de email invalido !'
  elif not re.match(r'[A-Za-z0-9]+', nome):
   msg = 'O nome de usuário deve conter apenas caracteres e números!'
  elif not nome or not senha or not email:
   msg = 'Por favor, preencha o formulário!'
  else:
   cursor.execute('INSERT INTO flask.user (nome, sobrenome, telefone, email, senha ) VALUES (% s, % s, % s, % s, % s)', (nome, sobrenome, str(telefone), email, senha ))
   mysql.connection.commit()
   msg = 'Você se registrou com sucesso!'
   return redirect(url_for('login'))
 elif request.method == 'POST':
  msg = 'Por favor, preencha o formulário!'
 return render_template('cadastro.html', msg = msg)








    
if __name__ == "__main__":
    app.run(debug=True)

# livro.titulo
# livro.sumario


