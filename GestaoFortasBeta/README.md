# Sistema de Gestão de Frota

O Sistema de Gestão de Frota é uma aplicação de monitoramento 24 horas para veículos de um órgão público, proporcionando rastreamento em tempo real, relatórios detalhados de trajetos e alertas automáticos. Desenvolvido utilizando o framework web Flask em Python e armazenando dados em um banco de dados MySQL, o sistema segue o padrão MVT (Model-View-Template).

## Funcionalidades Principais

- **Rastreamento em Tempo Real:** Monitora a localização atual de cada veículo em tempo real.

- **Relatórios de Trajeto:** Gera relatórios detalhados sobre o trajeto percorrido por cada veículo em um período específico.

- **Alertas e Notificações:** Recebe alertas automáticos sobre eventos específicos, como desvios de rota ou paradas não programadas.

## Tecnologias Utilizadas

- **Flask:** Framework web em Python para desenvolvimento rápido e eficiente.

- **MySQL:** Banco de dados relacional para armazenar e gerenciar os dados da frota.

- **MVT (Model-View-Template):** Padrão arquitetural que separa a lógica de negócios (Model), a lógica de apresentação (View) e o controle de fluxo (Template).

## Requisitos de Sistema

- **Python 3.9:** Versão necessária do Python para executar o sistema.

- **Flask:** Framework web, pode ser instalado com o comando `pip install flask`.

- **MySQL:** Banco de dados relacional. Certifique-se de ter um servidor MySQL em execução.

## Instalação e Configuração

1. Clone o repositório: `git clone https://github.com/talmeida1986/GestaoFrota.git`

2. Acesse o diretório do projeto: `cd GestaoFrota`

3. Instale as dependências:

   ```bash
   pip install flask folium flask-sqlalchemy SQLAlchemy
   ```

4. Configure as variáveis de ambiente em um arquivo `.env` com as informações do banco de dados:

   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=0kSY9mv1IytEgpNUkfnR
   DB_NAME=geo
   ```

5. Inicie o servidor: `python app.py`

6. Acesse o sistema no navegador: `http://localhost:5000`

## Modelos de Dados para Aplicação de Mapeamento

### Tabela Marcador
Modelo para representar marcadores fixos no mapa.

- **id (int):** Identificador único do marcador.
- **nome (str):** Nome do marcador.
- **latitude (float):** Latitude do marcador.
- **longitude (float):** Longitude do marcador.
- **popup (str):** Texto exibido quando o marcador é clicado.
- **icone (str):** Caminho para o ícone personalizado do marcador.

### Tabela CadastroVeiculo
Modelo para cadastrar informações de veículos.

- **id (int):** Identificador único do veículo.
- **imei (str):** IMEI único do veículo.
- **fabricante (str):** Fabricante do veículo.
- **modelo (str):** Modelo do veículo.
- **placa (str):** Placa do veículo.
- **quilometragem (float):** Quilometragem do veículo.
- **foto (str):** Caminho para a foto do veículo.
- **ano_fabricacao (int):** Ano de fabricação do veículo.
- **cor (str):** Cor do veículo.
- **tipo_combustivel (str):** Tipo de combustível do veículo.
- **crvl_ano (int):** Ano do CRVL do veículo.
- **secretaria (str):** Secretaria associada ao veículo.
- **dados_gps (relationship):** Relacionamento com os dados GPS associados ao veículo.

### Tabela DadosGPS
Modelo para representar dados GPS associados a veículos.

- **id (int):** Identificador único dos dados GPS.
- **imei (str):** IMEI único do veículo associado.
- **aceleracao_alarme (str):** Informação de aceleração ou alarme.
- **data_hora (str):** Data e hora dos dados GPS.
- **direcao (str):** Direção dos dados GPS.
- **horario (str):** Horário dos dados GPS.
- **status_gps (str):** Status do GPS nos dados.
- **latitude (float):** Latitude dos dados GPS.
- **longitude (float):** Longitude dos dados GPS.
- **velocidade (float):** Velocidade dos dados GPS.
- **direcao_gps (float):** Direção do GPS nos dados.
- **veiculo (relationship):** Relacionamento com o veículo associado aos dados GPS.

### Tabela CadastroAgentes
Modelo para cadastrar informações de agentes.

- **id (int):** Identificador único do agente.
- **nome_completo (str):** Nome completo do agente.
- **endereco (str):** Endereço do agente.
- **bairro (str):** Bairro do agente.
- **cidade (str):** Cidade do agente.
- **cep (str):** CEP do agente.
- **cpf (str):** CPF do agente.
- **rg (str):** RG do agente.
- **matricula (str):** Matrícula do agente.
- **data_nascimento (Date):** Data de nascimento do agente.
- **foto (str):** Caminho para a foto do agente.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).