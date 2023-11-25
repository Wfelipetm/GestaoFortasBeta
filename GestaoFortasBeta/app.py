from flask import Flask, redirect, render_template, request, url_for
from config import DB_URI
from models.models import db
#from views.crud_cadastro_veiculos import CadastroVeiculo
from views import index



# Inicializa o aplicativo Flask
app = Flask(__name__)

# Configuração da URI do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa a extensão SQLAlchemy com o aplicativo Flask
db.init_app(app)

# Com o contexto do aplicativo, cria as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Configuração das rotas
app.route('/')(index)




# Rota para cadastrar veículo
'''@app.route('/', methods=['GET', 'POST'])
def cadastrar_veiculo():
    if request.method == 'POST':
        imei = request.form['imei']
        placa = request.form['placa']

        novo_veiculo = CadastroVeiculo(imei=imei, placa=placa)
        db.session.add(novo_veiculo)
        db.session.commit()

        return redirect(url_for('obtertodos_veiculos'))

    return render_template('cadastro_veiculo.html')'''





# Configuração Global
if __name__ == '__main__':
    # Inicia o aplicativo Flask
    app.run(host='0.0.0.0', port='5000', debug=True)