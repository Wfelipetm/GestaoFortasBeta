# Importa o Flask e as extensões necessárias
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# Importa o modelo de banco de dados e as tabelas
from models.models import db, CadastroVeiculo




# Cria uma instância do aplicativo Flask
app = Flask(__name__)

# Configura a URI do banco de dados (usando SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Inicializa o banco de dados
db.init_app(app)

# Cria todas as tabelas do banco de dados, se não existirem
with app.app_context():
    db.create_all()




# Rota para exibir todos os veículos cadastrados
@app.route('/')
def obtertodos_veiculos():
    # Consulta todos os registros na tabela CadastroVeiculo
    veiculos = CadastroVeiculo.query.all()
    # Renderiza o template 'index.html' e passa a lista de veículos como argumento
    return render_template('index.html', veiculos=veiculos)





# Rota para inserir um novo veículo
@app.route('/inserir_veiculo', methods=['GET', 'POST'])
def inserir_veiculo():
    if request.method == 'POST':
        # Obtém os dados do formulário enviado pelo método POST
        imei = request.form['imei']
        placa = request.form['placa']
        
        # Cria uma nova instância de CadastroVeiculo com os dados fornecidos
        novo_veiculo = CadastroVeiculo(imei=imei, placa=placa)
        # Adiciona o novo veículo ao banco de dados
        db.session.add(novo_veiculo)
        # Confirma a transação no banco de dados
        db.session.commit()
        # Redireciona para a rota que exibe todos os veículos
        return redirect(url_for('obtertodos_veiculos'))

    # Renderiza o template 'add_veiculo.html' para inserção de dados
    return render_template('add_veiculo.html')





# Rota para editar um veículo existente
@app.route('/editar_veiculo/<int:id>', methods=['GET', 'POST'])
def editar_veiculo(id):
    # Obtém o veículo pelo ID fornecido
    veiculo = CadastroVeiculo.query.get(id)

    if request.method == 'POST':
        # Atualiza os dados do veículo com os dados do formulário enviado pelo método POST
        veiculo.imei = request.form['imei']
        veiculo.placa = request.form['placa']
        

        # Confirma a transação no banco de dados
        db.session.commit()

        # Redireciona para a rota que exibe todos os veículos
        return redirect(url_for('obtertodos_veiculos'))

    # Renderiza o template 'edit_veiculo.html' para edição de dados
    return render_template('edit_veiculo.html', veiculo=veiculo)




# Rota para deletar um veículo existente
@app.route('/deletar_veiculo/<int:id>')
def deletar_veiculo(id):
    # Obtém o veículo pelo ID fornecido
    veiculo = CadastroVeiculo.query.get(id)

    # Remove o veículo do banco de dados
    db.session.delete(veiculo)
    # Confirma a transação no banco de dados
    db.session.commit()

    # Redireciona para a rota que exibe todos os veículos
    return redirect(url_for('obtertodos_veiculos'))




# Executa o aplicativo se este script for executado diretamente
if __name__ == '__main__':
    app.run(debug=True)
