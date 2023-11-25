# Importa a biblioteca 'os' para manipulação de sistema de arquivos
import os

# Define a URI do banco de dados usando SQLite e o caminho absoluto para o arquivo "geo.db"
DB_URI = f'sqlite:///{os.path.abspath("C:/db/geo.db")}'
