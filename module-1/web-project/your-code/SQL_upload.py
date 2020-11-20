import psycopg2 as pg2

conn = pg2.connect(database='CENACE', user='postgres', password='Licuadora1234')

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS pnd;")

cur.execute("""CREATE TABLE IF NOT EXISTS pnd(
    sistema VARCHAR(3),
    mercado VARCHAR(3),
    fecha DATE ,
    hora SMALLINT,
    zona_de_carga VARCHAR(50),
    precio_zonal NUMERIC(7,2),
    c_energia NUMERIC(7,2),
    c_perdidas NUMERIC(7,2),
    c_congestion NUMERIC(10,2)
    );""")

cur.execute("DROP TABLE IF EXISTS pml;")

cur.execute("""CREATE TABLE IF NOT EXISTS pml(
    sistema VARCHAR(3),
    mercado VARCHAR(3),
    fecha DATE ,
    hora SMALLINT,
    clave_nodo VARCHAR(50),
    precio_marginal_local NUMERIC(10,2),
    c_energia NUMERIC(7,2),
    c_perdidas NUMERIC(7,2),
    c_congestion NUMERIC(7,2)
    );""")




conn.commit()
conn.close()