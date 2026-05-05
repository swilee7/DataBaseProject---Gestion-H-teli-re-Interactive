# Fichier : DataBaseProject/database/Reservation.py

# On importe les fonctions génériques de connexion pour exécuter les requêtes
# (Assurez-vous que le fichier 'connection.py' existe et contient ces fonctions)
from .connection import fetch_query, execute_query


def get_reservations_stats():
    """
    Récupère les données de réservation pour calculer le prix moyen par mois et par chambre.
    Retourne une liste de tuples (Cod_C, Surface, Type, Mois, Prix_Moyen).
    """
    query = """
        SELECT 
            C.Cod_C, 
            C.Surface,
            CASE 
                WHEN S.CHAMBRE_Cod_C IS NOT NULL THEN 'Suite'
                ELSE 'Standard'
            END AS Type,
            DATE_FORMAT(R.Date_debut, '%Y-%m') AS Mois,
            AVG(R.Prix) AS Prix_Moyen
        FROM RESERVATION R
        JOIN CHAMBRE C ON R.CHAMBRE_Cod_C = C.Cod_C
        LEFT JOIN SUITE S ON C.Cod_C = S.CHAMBRE_Cod_C
        GROUP BY Mois, C.Cod_C
        ORDER BY Mois, Prix_Moyen DESC
    """
    # fetch_query retourne une liste de tuples
    rows = fetch_query(query)
    return rows

# Vous pouvez ajouter ici d'autres fonctions CRUD (Create, Read, Update, Delete) pour les réservations.