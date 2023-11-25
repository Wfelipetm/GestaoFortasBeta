from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, CadastroAgentes

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/agentes')
def obtertodos_agentes():
    agentes = CadastroAgentes.query.all()
    return render_template('index_agentes.html', agentes=agentes)



@app.route('/inserir_agente', methods=['GET', 'POST'])
def inserir_agente():
    if request.method == 'POST':
        nome_completo = request.form['nome_completo']
        endereco = request.form['endereco']

        novo_agente = CadastroAgentes(nome_completo=nome_completo, endereco=endereco)
        db.session.add(novo_agente)
        db.session.commit()

        return redirect(url_for('obtertodos_agentes'))

    return render_template('add_agente.html')



@app.route('/editar_agente/<int:id>', methods=['GET', 'POST'])
def editar_agente(id):
    agente = CadastroAgentes.query.get(id)

    if request.method == 'POST':
        agente.nome_completo = request.form['nome_completo']
        agente.endereco = request.form['endereco']
        db.session.commit()

        return redirect(url_for('obtertodos_agentes'))

    return render_template('edit_agente.html', agente=agente)



@app.route('/deletar_agente/<int:id>')
def deletar_agente(id):
    agente = CadastroAgentes.query.get(id)
    db.session.delete(agente)
    db.session.commit()

    return redirect(url_for('obtertodos_agentes'))

if __name__ == '__main__':
    app.run(debug=True)
