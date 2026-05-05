# Fichier : app.py (Orchestrateur Principal & Sécurisé)

import streamlit as st
# ... (autres imports) ...
from database.login import login_agence

# --- CONFIGURATION INITIALE ---
st.set_page_config(
    page_title="DataBaseProject",
    page_icon="🏨",
    layout="wide"
)

# --- INITIALISATION DE L'ÉTAT DE SESSION ---
# =================================================================
# INITIALISATION DE L'ÉTAT DE SESSION
# =================================================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "User" not in st.session_state:
    st.session_state["User"] = ""
if "show_signup" not in st.session_state:
    st.session_state["show_signup"] = False
# =================================================================

# =================================================================
# LOGIQUE DE LANCEMENT SÉCURISÉE
# =================================================================

if st.session_state["logged_in"]:
    # 1. SI L'UTILISATEUR EST CONNECTÉ:
    # On redirige vers la VRAIE page d'accueil (qui affichera le menu latéral généré)
    # Assurez-vous que le nom du fichier est correct (ex: Accueil.py ou 1_Accueil.py)
    st.switch_page("pages/1_Accueil.py")

    # Si le fichier est dans le dossier pages/: st.switch_page("pages/1_Accueil.py")

else:
    # 2. SI L'UTILISATEUR N'EST PAS CONNECTÉ:

    # -----------------------------------------------------------------
    # NOUVEAU: INJECTION DE CSS POUR MASQUER LA BARRE LATÉRALE
    # -----------------------------------------------------------------
    st.markdown(
        """
        <style>
        /* Masque la barre latérale complète (où le menu de navigation apparaît) */
        section[data-testid="stSidebar"] {
            visibility: hidden;
            width: 0px; /* S'assure qu'elle ne prend pas de place */
        }
        /* Masque l'icône "ouvrir le menu" sur les petits écrans */
        .st-emotion-cache-1l02z88 {
            visibility: hidden;
        }
        /* Style de fond pour les pages d'authentification */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Affiche la page de connexion/inscription
    login_agence()