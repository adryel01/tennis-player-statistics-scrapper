import psycopg2


# Conexão com o banco de dados
conn = psycopg2.connect(
    host="localhost",
    database="machine_learning",
    user="LENOVO",
    password="1234"
)

# Criação do cursor
cur = conn.cursor()
cur2 = conn.cursor()

# Execução da consulta
cur.execute("SELECT name FROM jogadores")
cur2.execute("SELECT * FROM jogadores")



# Armazenamento dos 5 primeiros resultados em uma lista
results = [row[0] for row in cur]
results_id = [row[0] for row in cur2]

# Fechamento do cursor e da conexão com o banco de dados
cur.close()
cur2.close()
conn.close()


