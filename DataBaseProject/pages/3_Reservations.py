# Fichier : DataBaseProject/app/3_Reservations.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# --- CONFIGURATION DES CHEMINS ---
# Permet l'import des modules du dossier 'database'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# --- IMPORTS DES FONCTIONS BACKEND ---
from database.Reservation import get_reservations_stats
from database.page_security import check_authentication
# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Réservations", page_icon="📈")


# =================================================================
# 2. STYLE CSS CINÉMATIQUE (Pour uniformité)
# =================================================================
def inject_cinematic_style():
    """Injecte le CSS pour le style général et le menu horizontal."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Poppins', sans-serif;
        }
        h1, h2, h3 {
            background: -webkit-linear-gradient(45deg, #0984e3, #d63031);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        /* Style des boutons radio pour le menu */
        div[data-testid="stRadio"] { width: fit-content; margin: 0 auto; }
        div[data-testid="stRadio"] > label { display: none; }
        div[data-testid="stRadio"] div[role="radiogroup"] {
            background-color: rgba(255, 255, 255, 0.7);
            padding: 5px 10px;
            border-radius: 30px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
        }
         /* ... Le reste du code de style ... */
        /* Footer */
        .app-footer {
            /* Le petit coin d'informations tout en bas de la page. */
            margin-top: 50px;
        }
           /* 3. FOOTER STYLE & SOCIAL MEDIA */
        .app-footer {
            margin-top: 50px;
            padding: 15px 0;
            border-top: 1px solid #ccc;
            text-align: center;
            color: #636e72;
            font-size: 0.9rem;
        }
        .social-links {
            margin-bottom: 10px;
        }
        .social-links a {
            color: #0984e3; /* Couleur principale */
            margin: 0 15px;
            font-size: 1.5rem; /* Augmenté pour les icônes */
            text-decoration: none;
            transition: color 0.2s ease;
        }
        .social-links a:hover {
            color: #d63031; /* Couleur au survol */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =================================================================
# 3. FONCTION PRINCIPALE DE LA PAGE
# =================================================================
def page_reservations():
    inject_cinematic_style()
    check_authentication()
    # --------- MENU HAUT (Logique de redirection) ---------
    # choix_page = st.radio(
    #     "Navigation",
    #     ["Accueil", "Chambres", "Réservation", "Agence", "Contact"],
    #     horizontal=True,
    #     key="res_nav_radio"
    # )
    #
    # # Redirections (avec les chemins simples dans le dossier 'app/')
    # if choix_page == "Accueil":
    #     st.switch_page("1_Accueil.py")
    # elif choix_page == "Chambres":
    #     st.switch_page("2_Chambres.py")
    # elif choix_page == "Réservation":
    #     pass  # On reste sur cette page
    # elif choix_page == "Agence":
    #     st.switch_page("4_Agences.py")
    # elif choix_page == "Contact":
    #     st.switch_page("5_Contact.py")
    #
    # st.markdown("---")  # Séparateur visuel après le menu

    # --- CONTENU DE LA PAGE ---
    st.title("📈 Analyse des Réservations")
    st.markdown("Cette page affiche les tendances et le coût moyen des chambres par mois.")

    # 1. APPEL DE LA FONCTION BACKEND (récupère une liste de tuples)
    rows = get_reservations_stats()

    # 2. CONVERSION EN DATAFRAME DANS LE FRONTEND
    if rows:
        df_res = pd.DataFrame(rows, columns=[
            'Cod_C', 'Surface', 'Type', 'Mois', 'Prix_Moyen'
        ])
    else:
        df_res = pd.DataFrame()  # DataFrame vide si pas de résultats

    if not df_res.empty:
        st.success(f"✅ Données de réservations chargées pour {len(df_res)} entrées uniques.")

        # 1. Chambre la plus chère par mois
        st.subheader("Chambre ayant le coût journalier moyen le plus élevé par mois")

        # Grouper et trouver l'index du prix max pour chaque mois
        df_max_index = df_res.groupby('Mois')['Prix_Moyen'].idxmax()
        df_max = df_res.loc[df_max_index].sort_values(by='Mois')

        st.dataframe(
            df_max[['Mois', 'Cod_C', 'Surface', 'Type', 'Prix_Moyen']],
            use_container_width=True,
            hide_index=True
        )

        # 2. Graphique évolution du prix moyen par mois
        st.subheader("Évolution du coût journalier moyen au fil des mois")
        df_avg_month = df_res.groupby('Mois')['Prix_Moyen'].mean().reset_index()

        # Création et affichage du graphique Matplotlib
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df_avg_month['Mois'], df_avg_month['Prix_Moyen'], marker='o', color='blue')

        # Afficher les étiquettes de l'axe X correctement
        ax.set_xticks(df_avg_month['Mois'])
        ax.set_xticklabels(df_avg_month['Mois'], rotation=45, ha='right')

        ax.set_xlabel("Mois")
        ax.set_ylabel("Prix journalier moyen (€)")
        ax.set_title("Évolution du prix moyen par mois")
        ax.grid(True)
        st.pyplot(fig)

    else:
        st.warning("Aucune donnée de réservation disponible.")

    st.markdown("---")

    # ====================== FOOTER ==========================
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
<p>© 2025 - DataBaseProject | Réalisé dans le cadre du cours de SI & SGBD</p>        </div>
        """,
        unsafe_allow_html=True
    )


# Point d'entrée
if __name__ == "__main__":
    page_reservations()