# database/Support.py
from .connection import execute_query


def insert_contact_message(nom, email, objet, message):
    """
    Insère un nouveau message de contact dans la table SUPPORT.

    Args:
        nom (str): Nom complet du client.
        email (str): Email du client.
        objet (str): Objet de la demande.
        message (str): Contenu du message.

    Returns:
        bool: True si l'insertion a réussi, False sinon.
    """
    sql = """
    INSERT INTO SUPPORT (Nom_Client, Email_Client, Objet_Demande, Message_Client)
    VALUES (%s, %s, %s, %s)
    """
    params = (nom, email, objet, message)

    try:
        # execute_query est la fonction qui gère la connexion et l'exécution
        execute_query(sql, params)
        return True
    except Exception as e:
        print(f"Erreur lors de l'insertion du message de contact: {e}")
        return False

# Ajoutez d'autres fonctions ici si vous souhaitez lire les messages (ex: get_all_support_tickets)