# app/5_Contact.py

import streamlit as st
import os
import sys

# Ajustement du chemin pour l'import des dépendances (database, etc.)
# Ceci permet d'importer correctement les modules du dossier 'database'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
from database.page_security import check_authentication
# --- 2. IMPORTS DES FONCTIONS BACKEND ---
# Assurez-vous d'avoir créé le fichier database/Support.py et la fonction insert_contact_message
try:
    from database.Support import insert_contact_message
except ImportError:
    st.error(
        "Erreur: Le fichier 'database/Support.py' ou la fonction 'insert_contact_message' est introuvable. Veuillez vérifier votre backend.")


    # On définit une fonction mock pour éviter un crash si l'import échoue
    def insert_contact_message(nom, email, objet, message):
        return False

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Contact", page_icon="📞")


# =================================================================
# 3. STYLE CSS CINÉMATIQUE (COPIÉ/COLLÉ pour garantir la cohérence)
# =================================================================
def inject_cinematic_style():
    """Injecte le CSS pour le glassmorphism, les animations, centre le menu et style le footer."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        .stApp {
            font-family: 'Poppins', sans-serif;
            /* Si vous voulez un arrière-plan coloré comme 4_Agences.py, décommentez: */
            /* background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); */
        }
        /* Style pour centrer le menu */
        div[data-testid="stRadio"] {
            width: fit-content;
            margin: 0 auto;
        }
        div[data-testid="stRadio"] > label { 
            display: none;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] {
            background-color: rgba(255, 255, 255, 0.7);
            padding: 5px 10px;
            border-radius: 30px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
        }
        /* Titres */
        h1, h2, h3 {
            background: -webkit-linear-gradient(45deg, #0984e3, #d63031);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        /* Footer */
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
            color: #0984e3;
            margin: 0 15px;
            font-size: 1.5rem;
            text-decoration: none;
            transition: color 0.2s ease;
        }
        .social-links a:hover {
            color: #d63031;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =================================================================
# 4. FONCTION DE LA PAGE CONTACT
# =================================================================

def page_contact():
    # 1. Injection du style
    inject_cinematic_style()
    check_authentication()
    # --- HEADER ---
    st.title("📞 Contactez-nous")
    st.markdown(
        """
        <p style="font-size:1.1rem; color:#636e72;">
        Nous sommes là pour répondre à toutes vos questions.
        Remplissez le formulaire ci-dessous et notre équipe vous recontactera rapidement.
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    # =================================================================
    # STRUCTURE DU FORMULAIRE DE CONTACT
    # =================================================================

    col_form, col_info = st.columns([1, 1.5])

    with col_form:
        st.subheader("✉️ Formulaire de Requête")

        # Le formulaire est défini avec st.form
        with st.form(key='contact_form', clear_on_submit=True):

            # Champ Nom
            nom = st.text_input("Votre Nom Complet", placeholder="Ex: Dupont Jean")

            # Champ Email
            email = st.text_input("Votre Email", placeholder="Ex: jean.dupont@exemple.com")

            # Champ Objet (Selectbox pour la catégorisation)
            objet = st.selectbox(
                "Objet de votre demande",
                ["Informations générales", "Support technique", "Suggestion/Feedback", "Partenariat commercial"]
            )

            # Champ Message (Text Area)
            message = st.text_area("Votre Message", placeholder="Veuillez détailler votre requête ici...", height=150)

            # Bouton de Soumission
            submitted = st.form_submit_button("Envoyer le Message", type="primary")

        if submitted:
            # Logique de validation simple
            if not nom or not email or not message:
                st.error("Veuillez remplir tous les champs obligatoires.")
            else:
                # -------------------------------------------------------------
                # APPEL DE LA FONCTION BACKEND POUR SAUVEGARDER
                # -------------------------------------------------------------
                # Afficher un indicateur de chargement
                with st.spinner("Envoi du message et enregistrement dans la base de données..."):
                    if insert_contact_message(nom, email, objet, message):
                        st.success(f"Message de {nom} envoyé avec succès ! Il a été enregistré pour traitement.")
                    else:
                        st.error(
                            "Une erreur s'est produite lors de l'enregistrement de votre message. Veuillez réessayer (vérifiez la connexion à la base de données).")

    with col_info:
        st.subheader("🌐 Informations Utiles")
        st.info(
            """
            Si votre requête est urgente, vous pouvez nous joindre directement :

            * **Téléphone :** +212 5 XX XX XX XX
            * **Heures de bureau :** Lun - Ven, 9h00 - 18h00 (GMT+1)
            """
        )

        st.markdown("### 📍 Notre Localisation Principale")
        st.warning(
            "Note : Le point sur la carte est une localisation générique. Veuillez prendre rendez-vous avant de vous déplacer.")

        # Carte simplifiée (exemple de coordonnées pour le Maroc - Casablanca)
        coords = {'lat': [33.5731], 'lon': [-7.5898]}
        st.map(coords, zoom=10, use_container_width=True)

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


# Pour lancer directement cette page :
if __name__ == "__main__":
    page_contact()