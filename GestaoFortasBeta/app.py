# Importações necessárias
from flask import Flask, redirect, render_template, request, url_for, flash
from sqlite3 import IntegrityError
from config import DB_URI
from models.models import CadastroVeiculo, db
from views.crud_cadastro_veiculos import CadastroVeiculo
from views import index
from sqlalchemy.exc import IntegrityError




# Inicializa o aplicativo Flask
app = Flask(__name__)

# Configuração da URI do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Chave para o alert!
app.secret_key = '3ec3f66c3e0a4a4b93a5c578b3b1972d'

# Inicializa a extensão SQLAlchemy com o aplicativo Flask
db.init_app(app)

# Adicione esta linha para configurar a pasta templates
app.template_folder = 'templates'

# Com o contexto do aplicativo, cria as tabelas no banco de dados
with app.app_context():
    db.create_all()


# Configuração das rotas
@app.route('/')
def home():
    return render_template('index.html')



# Rota para exibir todos os veículos cadastrados
@app.route('/obtertodos_veiculos')
def obtertodos_veiculos():
    veiculos = CadastroVeiculo.query.all()
    return render_template('todos_veiculos.html', veiculos=veiculos)



# Rota para cadastrar veículo
@app.route('/cadastrar_veiculo', methods=['GET', 'POST'])
def cadastrar_veiculo():
    if request.method == 'POST':
        imei = request.form['imei']
        placa = request.form['placa']
        # Verifica se o IMEI já existe
        veiculo_existente = CadastroVeiculo.query.filter_by(imei=imei).first()
        if veiculo_existente:
            flash('IMEI já existe. Por favor, insira um IMEI único.', 'error')
            return redirect(url_for('cadastrar_veiculo'))
        novo_veiculo = CadastroVeiculo(imei=imei, placa=placa)
        db.session.add(novo_veiculo)
        db.session.commit()
        return redirect(url_for('obtertodos_veiculos'))
    return render_template('cadastro_veiculo.html')



# Rota para editar um veículo existente
@app.route('/editar_veiculo/<int:id>', methods=['GET', 'POST'])
def editar_veiculo(id):
    # Obtém o veículo pelo ID fornecido
    veiculo = CadastroVeiculo.query.get(id)
    if request.method == 'POST':
        # Obtém os dados do formulário enviado pelo método POST
        novo_imei = request.form['imei']
        novo_placa = request.form['placa']
        # Verifica se o novo IMEI já existe (ignorando o veículo atual)
        veiculo_existente = CadastroVeiculo.query.filter(CadastroVeiculo.imei == novo_imei, CadastroVeiculo.id != id).first()
        if veiculo_existente:
            flash('IMEI já existe. Por favor, insira um IMEI único.', 'error')
            return redirect(url_for('editar_veiculo', id=id))
        # Atualiza os dados do veículo com os dados do formulário enviado pelo método POST
        veiculo.imei = novo_imei
        veiculo.placa = novo_placa
        try:
            # Confirma a transação no banco de dados
            db.session.commit()
        except IntegrityError:
            # Se ocorrer um erro de integridade (IMEI duplicado), faça o rollback e exiba uma mensagem de erro
            db.session.rollback()
            flash('Erro ao editar veículo. Por favor, insira um IMEI único.', 'error')
            return redirect(url_for('editar_veiculo', id=id))
        # Redireciona para a rota que exibe todos os veículos
        return redirect(url_for('obtertodos_veiculos'))
    # Renderiza o template 'edit_veiculo.html' para edição de dados
    return render_template('editar_veiculo.html', veiculo=veiculo)



# Rota para deletar um veículo existente
@app.route('/deletar_veiculo/<int:id>')
def deletar_veiculo(id):
    veiculo = CadastroVeiculo.query.get(id)
    db.session.delete(veiculo)
    db.session.commit()
    return redirect(url_for('obtertodos_veiculos'))



# Configuração Global
if __name__ == '__main__':
    # Inicia o aplicativo Flask
    app.run(host='0.0.0.0', port='5000', debug=True)
