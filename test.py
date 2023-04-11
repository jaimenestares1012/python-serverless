import mysql.connector


def lambda_handler(event, context):
    try:
        # Conectarse a la base de datos
        print("lambda_handler")
        cnx = mysql.connector.connect(user='admin', password='12345678', host='database-prueba-tecnica.c0ffrigz07gs.us-east-1.rds.amazonaws.com', database='test')
        print("cnz", cnx)
        cursor = cnx.cursor()
        print("cursos", cursor)
        # Realizar una consulta
        query = "SELECT * FROM ejemplo"
        cursor.execute(query)
        print("exejcuta quety", query)
        # Obtener los resultados
        rows = cursor.fetchall()
        print("rows", rows)
        # Imprimir los resultados
        for row in rows:
            print(row)

        # Cerrar la conexión
        print("cursos cloase ")
        cursor.close()
        print("coese")
        cnx.close()
    except Exception as exception:
        print("exception", exception)

    response = {
        "statusCode": 200,
        "body": "ddd"
    }

    return response

