import psycopg2
conn = psycopg2.connect(
    dbname="data_arsenal_nueva",
    user="arsenal_user_nuevo",
    password="NuevaClave123",
    host="localhost",
    port="5432"
)
print("¡Conexión exitosa!")
conn.close()