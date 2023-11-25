import sqlite3

class DadosGPSModel:
    def __init__(self, db_path):
        """
        Inicializa o modelo de dados GPS.

        Parâmetros:
        - db_path (str): Caminho para o arquivo do banco de dados SQLite.
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """
        Cria a tabela 'dados_gps' no banco de dados, se não existir.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS dados_gps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                imei TEXT,
                aceleracao_alarme TEXT,
                data_hora TEXT,
                direcao TEXT,
                horario TEXT,
                status_gps TEXT,
                latitude REAL,
                longitude REAL,
                velocidade REAL,
                direcao_gps REAL
            )
        ''')
        self.conn.commit()

    def insert_data(self, data):
        """
        Insere dados na tabela 'dados_gps'.

        Parâmetros:
        - data (tuple): Tupla contendo os valores a serem inseridos.
        """
        self.cursor.execute('''
            INSERT INTO dados_gps (
                imei, aceleracao_alarme, data_hora, direcao, horario, status_gps,
                latitude, longitude, velocidade, direcao_gps
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        self.conn.commit()

    def close_connection(self):
        """
        Fecha a conexão com o banco de dados.
        """
        if self.conn:
            self.conn.close()
