# app/2_Chambres.py (Mise à jour pour la stabilité des types)

# On appelle les outils magiques de Python pour construire notre application.
import streamlit as st  # L'outil principal qui fait apparaître les boutons et les images.
import pandas as pd  # L'outil pour gérer les grandes listes de données (les tableaux).
import os  # L'outil pour parler aux dossiers de l'ordinateur.
import sys  # L'outil pour les choses très techniques.

# On dit à l'ordinateur où sont rangés tous les autres fichiers importants du projet.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
from database.page_security import check_authentication
# --- 1. CONFIGURATION DE LA PAGE ---
# On donne un joli titre à notre page et une petite icône de lit (🛏️).
st.set_page_config(layout="wide", page_title="Chambres", page_icon="🛏️")

# --- 2. IMPORTS DES FONCTIONS BACKEND ---
# On va chercher les fonctions qui parlent à la base de données (le grand classeur de l'hôtel).
from database.Chambre import get_chambres_filtrees, get_all_equipements


# =================================================================
# 3. STYLE CSS CINÉMATIQUE
# =================================================================
def inject_cinematic_style():
    """
    C'est la partie qui met des jolies couleurs et des belles formes
    à toute l'application, comme un décor de film !
    """
    st.markdown(
        """
        <style>
        /* ... Le code secret des couleurs et des formes ... */
        .stApp {
            /* On met un fond avec une belle couleur dégradée. */
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Poppins', sans-serif;
        }
        h1, h2, h3 {
            /* Les titres sont super brillants et colorés. */
            background: -webkit-linear-gradient(45deg, #0984e3, #d63031);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        /* Style des cartes de chambres */
        .room-card {
            /* Chaque chambre a une belle carte blanche avec une ombre. */
            background-color: rgba(255, 255, 255, 0.7);
            border-left: 5px solid #0984e3;
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
# 4. FONCTION PRINCIPALE DE LA PAGE
# =================================================================

def page_chambres():
    # On met le beau style qu'on a préparé.
    inject_cinematic_style()
    check_authentication()

    # --- HEADER ---
    # Le grand titre de la page, comme sur une affiche.
    st.title("🛏️ Catalogue des Chambres")
    st.markdown(
        """
        <p style="font-size:1.1rem; color:#636e72;">
        Utilisez les filtres ci-dessous pour trouver la chambre parfaite.
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    # ====================== SIDEBAR ET FILTRES ==========================
    # Une petite boîte sur le côté pour choisir ce qu'on cherche.
    st.sidebar.header("🔎 Filtres de Recherche")

    # On demande à la base de données quels équipements sont disponibles (Wi-Fi, etc.).
    equipements_options = get_all_equipements()

    # On peut choisir le type de chambre (Simple, Double, Triple, Suite).
    type_chambre = st.sidebar.radio(
        "Type de chambre",
        ["Toutes", "Simple", "Double", "Triple", "Suite"],
        key='chambre_type'
    )

    # On peut cocher plusieurs petits plus qu'on veut (comme le Mini-bar).
    equipements_selectionnes = st.sidebar.multiselect(
        "Équipements supplémentaires",
        options=[eq for eq in equipements_options if eq != 'Cuisine'],
        key='equipements_select'
    )

    # Une case à cocher pour dire si on veut une cuisine ou non.
    cuisine = st.sidebar.checkbox("Présence d'une Cuisine", key='cuisine_check')

    # --- Appel de la fonction de recherche ---

    # Quand on appuie sur le gros bouton magique "Afficher les Chambres"...
    if st.sidebar.button("Afficher les Chambres", type="primary"):
        # ... on se souvient de nos choix pour la recherche.
        st.session_state['show_results_chambre'] = True
        st.session_state['filtres_complets'] = {
            'type': type_chambre,
            'equipements': equipements_selectionnes,
            'cuisine': cuisine
        }

    # On démarre sans montrer de résultats au début.
    if 'show_results_chambre' not in st.session_state:
        st.session_state['show_results_chambre'] = False

    # ====================== LOGIQUE D'AFFICHAGE DES RÉSULTATS ==========================

    # Si on a appuyé sur le bouton de recherche, on continue ici !
    if st.session_state['show_results_chambre']:

        # On se souvient des choix qu'on a faits (type, équipements...).
        filtres = st.session_state.get('filtres_complets', {
            'type': type_chambre,
            'equipements': equipements_selectionnes,
            'cuisine': cuisine
        })

        # On demande à la base de données (le grand classeur) de chercher les chambres.
        with st.spinner(f"Recherche de chambres {filtres['type']}..."):
            df_chambres = get_chambres_filtrees(
                type_chambre=filtres['type'],
                equipements=filtres['equipements'],
                cuisine=filtres['cuisine']
            )

        if df_chambres.empty:
            # Si le classeur ne trouve rien.
            st.warning("Aucune chambre ne correspond aux critères de recherche spécifiés.")
        else:
            # Super, on dit combien de chambres on a trouvées !
            st.success(f"✅ {len(df_chambres)} chambre(s) trouvée(s) !")

            # On crée deux onglets : un pour le tableau, un pour les photos.
            tab_tableau, tab_detail = st.tabs(["📋 Tableau des Résultats", "🖼️ Aperçu Détaillé (Top 5)"])

            with tab_tableau:
                st.subheader("Résultats Complètes")
                # On montre la liste de toutes les chambres trouvées dans un tableau.
                df_display = df_chambres.rename(columns={
                    'Cod_C': 'Code Chambre',
                    'Surface': 'Superficie (m²)',
                    'Etage': 'Étage',
                    'Nom_Ville': 'Ville',
                    'Type': 'Type de Chambre'
                })
                st.dataframe(df_display, use_container_width=True, hide_index=True)

            with tab_detail:
                st.subheader("Aperçu Détaillé des Chambres (max 5)")

                # On affiche les photos des 5 premières chambres trouvées.
                for index, row in df_chambres.head(5).iterrows():

                    # On associe le type de chambre (Simple, Double...) à un nom de fichier image.
                    image_map = {
                        'Simple': "simple.jpg",
                        'Double': "double.jpg",
                        'Triple': "triple.jpg",
                        'Suite': "suite.jpg",
                    }
                    img_file = image_map.get(row['Type'], "default.jpg")
                    image_path = os.path.join(BASE_DIR, "assets", img_file)

                    # On divise l'espace en deux colonnes : Infos (2) et Image (1).
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        # On écrit les informations importantes de la chambre.
                        st.markdown(f"<div class='room-card'>", unsafe_allow_html=True)
                        st.markdown(f"**Code chambre** : {row['Cod_C']}")
                        st.markdown(f"**Ville** : {row['Nom_Ville']}")
                        st.markdown(f"**Surface** : {row['Surface']} m²")
                        st.markdown(f"**Étage** : {row['Etage']}")
                        st.markdown(f"**Type** : <span style='color:#d63031; font-weight:600;'>{row['Type']}</span>",
                                    unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                    with col2:
                        # On affiche la photo !
                        if os.path.exists(image_path):
                            # On met la photo bien grande (300 pixels de large) !
                            st.image(image_path, width=300, caption=row['Type'])
                        else:
                            # Si la photo n'est pas là, on nous dit qu'elle manque.
                            st.warning(f"Image {img_file} manquante")

    st.markdown("---")

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


# Pour lancer directement cette page :
if __name__ == "__main__":
    page_chambres()