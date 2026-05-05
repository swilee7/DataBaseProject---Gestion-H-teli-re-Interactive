import streamlit as st
import pandas as pd

# Import de sécurité
from database.page_security import check_authentication
# Import des fonctions spécifiques aux agences depuis votre module backend
from database.Agence import (
    agences_distinct,
    villes_distinctes,
    ville_plus_agences,
    agence_adresse,
    agence_par_ville,
    coords_agences
)

# --- Configuration de la Page ---
st.set_page_config(
    page_title="Agences",
    page_icon="✈️",
    layout="wide"
)


# =================================================================
# 1. STYLE CSS
# =================================================================
def inject_cinematic_style():
    st.markdown(
        """
        <style>
        h1, h2, h3 {
            background: -webkit-linear-gradient(45deg, #0984e3, #d63031);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        [data-testid="stMetricValue"] { font-size: 2.5rem; }
        .app-footer {
            margin-top: 50px;
            padding: 15px 0;
            border-top: 1px solid #ccc;
            text-align: center;
            color: #636e72;
            font-size: 0.9rem;
        }
        .social-links a {
            color: #0984e3;
            margin: 0 15px;
            font-size: 1.2rem;
            text-decoration: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =================================================================
# 2. FONCTION PRINCIPALE
# =================================================================

def page_agences():
    # SÉCURITÉ
    check_authentication()
    inject_cinematic_style()

    st.title("✈️ Nos Agences Partenaires")
    st.markdown('<p style="color:#636e72;">Visualisez les informations clés de nos partenaires.</p>',
                unsafe_allow_html=True)
    st.markdown("---")

    # --- 1. RÉCUPÉRATION DES MÉTRIQUES ---
    nb_agences = agences_distinct()
    nb_villes = villes_distinctes()
    ville_max_tuple = ville_plus_agences()

    col_met1, col_met2, col_met3 = st.columns(3)
    with col_met1:
        st.metric("Agences", value=int(nb_agences))
    with col_met2:
        st.metric("Villes", value=int(nb_villes))
    with col_met3:
        nom_v = ville_max_tuple[0] if ville_max_tuple[0] else "N/A"
        st.metric("Top Ville", value=nom_v, delta=f"{int(ville_max_tuple[1])} Agences")

    st.markdown("---")

    # --- 2. CARTE GÉOGRAPHIQUE (CORRECTION ValueError) ---
    st.subheader("📍 Localisation des Agences")

    # Récupère le DataFrame préparé par le backend
    map_df = coords_agences()

    # CORRECTION : Utilisation de .empty pour éviter ValueError
    if not map_df.empty:
        # st.map utilise automatiquement les colonnes 'latitude' et 'longitude'
        st.map(map_df, zoom=5)
    else:
        st.warning("Aucune coordonnée (Latitude/Longitude) n'est renseignée dans la table VILLE pour ces agences.")

    st.markdown("---")

    # --- 3. FILTRES ET TABLEAU ---
    with st.expander("🔎 Filtrer les Agences par Ville"):
        city_filter = st.text_input("Rechercher une ville", placeholder="Ex: Casablanca...").strip()

    st.subheader("Liste Détaillée")

    # Logique de filtrage
    if city_filter:
        agence_rows = agence_par_ville(city_filter)
    else:
        agence_rows = agence_adresse()

    if agence_rows:
        columns = ['Code Agence', 'Téléphone', 'Site Web', 'Adresse Complète']
        df_display = pd.DataFrame(agence_rows, columns=columns)
        st.dataframe(df_display, use_container_width=True)
    elif city_filter:
        st.info(f"Aucune agence trouvée à **{city_filter}**.")
    else:
        st.info("La base de données est vide.")

    # --- FOOTER ---
    st.markdown(
        """
        <div class="app-footer">
            <div class="social-links">
                <a href="#">📘 Facebook</a>
                <a href="#">📸 Instagram</a>
                <a href="#">🔗 LinkedIn</a>
            </div>
            <p>© 2025 - DataBaseProject | Cours de SI & SGBD</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    page_agences()