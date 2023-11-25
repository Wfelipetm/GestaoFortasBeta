import socket
import datetime
from models.dados_gps_model import DadosGPSModel

class DadosGPSView:
    def __init__(self, model, host, port):
        """
        Inicializa a visualização de dados GPS.

        Parâmetros:
        - model (DadosGPSModel): A instância do modelo de dados GPS.
        - host (str): O endereço IP do servidor.
        - port (int): A porta do servidor.
        """
        self.model = model
        self.host = host
        self.port = port

    def run_server(self):
        """
        Inicia o servidor UDP para receber dados GPS e processá-los.
        """
        try:
            # Configura o socket UDP
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_socket.bind((self.host, self.port))

            print(f"Servidor escutando em {self.host}:{self.port}")

            while True:
                data, addr = server_socket.recvfrom(1024)
                mensagem = data.decode('utf-8')

                partes = mensagem.split(',')
                self.process_data(partes)

        except Exception as e:
            print(f"Erro: {e}")

        finally:
            self.model.close_connection()

    def process_data(self, partes):
        """
        Processa os dados recebidos e os insere no banco de dados.

        Parâmetros:
        - partes (list): Lista de partes da mensagem recebida.
        """
        if len(partes) >= 11:
            imei = partes[0].split(':')[1]
            aceleracao_alarme = partes[1]

            data_hora = partes[2]
            current_year = datetime.datetime.now().year
            data_hora_formatted = datetime.datetime.strptime(data_hora, "%d%m%y%H%M%S").replace(
                year=current_year).strftime("%Y-%m-%d %H:%M:%S")

            direcao = partes[4]
            horario = partes[5]
            status_gps = partes[6]

            if status_gps == 'L':
                latitude = None
                longitude = None
            else:
                latitude, longitude = self.process_coordinates(partes[7], partes[9])

            velocidade = self.process_value(partes[11])
            direcao_gps = self.process_value(partes[12]) if len(partes) >= 13 and partes[12] else None

            data_to_insert = (imei, aceleracao_alarme, data_hora_formatted, direcao, horario, status_gps,
                              latitude, longitude, velocidade, direcao_gps)

            self.model.insert_data(data_to_insert)

            print(f"Dados inseridos no banco de dados")
        else:
            print("Número insuficiente de elementos na lista.")

    def process_coordinates(self, latitude_str, longitude_str):
        """
        Processa as coordenadas da mensagem e retorna a latitude e longitude.

        Parâmetros:
        - latitude_str (str): String representando a latitude.
        - longitude_str (str): String representando a longitude.

        Retorna:
        tuple: Tupla contendo a latitude e a longitude.
        """
        latitude = self.parse_coordinate(latitude_str)
        longitude = self.parse_coordinate(longitude_str)
        return latitude, longitude

    def parse_coordinate(self, coordinate_str):
        """
        Converte a string de coordenada em graus decimais.

        Parâmetros:
        - coordinate_str (str): String representando a coordenada.

        Retorna:
        float: Valor em graus decimais.
        """
        coordinate_str = coordinate_str.rstrip(';')
        degrees = int(coordinate_str[:3])
        minutes = float(coordinate_str[3:])
        return -1 * (degrees + minutes / 60)

    def process_value(self, value_str):
        """
        Processa o valor da mensagem e retorna como float.

        Parâmetros:
        - value_str (str): String representando o valor.

        Retorna:
        float or None: Valor convertido ou None se vazio.
        """
        value_str = value_str.rstrip(';')
        return float(value_str) if value_str and value_str != ';' else None