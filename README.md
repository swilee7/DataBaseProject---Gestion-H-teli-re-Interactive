# 🏨 DataBaseProject - Gestion Hôtelière Interactive

**DataBaseProject** est une application web complète développée dans le cadre du module **SI & SGBD**. Elle permet de gérer les chambres, les réservations et le support client d'une agence de voyages de manière centralisée et sécurisée.

## 👥 Membres du Groupe
* **ABRIK Hicham**
* **BEKKALI Sara**
* **ELHAMRI Amine**
* **EL BOURIMI Fatima-zahra**
* **EL FILALI Zouhayr**
* **HANI Hasna**
* **SAÏDI Safa**

## 🛠️ Technologies Utilisées
* **Interface (Front-End) :** Streamlit (Python)
* **Logique (Back-End) :** Python 3.10+
* **Base de Données :** MySQL Workbench
* **Connecteur :** mysql-connector-python

## 📂 Structure du Projet
Le projet est organisé de la manière suivante :
* `app.py` : Point d'entrée de l'application.
* `database/` : Fonctions SQL et logique de connexion (`connection.py`, `Chambre.py`, `Support.py`, etc.).
* `pages/` : Différentes interfaces de l'application (Accueil, Chambres, Réservations, etc.).
* `assets/` : Ressources visuelles (images).
* `creation.sql` : Script pour recréer la base de données et la table `SUPPORT`.

## 🚀 Installation et Lancement
1. **Cloner le projet :**
   ```bash
   git clone [https://github.com/votre-utilisateur/DataBaseProject.git](https://github.com/votre-utilisateur/DataBaseProject.git)
   cd DataBaseProject
Installer les dépendances :
   ```bash 
pip install -r requirements.txt
Configurer la base de données : Importez le fichier database/creation.sql dans MySQL Workbench et configurez vos accès dans database/connection.py.
Lancer l'application :
    ```bash
   streamlit run app.py

© 2025 - Réalisé sous l'encadrement de Mme Chaoui.
