import socket
import sqlite3
import datetime

host = '0.0.0.0'
port = 8090

# Conectar ao banco de dados SQLite (ou criar se não existir)
db_path = "/home/sadmin/GestaoFrota/dbgeo.db"

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Criar tabela se não existir
    cursor.execute('''
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
    conn.commit()

    # Configurar o socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"Servidor escutando em {host}:{port}")

    while True:
        data, addr = server_socket.recvfrom(1024)
        mensagem = data.decode('utf-8')

        # Dividir a mensagem em partes usando vírgula como delimitador
        partes = mensagem.split(',')

        # Adicionar logs para depuração
        print(f"Mensagem recebida: {mensagem}")
        print(f"Lista de partes: {partes}")

        # Verificar se há elementos suficientes antes de acessar os índices
        if len(partes) >= 11:
            imei = partes[0].split(':')[1]
            aceleracao_alarme = partes[1]

            # Format data_hora with the desired format including the current year
            data_hora = partes[2]
            current_year = datetime.datetime.now().year
            data_hora_formatted = datetime.datetime.strptime(data_hora, "%d%m%y%H%M%S").replace(
                year=current_year).strftime("%Y-%m-%d %H:%M:%S")

            direcao = partes[4]
            horario = partes[5]
            status_gps = partes[6]

            # Handle cases when there is no GPS signal
            if status_gps == 'L':
                latitude = None
                longitude = None
            else:
                # Check for semicolon at the end of latitude and remove it
                latitude_str = partes[7].rstrip(';')
                latitude_degrees_str = latitude_str[:2]

                # Verificar se os caracteres são dígitos antes de convertê-los
                if latitude_degrees_str.isdigit():
                    latitude_degrees = int(latitude_degrees_str)
                else:
                    # Tratar o caso em que os caracteres não são dígitos
                    latitude_degrees = None

                latitude_minutes = float(latitude_str[2:])  # O restante representa os minutos e parte decimal
                latitude = -1 * (latitude_degrees + latitude_minutes / 60)

                # Check for semicolon at the end of longitude and remove it
                longitude_str = partes[9].rstrip(';')
                longitude_degrees_str = longitude_str[:3]

                # Verificar se os caracteres são dígitos antes de convertê-los
                if longitude_degrees_str.isdigit():
                    longitude_degrees = int(longitude_degrees_str)
                else:
                    # Tratar o caso em que os caracteres não são dígitos
                    longitude_degrees = None

                longitude_minutes = float(longitude_str[3:])  # O restante representa os minutos e parte decimal
                longitude = -1 * (longitude_degrees + longitude_minutes / 60)

            # Check for semicolon at the end of velocidade and remove it
            velocidade_str = partes[11].rstrip(';')
            velocidade = float(velocidade_str) if velocidade_str and velocidade_str != ';' else None

            # Check for semicolon at the end of direcao_gps and remove it
            direcao_gps_str = partes[12].rstrip(';') if len(partes) >= 13 and partes[12] else None
            direcao_gps = float(direcao_gps_str) if direcao_gps_str and direcao_gps_str != ';' else None

            # Inserir dados na tabela
            cursor.execute('''
                INSERT INTO dados_gps (
                    imei, aceleracao_alarme, data_hora, direcao, horario, status_gps,
                    latitude, longitude, velocidade, direcao_gps
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (imei, aceleracao_alarme, data_hora_formatted, direcao, horario, status_gps,
                  latitude, longitude, velocidade, direcao_gps))
            conn.commit()

            print(f"Dados inseridos no banco de dados")
        else:
            print("Número insuficiente de elementos na lista.")

except Exception as e:
    print(f"Erro: {e}")

finally:
    # Fechar a conexão com o banco de dados quando o programa encerrar
    if conn:
        conn.close()
