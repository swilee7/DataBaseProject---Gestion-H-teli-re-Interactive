from .connection import fetch_query, execute_query
import pandas as pd
import warnings

# ====================================================================
# 1. RÉCUPÉRATION DES ESPACES DISPONIBLES (Table ESPACES_DISPO)
# ====================================================================
def get_all_espaces():
    """
    Récupère la liste unique des espaces (bathroom, cuisine, etc.)
    depuis la table ESPACES_DISPO.
    """
    sql = "SELECT Espaces_Dispo FROM ESPACES_DISPO ORDER BY Espaces_Dispo ASC"
    try:
        rows = fetch_query(sql)
        # Retourne la liste (ex: ['bathroom', 'cuisine', 'dining room'])
        return [row[0] for row in rows] if rows else []
    except Exception as e:
        print(f"Erreur lors de la récupération des espaces: {e}")
        # Valeurs de secours basées sur votre capture d'écran
        return ["bathroom", "chambre à choucher", "cuisine", "dining room"]

# ====================================================================
# 2. FONCTION DE FILTRAGE DES CHAMBRES (ADAPTÉE À VOTRE SCHÉMA SQL)
# ====================================================================
def get_chambres_filtrees(type_chambre=None, equipements=None, cuisine=False, espaces=None):
    """
    Récupère les chambres filtrées selon le type, les équipements et les espaces.
    La cuisine est traitée comme un espace selon votre nouvelle structure.
    """
    if equipements is None: equipements = []
    if espaces is None: espaces = []

    # Si la case 'cuisine' est cochée, on l'ajoute à la liste des espaces à filtrer
    if cuisine and 'cuisine' not in espaces:
        espaces.append('cuisine')

    # Requête de base avec jointure pour récupérer la ville
    base_query = """
        SELECT 
            C.Cod_C, 
            C.Etage,
            C.Surface,
            (
                SELECT V.Nom_Ville
                FROM RESERVATION R
                JOIN AGENCE_DE_VOYAGE A ON R.AGENCE_DE_VOYAGE_Cod_A = A.Cod_A
                JOIN VILLE V ON A.VILLE_Nom_Ville = V.Nom_Ville
                WHERE R.CHAMBRE_Cod_C = C.Cod_C
                LIMIT 1
            ) AS Nom_Ville,
            C.Type
        FROM CHAMBRE C
    """

    conditions = []

    # 1. Filtrage par Type
    if type_chambre and type_chambre != "Toutes":
        safe_type = str(type_chambre).lower().replace("'", "''")
        conditions.append(f"LOWER(C.Type) = '{safe_type}'")

    # 2. Filtrage par Espaces (inclut la cuisine) via HAS_ESPACES_DISPO
    if espaces:
        for esp in espaces:
            safe_esp = str(esp).replace("'", "''")
            # On utilise la table d'association définie dans votre SQL
            conditions.append(f"""
                C.Cod_C IN (
                    SELECT SUITE_CHAMBRE_Cod_C 
                    FROM HAS_ESPACES_DISPO 
                    WHERE ESPACES_DISPO_Espaces_Dispo = '{safe_esp}'
                )
            """)

    # 3. Filtrage par équipements via HAS_EQUIPEMENT
    if equipements:
        for eq in equipements:
            safe_eq = str(eq).replace("'", "''")
            conditions.append(f"""
                C.Cod_C IN (
                    SELECT CHAMBRE_Cod_C 
                    FROM HAS_EQUIPEMENT 
                    WHERE EQUIPEMENT_Equipement = '{safe_eq}'
                )
            """)

    # Construction de la requête finale
    final_query = base_query
    if conditions:
        final_query += " WHERE " + " AND ".join(conditions)

    final_query += " ORDER BY C.Cod_C ASC"

    try:
        rows = fetch_query(final_query)
    except Exception as e:
        print(f"Erreur d'exécution SQL: {e}")
        rows = []

    if not rows:
        return pd.DataFrame()

    columns = ["Cod_C", "Etage", "Surface", "Nom_Ville", "Type"]
    return pd.DataFrame(rows, columns=columns)

# ====================================================================
# 3. RÉCUPÉRATION DES ÉQUIPEMENTS
# ====================================================================
def get_all_equipements():
    """Récupère les équipements depuis la table EQUIPEMENT."""
    sql = "SELECT Equipement FROM EQUIPEMENT ORDER BY Equipement ASC"
    try:
        rows = fetch_query(sql)
        return [row[0] for row in rows] if rows else []
    except Exception as e:
        print(f"Erreur équipements: {e}")
        return ["WiFi", "Climatisation", "Mini-bar", "Balcon"]