import streamlit as st
import os
import pandas as pd  # Ajouté pour les futures métriques si besoin

# --- Configuration de la Page ---
st.set_page_config(
    page_title="Accueil",
    page_icon="🏠",
    layout="wide"
)

from database.page_security import check_authentication


# =================================================================
# 1. STYLE CSS CINÉMATIQUE
# =================================================================
def inject_cinematic_style():
    """
    Injecte le CSS pour le style général, le fond d'écran et
    l'effet de gradient sur les titres.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        .stApp {
            /* Fond d'écran cohérent */
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Poppins', sans-serif;
        }
        /* Style des titres en dégradé */
        h1, h2, h3 {
            background: -webkit-linear-gradient(45deg, #0984e3, #d63031);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        /* Style des conteneurs pour les images/cartes si vous en ajoutez */
        .stImage {
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        .group-member-list {
            list-style-type: none;
            padding: 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
        }
        .group-member-list li {
            background-color: #ffffff;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            font-weight: 600;
            color: #0984e3;
            text-align: center;
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
        unsafe_allow_html=True
    )


# =================================================================
# 2. FONCTION PRINCIPALE DE LA PAGE
# =================================================================

def page_home():
    # ⚠️ Injection du style au début de la fonction
    inject_cinematic_style()
    check_authentication()

    # =================================================================
    # 3. NOUVELLE SECTION : MEMBRES DU GROUPE
    # =================================================================
    st.subheader("Membres du Groupe Projet")
    # Liste des membres basée sur l'image fournie
    membres = [
        "ABRIK Hicham , BEKKALI Sara , ELHAMRI Amine , EL BOURIMI Fatima-zahra , EL FILALI Zouhayr , HANI HASNA , SAÏDI Safa"
    ]

    # Utilisation d'un markdown HTML pour une liste stylisée
    membres_html = "\n".join([f"<li>{membre}</li>" for membre in membres])
    st.markdown(f"<ul class='group-member-list'>{membres_html}</ul>", unsafe_allow_html=True)

    st.markdown("---")
    # 🔹 CONTENU
    st.title("🏠 Bienvenue sur DataBaseProject")
    st.markdown("---")

    # Utilisation de colonnes pour mieux présenter le texte et l'image
    col_text, col_img = st.columns([1.5, 1])

    with col_text:
        st.header("Découvrez l'expérience de voyage simplifiée")
        st.write(
            """
            Notre plateforme est dédiée à l'optimisation de la gestion des chambres 
            et des réservations pour nos agences partenaires. Accédez à des données 
            clés pour améliorer vos stratégies de vente et offrir un service client exceptionnel.
            """
        )
        st.write(
            """
            Grâce au menu de navigation latéral (à gauche), explorez rapidement les 
            statistiques de réservation, le catalogue des chambres et les informations sur nos agences.
            """
        )
        # Ajout d'une fausse métrique pour illustrer l'utilisation du design
        st.metric(label="Taux de satisfaction Agences", value="98.5%", delta="+0.2%")

    with col_img:
        st.subheader("Nos meilleures destinations")
        # Assurez-vous que l'image 'assets/default.jpg' existe
        image_path = os.path.join("assets", "hotel.png")

        # Utilisez le tag <img> pour appliquer le CSS de la classe .stImage si nécessaire
        try:
            st.image(image_path, caption="Voyagez avec nous", use_container_width=True)
        except FileNotFoundError:  # Ligne 108 (si vous comptez depuis le début)
            # 📌 ATTENTION : Cette ligne DOIT être indentée sous le 'except'
            st.warning("Image 'assets/default.jpg' introuvable. Veuillez la placer dans le dossier 'assets'.")

    st.markdown("---")  # 📌 Cette ligne NE DOIT PAS être indentée
    st.info("💡 Utilisez le menu latéral (à gauche) pour naviguer entre les fonctionnalités de l'application.")

    # ====================== FOOTER (AVEC SOCIAL MEDIA) ==========================
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


# Exécution de la page
if __name__ == "__main__":
    page_home()