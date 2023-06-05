import pandas as pd
import psycopg2

# Conexão com o banco de dados PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="machine_learning",
    user="LENOVO",
    password="1234"
)

# Leitura da planilha em formato CSV usando o pandas
df = pd.read_excel("C:/Users/LENOVO/Desktop/Machine Learning/src/Dados/partidas.xls")

# Iteração sobre cada linha da planilha
for index, row in df.iterrows():
    # Extração dos valores das colunas
    id = row['id']
    name = row['name']
    opponent_name = row['opponent_name']
    date = row['date']
    bestOf = row['bestOf']
    surface = row['surface']
    indoor = row['indoor']
    speed = row['speed']
    winner = row['winner']
    
    # Criação do comando SQL para inserir os valores na tabela do banco de dados
    sql = f"INSERT INTO partidas (id, name, opponent_name, date, bestOf, surface, indoor, speed, winner) VALUES ({id}, '{name}', '{opponent_name}', '{date}', {bestOf}, '{surface}', {indoor}, {speed}, '{winner}')"
    
    # Execução do comando SQL
    cursor = conn.cursor()
    cursor.execute(sql)
    
    # Confirmação da transação
    conn.commit()
    
# Fechamento da conexão com o banco de dados
conn.close()
