# Fichier : database/page_security.py

import streamlit as st


def check_authentication():
    """
    Vérifie si l'utilisateur est connecté.
    Si non, il redirige l'utilisateur vers la page principale (app.py)
    qui affichera l'écran de connexion.
    """
    # 1. Vérifiez si l'état de connexion est manquant ou False
    if "logged_in" not in st.session_state or st.session_state["logged_in"] is False:
        # 2. Afficher un message rapide (pour le débogage/l'utilisateur)
        st.error("Accès refusé. Veuillez vous connecter.")

        # 3. Rediriger vers la page principale (app.py)
        # Note: Streamlit considère le script principal comme le script d'entrée.
        st.switch_page("app.py")

        # 4. Arrêter l'exécution du reste du script de la page actuelle
        st.stop()