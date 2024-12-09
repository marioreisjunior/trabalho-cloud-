from flask import Flask, render_template, request
import psycopg2
import pymysql
from datetime import date

app = Flask(__name__)

# Configurações do PostgreSQL
POSTGRES_CONFIG = {
    "host": "postgres-aula.cuebxlhckhcy.us-east-1.rds.amazonaws.com",
    "database": "postgresaula",
    "user": "postgresaula",
    "password": "PostgresAula123!",
    "port": 5432
}

# Configurações do MySQL
MYSQL_CONFIG = {
    "host": "mysql-aula.cuebxlhckhcy.us-east-1.rds.amazonaws.com",
    "database": "mysqlaula",
    "user": "mysqlaula",
    "password": "MySQLAula123!",
    "port": 3306
}

def insert_postgres(data_hoje, car_brand, km_per_liter, gas_price, ethanol_price, result):
    """Insere um registro na tabela logfuel do Postgres."""
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cur = conn.cursor()
        insert_query = """
            INSERT INTO logfuel (data, car_brand, km_per_liter, gas_price, ethanol_price, result)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        cur.execute(insert_query, (data_hoje, car_brand, km_per_liter, gas_price, ethanol_price, result))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return new_id
    except Exception as e:
        print("Erro ao inserir no Postgres:", e)
        return None

def insert_mysql(car_brand, km_per_liter, gas_price, ethanol_price, result):
    """Insere um registro na tabela logfuel do MySQL."""
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        cur = conn.cursor()
        insert_query = """
            INSERT INTO logfuel (car_brand, km_per_liter, gas_price, ethanol_price, result)
            VALUES (%s, %s, %s, %s, %s);
        """
        cur.execute(insert_query, (car_brand, km_per_liter, gas_price, ethanol_price, result))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        conn.close()
        return new_id
    except Exception as e:
        print("Erro ao inserir no MySQL:", e)
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            # Captura os dados do formulário
            car_brand = request.form.get('car_brand')
            km_per_liter = float(request.form.get('km_per_liter'))
            gas_price = float(request.form.get('gas_price'))
            ethanol_price = float(request.form.get('ethanol_price'))

            # Cálculo de custo-benefício
            gas_cost_per_km = gas_price / km_per_liter
            ethanol_cost_per_km = ethanol_price / km_per_liter

            if gas_cost_per_km < ethanol_cost_per_km:
                result = f"A gasolina é mais vantajosa para o carro {car_brand}."
            else:
                result = f"O etanol é mais vantajoso para o carro {car_brand}."

            # Inserção no banco de dados
            data_hoje = date.today()
            postgres_id = insert_postgres(data_hoje, car_brand, km_per_liter, gas_price, ethanol_price, result)
            mysql_id = insert_mysql(car_brand, km_per_liter, gas_price, ethanol_price, result)

            print(f"Inserido no Postgres com ID: {postgres_id}, e no MySQL com ID: {mysql_id}")

        except Exception as e:
            result = f"Erro no cálculo ou inserção no banco: {str(e)}"
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=False)
