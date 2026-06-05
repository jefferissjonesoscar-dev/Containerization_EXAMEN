-- Base de données HairBook - Gestion des rendez-vous pour salon de coiffure

DROP DATABASE IF EXISTS GUERID_RAYAN_DEVA1A_HAIRBOOK_164_2024;
CREATE DATABASE IF NOT EXISTS GUERID_RAYAN_DEVA1A_HAIRBOOK_164_2024
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE GUERID_RAYAN_DEVA1A_HAIRBOOK_164_2024;

-- Table : t_client
CREATE TABLE IF NOT EXISTS t_client (
    id_client         INT NOT NULL AUTO_INCREMENT,
    nom_client        VARCHAR(100) NOT NULL,
    prenom_client     VARCHAR(100) NOT NULL,
    telephone_client  VARCHAR(20),
    email_client      VARCHAR(150),
    date_ins_client   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_client)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table : t_coiffeur
CREATE TABLE IF NOT EXISTS t_coiffeur (
    id_coiffeur         INT NOT NULL AUTO_INCREMENT,
    nom_coiffeur        VARCHAR(100) NOT NULL,
    prenom_coiffeur     VARCHAR(100) NOT NULL,
    specialite_coiffeur VARCHAR(100),
    date_ins_coiffeur   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_coiffeur)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table : t_prestation
CREATE TABLE IF NOT EXISTS t_prestation (
    id_prestation       INT NOT NULL AUTO_INCREMENT,
    nom_prestation      VARCHAR(100) NOT NULL,
    duree_prestation    INT NOT NULL COMMENT 'Durée en minutes',
    prix_prestation     DECIMAL(8,2) NOT NULL,
    date_ins_prestation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_prestation)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table : t_rendez_vous
CREATE TABLE IF NOT EXISTS t_rendez_vous (
    id_rdv            INT NOT NULL AUTO_INCREMENT,
    date_rdv          DATE NOT NULL,
    heure_rdv         TIME NOT NULL,
    statut_rdv        VARCHAR(20) DEFAULT 'En attente',
    retard_rdv        INT DEFAULT 0 COMMENT 'Retard en minutes',
    note_rdv          VARCHAR(255),
    date_ins_rdv      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fk_client         INT NOT NULL,
    fk_coiffeur       INT NOT NULL,
    fk_prestation     INT NOT NULL,
    PRIMARY KEY (id_rdv),
    CONSTRAINT fk_rdv_client     FOREIGN KEY (fk_client)    REFERENCES t_client(id_client),
    CONSTRAINT fk_rdv_coiffeur   FOREIGN KEY (fk_coiffeur)  REFERENCES t_coiffeur(id_coiffeur),
    CONSTRAINT fk_rdv_prestation FOREIGN KEY (fk_prestation) REFERENCES t_prestation(id_prestation)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Données de test : t_client
INSERT INTO t_client (nom_client, prenom_client, telephone_client, email_client) VALUES
('Dupont',   'Marie',   '021 123 45 67', 'marie.dupont@email.ch'),
('Martin',   'Jean',    '021 234 56 78', 'jean.martin@email.ch'),
('Rochat',   'Sophie',  '021 345 67 89', 'sophie.rochat@email.ch'),
('Favre',    'Lucas',   '021 456 78 90', 'lucas.favre@email.ch'),
('Müller',   'Emma',    '021 567 89 01', 'emma.muller@email.ch');

-- Données de test : t_coiffeur
INSERT INTO t_coiffeur (nom_coiffeur, prenom_coiffeur, specialite_coiffeur) VALUES
('Bernasconi', 'Laura',   'Coloriste'),
('Fontaine',   'Marc',    'Barbier'),
('Girardin',   'Céline',  'Coupe femme'),
('Humbert',    'Patrick', 'Coupe homme');

-- Données de test : t_prestation
INSERT INTO t_prestation (nom_prestation, duree_prestation, prix_prestation) VALUES
('Coupe femme',        45, 55.00),
('Coupe homme',        30, 35.00),
('Coloration complète', 120, 120.00),
('Mèches',             90, 95.00),
('Brushing',           30, 40.00),
('Barbe',              20, 25.00);

-- Données de test : t_rendez_vous
INSERT INTO t_rendez_vous (date_rdv, heure_rdv, statut_rdv, retard_rdv, note_rdv, fk_client, fk_coiffeur, fk_prestation) VALUES
('2026-05-10', '09:00', 'Confirmé',   0,  NULL,                1, 1, 1),
('2026-05-10', '10:00', 'Confirmé',   0,  'Client fidèle',     2, 2, 2),
('2026-05-12', '14:00', 'En attente', 0,  NULL,                3, 3, 3),
('2026-05-13', '11:00', 'Confirmé',  10,  'Retard signalé',    4, 4, 6),
('2026-05-15', '09:30', 'Annulé',     0,  'Annulé par client', 5, 1, 5);
