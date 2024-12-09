# Fuel Calculator Web App

Este projeto consiste em uma aplicação web desenvolvida em Python (Flask) que auxilia o usuário a determinar qual combustível (gasolina ou etanol) é mais vantajoso abastecer, considerando o custo-benefício. Além disso, a aplicação integra-se a bancos de dados PostgreSQL e MySQL, armazenando um histórico das consultas realizadas pelo usuário.

## Objetivo

Fornecer uma interface simples na web onde o usuário possa inserir:
- Marca do automóvel
- Quilômetros rodados por litro (km/L) do veículo
- Preço da Gasolina
- Preço do Etanol

Ao clicar em um botão, a aplicação calcula qual combustível é mais vantajoso e exibe o resultado. Os dados da requisição (marca, preços e resultado do cálculo) são então gravados em tabelas no PostgreSQL e MySQL.

## Funcionalidades

- **Interface Web Simples**: Formulário para inserção de dados e botão para cálculo.
- **Cálculo de Melhor Combustível**: Avalia custo por km com gasolina e etanol.
- **Integração com Bancos de Dados**: Salva as consultas (marca, preços, resultado, data) nos bancos Postgres e MySQL.
- **Histórico e Armazenamento**: Permite auditoria e análise posterior dos dados inseridos.

## Requisitos

- Python 3.9 ou superior
- Pip3 (gerenciador de pacotes Python)
- Servidor WSGI (Gunicorn recomendado)
- Servidor Web (Nginx recomendado)
- PostgreSQL e MySQL (com tabelas pré-configuradas e acessíveis)
- Acesso à internet para instalar dependências

## Instalação das Dependências

1. (Opcional) Crie um ambiente virtual Python:
python3 -m venv venv source venv/bin/activate


2. Instale as dependências:
pip install -r requirements.txt


## Estrutura do Projeto

fuel_calculator/
├── app.py               # Arquivo principal da aplicação Flask
├── requirements.txt      # Lista de dependências
├── templates/
│   └── index.html        # Página inicial do formulário
├── static/               # (opcional) Arquivos estáticos (CSS, JS, imagens)
└── README.md             # Documentação do projeto



## Como Rodar Localmente (Desenvolvimento)

1. Certifique-se de que o Postgres e o MySQL estejam rodando e acessíveis. Ajuste as credenciais no `app.py` se necessário.
2. Rode o servidor Flask embutido (modo desenvolvimento):
python app.py
3. Acesse `http://127.0.0.1:5000` no navegador.

**Observação**: O servidor Flask interno é para desenvolvimento apenas. Em produção, utilize Gunicorn + Nginx.

## Rodando com Gunicorn (Produção Local)

1. Instale o Gunicorn:
pip install gunicorn

2. Rode a aplicação com Gunicorn:
gunicorn --bind 0.0.0.0:8000 app:app

3. Acesse `http://127.0.0.1:8000`.

## Deploy no EC2 (AWS)

### Pré-Requisitos no EC2

- Instância EC2 Linux (Amazon Linux 2 ou Ubuntu).
- Python 3, pip3, Git, Nginx, Gunicorn instalados:
sudo yum update -y sudo yum install python3 python3-pip git nginx -y sudo pip3 install gunicorn


### Passo a Passo

1. **Clonar o Repositório no EC2**:
git clone https://github.com/seu-usuario/seu-repo.git cd seu-repo


2. **Instalar Dependências**:
pip3 install -r requirements.txt


3. **Executar o Gunicorn**:
gunicorn --bind 0.0.0.0:8000 app:app


4. **Configurar o Nginx**:
Edite o arquivo `/etc/nginx/conf.d/fuel_calculator.conf` (exemplo):
server { listen 80; server_name SEU-ENDERECO-EC2;
   location / {
       proxy_pass http://127.0.0.1:8000;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
   }
}


Reinicie o Nginx:
sudo systemctl restart nginx


5. **Acessar Externamente**:
Abra o navegador e acesse:
http://SEU-ENDERECO-EC2/


Sua aplicação deve estar acessível publicamente.

### Considerações de Produção

- Ajuste o Security Group da instância EC2 para liberar a porta 80 (HTTP) e 22 (SSH).
- Configure HTTPS com Let’s Encrypt (opcional).
- Rode o Gunicorn como um serviço systemd para iniciar automaticamente ao reiniciar a instância.
- Utilize variáveis de ambiente para credenciais sensíveis.

## Integração com Bancos de Dados

No `app.py`, as configurações de conexão estão definidas como:

POSTGRES_CONFIG = { "host": "postgres-aula.cuebxlhckhcy.us-east-1.rds.amazonaws.com", "database": "postgresaula", "user": "postgresaula", "password": "PostgresAula123!", "port": 5432 }

MYSQL_CONFIG = { "host": "mysql-aula.cuebxlhckhcy.us-east-1.rds.amazonaws.com", "database": "mysqlaula", "user": "mysqlaula", "password": "MySQLAula123!", "port": 3306 }


### Tabela `logfuel`

- `id` (int, chave primária)
- `data` (date)
- `car_brand` (varchar)
- `km_per_liter` (numeric)
- `gas_price` (numeric)
- `ethanol_price` (numeric)
- `result` (varchar)

Certifique-se de que a tabela `logfuel` exista em ambos os bancos e possua essas colunas.
