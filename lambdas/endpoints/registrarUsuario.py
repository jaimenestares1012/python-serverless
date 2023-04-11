import json
import os
import mysql.connector

def handler(event, context):
    # Conexión a la base de datos
    body = json.loads(event["body"])
    registro_id = ''
    name = body["name"]
    last_name = body["last_name"]
    mail = body["mail"]
    cnx = mysql.connector.connect(user='admin', password='12345678', host='database-prueba-tecnica.c0ffrigz07gs.us-east-1.rds.amazonaws.com', database='test')
    cursor = cnx.cursor()
    try:
        add_data = ("INSERT INTO registros (nombre, apellido, correo) VALUES (%s, %s, %s)")
        data_values = (name, last_name, mail)
        cursor.execute(add_data, data_values)
        cnx.commit()
        registro_id = cursor.lastrowid
        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print("error")
        body = {
            "message": "Failed to connect to database: {}".format(err)
        }
        print("body", body)
        response = {
            "statusCode": 500,
            "body": json.dumps(body)
        }
        return response
    body = {
     "message": "Data inserted successfully",
     "registro_id": registro_id
    }
    response = {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
        },
        "body": json.dumps(body)
    }


    return response
