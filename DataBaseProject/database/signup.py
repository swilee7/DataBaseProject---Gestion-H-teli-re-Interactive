import streamlit as st
from .connection import create_connection, execute_query, fetch_query


def signup_agence():
    st.title("Créer un compte Agence")

    if st.button("J'ai déjà un compte"):
        st.session_state["show_signup"] = False
        st.rerun()
        return

    # Champs du formulaire
    Cod_A = st.number_input("Code agence (entier)",min_value=1,step=1)
    Site_web = st.text_input("Site web")
    Adresse_Rue_A = st.text_input("Rue")
    Adresse_Pays_A = st.text_input("Pays")
    Adresse_Num_A = st.number_input("Numéro", min_value=1, step=1)
    Adresse_Code_Postal = st.number_input("Code postal", min_value=10000, step=1)
    Telephone = st.number_input("Téléphone")
    VILLE_Nom_Ville = st.text_input("Ville")
    mot_passe = st.text_input("Mot de passe", type="password")
    mot_passe2 = st.text_input("Resaisir le mot de passe", type="password")

    if st.button("S'inscrire"):
        # Vérifier les champs obligatoires
        if not all([
            Cod_A,
            Site_web,
            Telephone,
            Adresse_Num_A,
            Adresse_Pays_A,
            Adresse_Rue_A,
            Adresse_Code_Postal,
            VILLE_Nom_Ville,
            mot_passe,
            mot_passe2,
        ]):
            st.warning("Veuillez remplir tous les champs obligatoires")
            return

        # Vérifier la confirmation de mot de passe
        if mot_passe != mot_passe2:
            st.error("Les mots de passe ne correspondent pas")
            return

        # Vérifier si le code agence existe déjà
        query_check = "SELECT Cod_A FROM AGENCE_DE_VOYAGE WHERE Cod_A = %s"
        result = fetch_query(query_check, (Cod_A,))
        if result:
            st.error(f"L'agence avec le code {Cod_A} existe déjà")
            return

        # Insérer la nouvelle agence
        query_insert = """
            INSERT INTO AGENCE_DE_VOYAGE
            (Cod_A, Site_web, Telephone,
             Adresse_Num_A, Adresse_Pays_A, Adresse_Rue_A,
             Adresse_Code_Postal, VILLE_Nom_Ville, mot_passe)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(
            query_insert,
            (
                Cod_A,
                Site_web,
                Telephone,
                Adresse_Num_A,
                Adresse_Pays_A,
                Adresse_Rue_A,
                Adresse_Code_Postal,
                VILLE_Nom_Ville,
                mot_passe,   # idéalement, stocker un hash ici
            ),
        )
        print('done')

        st.success("Agence créée avec succès ! Vous pouvez maintenant vous connecter.")
        st.session_state["show_signup"] = False
        st.rerun()
