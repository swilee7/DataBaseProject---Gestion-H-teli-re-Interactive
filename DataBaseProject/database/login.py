import streamlit as st
import os
from .connection import fetch_query,create_connection
from .signup import signup_agence




# =================================================================
# 1. STYLE CSS CINÉMATIQUE (Copie des autres pages + style Login)
# =================================================================
def inject_cinematic_style():
    """Injecte le CSS global pour les pages, adapté ici pour le login."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        .stApp {
            font-family: 'Poppins', sans-serif;
            /* Le fond d'écran est géré par main_app.py */
        }
        /* Titres pour le gradient */
        h1, h2, h3 {
            background: -webkit-linear-gradient(45deg, #0984e3, #d63031);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        /* Footer */
        .app-footer {
            position: fixed; /* Fixe le footer en bas */
            bottom: 0;
            left: 0;
            width: 100%;
            padding: 15px 0;
            border-top: 1px solid #ccc;
            text-align: center;
            color: #636e72;
            font-size: 0.9rem;
            background-color: rgba(255, 255, 255, 0.8); /* Fond clair pour qu'il soit lisible */
            backdrop-filter: blur(5px);
            z-index: 100;
        }
        .social-links {
            margin-bottom: 10px;
        }
        .social-links a {
            color: #0984e3;
            margin: 0 15px;
            font-size: 1.5rem;
            text-decoration: none;
            transition: color 0.2s ease;
        }
        .social-links a:hover {
            color: #d63031;
        }
        /* Style spécifique pour le conteneur de login (Glassmorphism sur l'image de fond) */
        .login-container {
            background-color: rgba(255, 255, 255, 0.85); /* Semi-transparent */
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.4);
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def login_agence():
    # 2. Injection du style au début
    inject_cinematic_style()

    if st.session_state["show_signup"]:
        signup_agence()
        return

    # 3. Utiliser le conteneur stylisé pour le formulaire
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    # Remplacer l'ancien header stylisé par un h2 qui utilise le CSS de gradient
    st.markdown('<h2 style="text-align:center;">Connexion Agence</h2>', unsafe_allow_html=True)

    Cod_A = st.number_input("Code agence", min_value=1)
    mot_passe = st.text_input("Mot de passe", type="password")

    col1, col2 = st.columns([2, 3])

    with col1:
        if st.button("Se connecter 🔑"):
            # On recherche l’agence par son code
            query = "SELECT Cod_A, mot_passe FROM AGENCE_DE_VOYAGE WHERE Cod_A = %s"
            result = fetch_query(query, (Cod_A,))

            if result:
                db_cod_a, db_mot_passe = result[0]
                if mot_passe == db_mot_passe:
                    st.session_state["logged_in"] = True
                    st.session_state["User"] = db_cod_a
                    st.success(f"Connexion réussie pour l'agence {db_cod_a} ✅")

                    # Redirection immédiate
                    st.rerun()

                else:
                    st.error("Mot de passe incorrect ❌")
            else:
                st.error("Code agence introuvable ❌")

    with col2:
        if st.button("Créer un nouveau compte 📝"):
            st.session_state["show_signup"] = True
            st.rerun()

    # Fermer le conteneur de login
    st.markdown('</div>', unsafe_allow_html=True)

    # ====================== FOOTER ==========================
    # Le footer est positionné en bas de manière fixe
    st.markdown(
        """
        <div class="app-footer">
            <div class="social-links">
                <a href="#" target="_blank">
                    <span style="color: #3b5998;">📘</span> Facebook
                </a>
                <a href="#" target="_blank">
                    <span style="color: #c13584;">📸</span> Instagram
                </a>
                <a href="#" target="_blank">
                    <span style="color: #0077b5;">🔗</span> LinkedIn
                </a>
            </div>
            <p style="margin-top: 10px;">© 2025 - DataBaseProject | Connexion Agence | Tous droits réservés.</p>
        </div>
        """,
        unsafe_allow_html=True
    )