import psycopg2 as pg2

conn = pg2.connect(database='CENACE', user='postgres', password='Licuadora1234')

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS pnd;")

cur.execute("""CREATE TABLE IF NOT EXISTS pnd(
    fecha DATE ,
    hora SMALLINT,
    zona_de_carga VARCHAR(50),
    precio_zonal NUMERIC(6,2),
    c_energia NUMERIC(6,2),
    c_perdidas NUMERIC(6,2),
    c_congestion NUMERIC(6,2)
    );""")


cur.execute("""COPY pnd FROM 'C:/Users/Angel/Documents/Ironhack/web_project/files/BCA-PND-MTR.csv' WITH (FORMAT csv);""")

conn.commit()
conn.close()