from .connection import fetch_query
import pandas as pd


def agences_distinct():
    rows = fetch_query("SELECT COUNT(DISTINCT Cod_A) FROM AGENCE_DE_VOYAGE")
    return rows[0][0] if rows and rows[0][0] is not None else 0


def villes_distinctes():
    rows = fetch_query("SELECT COUNT(DISTINCT Nom_Ville) FROM VILLE")
    return rows[0][0] if rows and rows[0][0] is not None else 0


def ville_plus_agences():
    rows = fetch_query("""
        SELECT VILLE_Nom_Ville, COUNT(*) as nb 
        FROM AGENCE_DE_VOYAGE GROUP BY VILLE_Nom_Ville 
        ORDER BY nb DESC LIMIT 1
    """)
    return rows[0] if rows else (None, 0)


def agence_adresse():
    sql = """
        SELECT A.Cod_A, A.Telephone, A.Site_web,
        CONCAT(A.Adresse_Num_A, ' ', A.Adresse_Rue_A, ' - ', A.Adresse_Code_Postal, ' ', A.VILLE_Nom_Ville) 
        FROM AGENCE_DE_VOYAGE A ORDER BY A.Cod_A ASC
    """
    return fetch_query(sql)


def agence_par_ville(ville):
    sql = """
        SELECT A.Cod_A, A.Telephone, A.Site_web,
        CONCAT(A.Adresse_Num_A, ' ', A.Adresse_Rue_A, ' - ', A.Adresse_Code_Postal, ' ', A.VILLE_Nom_Ville)
        FROM AGENCE_DE_VOYAGE A WHERE A.VILLE_Nom_Ville = %s
    """
    return fetch_query(sql, (ville,))


def coords_agences():
    """
    Retourne un DataFrame propre pour st.map sans valeurs NULL.
    """
    sql = """
        SELECT V.Latitude as latitude, V.Longitude as longitude, A.Cod_A as id_agence
        FROM AGENCE_DE_VOYAGE A
        JOIN VILLE V ON A.VILLE_Nom_Ville = V.Nom_Ville
        WHERE V.Latitude IS NOT NULL AND V.Longitude IS NOT NULL
    """
    rows = fetch_query(sql)

    # Retourne un DataFrame vide avec les colonnes si aucun résultat
    if not rows:
        return pd.DataFrame(columns=['latitude', 'longitude'])

    df = pd.DataFrame(rows, columns=['latitude', 'longitude', 'id_agence'])

    # Conversion forcée en float pour éviter les erreurs Streamlit
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)

    return df