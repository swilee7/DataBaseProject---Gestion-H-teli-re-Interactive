-- create database projetbd5;
-- use projetbd5;
-- TABLE VILLE
CREATE TABLE VILLE (
    Nom_Ville      VARCHAR(100)  NOT NULL,
    Longitude      DECIMAL(9,6),
    Latitude       DECIMAL(9,6),
    Region         VARCHAR(100),
    Pays           VARCHAR(100),
    PRIMARY KEY (Nom_Ville)
) ENGINE=InnoDB;

-- TABLE AGENCE_DE_VOYAGE
CREATE TABLE AGENCE_DE_VOYAGE (
    Cod_A              INT         NOT NULL AUTO_INCREMENT,
    Site_web           VARCHAR(255),
    Telephone          VARCHAR(30),
    Adresse_Num_A      INT,
    Adresse_Pays_A     VARCHAR(100),
    Adresse_Rue_A      VARCHAR(255),
    Adresse_Code_Postal VARCHAR(20),
    VILLE_Nom_Ville    VARCHAR(100),
    Mot_Passe VARCHAR(255) NOT NULL,
    PRIMARY KEY (Cod_A),
    CONSTRAINT fk_agence_ville
        FOREIGN KEY (VILLE_Nom_Ville)
        REFERENCES VILLE (Nom_Ville)
        ON UPDATE CASCADE
        ON DELETE SET NULL
        
) ENGINE=InnoDB;

-- TABLE CHAMBRE (super-classe)
CREATE TABLE CHAMBRE (
    Cod_C    INT          NOT NULL AUTO_INCREMENT,
    Surface  DECIMAL(6,2),
    Etage int,
    Type varchar(255),
    PRIMARY KEY (Cod_C)
) ENGINE=InnoDB;
-- TABLE SUITE (spécialisation de CHAMBRE)
CREATE TABLE SUITE (
    CHAMBRE_Cod_C INT NOT NULL,
    PRIMARY KEY (CHAMBRE_Cod_C),
    CONSTRAINT fk_suite_chambre
        FOREIGN KEY (CHAMBRE_Cod_C)
        REFERENCES CHAMBRE (Cod_C)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- TABLE RESERVATION
CREATE TABLE RESERVATION (
    CHAMBRE_Cod_C         INT         NOT NULL,
    Date_debut            DATE        NOT NULL,
    Date_fin              DATE,
    Prix                  DECIMAL(10,2),
    AGENCE_DE_VOYAGE_Cod_A INT        NOT NULL,
    PRIMARY KEY (CHAMBRE_Cod_C, Date_debut),
    CONSTRAINT fk_reservation_chambre
        FOREIGN KEY (CHAMBRE_Cod_C)
        REFERENCES CHAMBRE (Cod_C)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_reservation_agence
        FOREIGN KEY (AGENCE_DE_VOYAGE_Cod_A)
        REFERENCES AGENCE_DE_VOYAGE (Cod_A)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- TABLE EQUIPEMENT (si tu veux la normaliser)
CREATE TABLE EQUIPEMENT (
    Equipement VARCHAR(100) NOT NULL,
    PRIMARY KEY (Equipement)
) ENGINE=InnoDB;

-- TABLE D’ASSOCIATION HAS_EQUIPEMENT (CHAMBRE–EQUIPEMENT)
CREATE TABLE HAS_EQUIPEMENT (
    CHAMBRE_Cod_C INT          NOT NULL,
    EQUIPEMENT_Equipement VARCHAR(100) NOT NULL,
    PRIMARY KEY (CHAMBRE_Cod_C, EQUIPEMENT_Equipement),
    CONSTRAINT fk_has_eq_chambre
        FOREIGN KEY (CHAMBRE_Cod_C)
        REFERENCES CHAMBRE (Cod_C)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_has_eq_equipement
        FOREIGN KEY (EQUIPEMENT_Equipement)
        REFERENCES EQUIPEMENT (Equipement)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- TABLE ESPACES_DISPO (si tu veux une table des types d’espaces)
CREATE TABLE ESPACES_DISPO (
    Espaces_Dispo VARCHAR(100) NOT NULL,
    PRIMARY KEY (Espaces_Dispo)
) ENGINE=InnoDB;

-- TABLE D’ASSOCIATION HAS_ESPACES_DISPO (SUITE–ESPACES_DISPO)
CREATE TABLE HAS_ESPACES_DISPO (
    SUITE_CHAMBRE_Cod_C INT          NOT NULL,
    ESPACES_DISPO_Espaces_Dispo VARCHAR(100) NOT NULL,
    PRIMARY KEY (SUITE_CHAMBRE_Cod_C, ESPACES_DISPO_Espaces_Dispo),
    CONSTRAINT fk_has_esp_suite
        FOREIGN KEY (SUITE_CHAMBRE_Cod_C)
        REFERENCES SUITE (CHAMBRE_Cod_C)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_has_esp_espace
        FOREIGN KEY (ESPACES_DISPO_Espaces_Dispo)
        REFERENCES ESPACES_DISPO (Espaces_Dispo)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;

create table support(
ID_Support int auto_increment primary key,
Nom_Client varchar (255) Not Null,
Email_Client varchar (255) Not Null,
Objet_Demande Varchar(255),
Message_Client text,
Date_Soumission DATETIME DEFAULT current_timestamp,
Statut_Traitement varchar(50) default 'Nouveau'
);