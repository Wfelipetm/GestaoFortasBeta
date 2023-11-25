# views/index.py
from flask import render_template
from models.models import db, Marcador, Dados
from sqlalchemy import func
import folium

def index():
    """
    Renderiza a página inicial com um mapa contendo marcadores e popups.

    Retorna:
    flask.render_template: Template HTML renderizado.
    """
    # Consulta para obter os últimos registros para cada identificador
    dados = Dados.query.group_by(Dados.identificacao).having(func.max(Dados.data_hora)).all()

    # Buscar marcadores do banco de dados
    marcadores = Marcador.query.all()

    # Cria um mapa usando Folium
    if marcadores:
        m = folium.Map(location=[marcadores[0].latitude, marcadores[0].longitude], zoom_start=15)
    else:
        m = folium.Map(location=[0, 0], zoom_start=15)  # Fallback para coordenadas padrão ou ajuste conforme necessário

    # Adiciona marcadores para cada conjunto de coordenadas com popups e ícones personalizados
    for dado in dados:
        folium.Marker(
            location=[float(dado.latitude), float(dado.longitude)],
            popup=f'Dados: {dado.identificacao}'
        ).add_to(m)

    # Adiciona marcadores para cada conjunto de coordenadas com popups e ícones personalizados
    for marcador in marcadores:
        folium.Marker(
            location=[marcador.latitude, marcador.longitude],
            popup=marcador.popup,
            
            icon=folium.CustomIcon(icon_image='static/img/saude.png', icon_size=(28, 28))

        ).add_to(m)

    # Salva o mapa como um arquivo HTML temporário
    m.save('templates/map.html')

    # Renderiza o template HTML
    return render_template('index.html')