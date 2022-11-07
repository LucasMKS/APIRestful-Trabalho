from calendar import c
import sqlite3
from sqlite3 import Error
from flask import Flask, request, render_template, redirect, url_for, flash, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a9e0759a726a5d1c0fd37324feba25506'


def get_db_connection():
    conn = sqlite3.connect("C:\\Users\\lucas\\Documents\\projetos\\APIRestful\\agenda.db")
    conn.row_factory = sqlite3.Row
    return conn


conn = get_db_connection()
cur = conn.cursor()


def get_contato(contato_id):
    conn = get_db_connection()
    contato = conn.execute('SELECT * FROM contatos WHERE id = ?',
                           (contato_id,)).fetchone()
    conn.close()
    if contato is None:
        abort(404)
    return contato



# Mostrar tabela completa na tela inicial
@app.route('/', methods=('POST', 'GET'))
def index():
    conn = get_db_connection()
    contatos = conn.execute('SELECT * FROM contatos').fetchall()
    conn.close()
    return render_template('index.html', contatos=contatos)


# Criar
@app.route('/criar/', methods=('POST', 'GET'))
def criar():
    if request.method == 'POST':
        nome = request.form['nome']
        empresa = request.form['empresa']
        telefone = request.form['telefone']
        email = request.form['email']
        if not nome:
            flash('Preencha o NOME!')
        elif not empresa:
            flash('Preencha a EMPRESA!')
        elif not telefone:
            flash('Preencha o TELEFONE!')
        elif not email:
            flash('Preencha o EMAIL!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO contatos (nome, empresa, telefone, email) VALUES (?, ?, ?, ?)',
                         (nome, empresa, telefone, email))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('criar.html')


# Deletar por ID
@app.route('/deletar/<int:id>')
def deletar(id):
        contato = get_contato(id)
        conn = get_db_connection()
        conn.execute('DELETE FROM contatos WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('{} foi excluído com sucesso!'.format(contato['nome']))
        return redirect(url_for('index'))

# Editar por ID
@app.route('/editar/<int:id>', methods=('GET', 'POST'))
def editar(id):
    contato = get_contato(id)

    if request.method == 'POST':
        nome = request.form['nome']
        empresa = request.form['empresa']
        telefone = request.form['telefone']
        email = request.form['email']

        if not nome:
            flash('Preencha o NOME!')
        elif not empresa:
            flash('Preencha a EMPRESA!')
        elif not telefone:
            flash('Preencha o TELEFONE!')
        elif not email:
            flash('Preencha o EMAIL!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE contatos SET nome = ?, empresa = ?, telefone = ?, email = ?' 'WHERE id = ?',
                         (nome, empresa, telefone, email, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('editar.html', contato=contato)


@app.route('/selecao/', methods=('GET','POST'))
def selecao():
        
        if request.method == 'POST':
            busca = request.form['busca'].lower()
            conn = get_db_connection()
            select = None
            nome = None
            if busca == 'nome':
                nome = request.form['valor']
                select = conn.execute("SELECT * FROM contatos WHERE nome = ?",(nome,)).fetchone()
            if busca == 'email':
                email = request.form['valor']
                select = conn.execute('SELECT * FROM contatos WHERE email = ?',(email,)).fetchone()
            if busca == 'empresa':
                empresa = request.form['valor']
                select = conn.execute('SELECT * FROM contatos WHERE empresa = ?',(empresa,)).fetchone()

            if select is None:
                abort(404)

            conn.commit()
            conn.close()
            return render_template('view.html', select=select)
        return render_template('selecao.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)


# venv\scripts\ligar.ps1
# python main.py
# http://127.0.0.1:5000/
# desligar
# deactivate
