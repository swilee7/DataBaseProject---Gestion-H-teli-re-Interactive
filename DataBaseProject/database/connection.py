import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="projetBD5"
        )
        if connection.is_connected():
            print("Connexion réussie à la base de données MySQL")
            return connection
    except Error as e:
        print("Erreur :", e)
        return None

def execute_query(query, params=None):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
            print("Requête exécutée avec succès")
        except Error as e:
            print("Erreur lors de l’exécution :", e)
        finally:
            cursor.close()
            connection.close()

def fetch_query(query, params=None):
    connection = create_connection()
    result = None
    if connection:
        try:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print("Erreur lors de la récupération :", e)
        finally:
            cursor.close()
            connection.close()
    return result
