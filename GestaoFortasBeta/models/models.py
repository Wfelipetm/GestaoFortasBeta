from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

# Inicializa a extensão SQLAlchemy
db = SQLAlchemy()

class Marcador(db.Model):
    """
    Modelo para representar marcadores fixo no mapa.

    Atributos:
    - id (int): Identificador único do marcador.
    - nome (str): Nome do marcador.
    - latitude (float): Latitude do marcador.
    - longitude (float): Longitude do marcador.
    - popup (str): Texto exibido quando o marcador é clicado.
    - icone (str): Caminho para o ícone personalizado do marcador.
    """
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    popup = db.Column(db.String(50))
    icone = db.Column(db.String(100))  # Caminho para o ícone personalizado

class Dados(db.Model):
    """
    Modelo para representar dados relacionados à localização.

    Atributos:
    - id (int): Identificador único do dado.
    - identificacao (str): Identificação do dado.
    - latitude (str): Latitude associada ao dado.
    - longitude (str): Longitude associada ao dado.
    - velocidade (str): Velocidade associada ao dado.
    - data_hora (str): Data e hora do dado.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    identificacao = db.Column(db.String(50))
    latitude = db.Column(db.String(20))
    longitude = db.Column(db.String(20))
    velocidade = db.Column(db.String(10))
    data_hora = db.Column(db.String(50))

class CadastroVeiculo(db.Model):
    """
    Modelo para cadastrar informações de veículos.

    Atributos:
    - id (int): Identificador único do veículo.
    - imei (str): IMEI único do veículo.
    - fabricante (str): Fabricante do veículo.
    - modelo (str): Modelo do veículo.
    - placa (str): Placa do veículo.
    - quilometragem (float): Quilometragem do veículo.
    - foto (str): Caminho para a foto do veículo.
    - ano_fabricacao (int): Ano de fabricação do veículo.
    - cor (str): Cor do veículo.
    - tipo_combustivel (str): Tipo de combustível do veículo.
    - crvl_ano (int): Ano do CRVL do veículo.
    - secretaria (str): Secretaria associada ao veículo.
    """
    __tablename__ = 'cadastro_veiculo'

    id = db.Column(db.Integer, primary_key=True)
    imei = db.Column(db.String, unique=True)
    fabricante = db.Column(db.String)
    modelo = db.Column(db.String)
    placa = db.Column(db.String)
    quilometragem = db.Column(db.Float)
    foto = db.Column(db.String)
    ano_fabricacao = db.Column(db.Integer)
    cor = db.Column(db.String)
    tipo_combustivel = db.Column(db.String)
    crvl_ano = db.Column(db.Integer)
    secretaria = db.Column(db.String)
    dados_gps = relationship("DadosGPS", back_populates="veiculo", uselist=False)

class DadosGPS(db.Model):
    """
    Modelo para representar dados GPS associados a veículos.

    Atributos:
    - id (int): Identificador único dos dados GPS.
    - imei (str): IMEI único do veículo associado.
    - aceleracao_alarme (str): Informação de aceleração ou alarme.
    - data_hora (str): Data e hora dos dados GPS.
    - direcao (str): Direção dos dados GPS.
    - horario (str): Horário dos dados GPS.
    - status_gps (str): Status do GPS nos dados.
    - latitude (float): Latitude dos dados GPS.
    - longitude (float): Longitude dos dados GPS.
    - velocidade (float): Velocidade dos dados GPS.
    - direcao_gps (float): Direção do GPS nos dados.
    """
    __tablename__ = 'dados_gps'

    id = db.Column(db.Integer, primary_key=True)
    imei = db.Column(db.String, db.ForeignKey('cadastro_veiculo.imei'), unique=True)
    aceleracao_alarme = db.Column(db.String)
    data_hora = db.Column(db.String)
    direcao = db.Column(db.String)
    horario = db.Column(db.String)
    status_gps = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    velocidade = db.Column(db.Float)
    direcao_gps = db.Column(db.Float)

    veiculo = relationship("CadastroVeiculo", back_populates="dados_gps")

class CadastroAgentes(db.Model):
    """
    Modelo para cadastrar informações de agentes.

    Atributos:
    - id (int): Identificador único do agente.
    - nome_completo (str): Nome completo do agente.
    - endereco (str): Endereço do agente.
    - bairro (str): Bairro do agente.
    - cidade (str): Cidade do agente.
    - cep (str): CEP do agente.
    - cpf (str): CPF do agente.
    - rg (str): RG do agente.
    - matricula (str): Matrícula do agente.
    - data_nascimento (Date): Data de nascimento do agente.
    - foto (str): Caminho para a foto do agente.
    """
    __tablename__ = 'cadastro_agentes'

    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String)
    endereco = db.Column(db.String)
    bairro = db.Column(db.String)
    cidade = db.Column(db.String)
    cep = db.Column(db.String)
    cpf = db.Column(db.String)
    rg = db.Column(db.String)
    matricula = db.Column(db.String)
    data_nascimento = db.Column(db.Date)
    foto = db.Column(db.String)