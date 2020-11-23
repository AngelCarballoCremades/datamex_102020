import mysql.connector
from mysql.connector import errorcode

try:
    conn = mysql.connector.connect(user='root', password='Licuadora1234', host='127.0.0.1', database='cenace')
    print('Succesfull connection!')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:

    cur = conn.cursor(buffered=True)

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

    # cur.execute("""INSERT INTO pnd VALUES ('SIN', 'MDA', '2019-04-01', 23, 'OAXACA', 100.23, 2.45, 10000.30, 0.00);""")

    cur.execute("""LOAD DATA INFILE 'PND.csv'
                    INTO TABLE pnd
                    FIELDS TERMINATED BY ','
                    LINES TERMINATED BY '\\n'
                    IGNORE 1 ROWS;""")
    conn.commit()

    cur.execute("""SELECT * FROM pnd;""")
    print(list(cur.fetchone()))

    cur.close()
    conn.close()

