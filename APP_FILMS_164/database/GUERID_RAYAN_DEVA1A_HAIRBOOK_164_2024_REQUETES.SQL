-- Projet     : HairBook - Gestion des rendez-vous pour salon de coiffure

USE GUERID_RAYAN_DEVA1A_HAIRBOOK_164_2024;


-- SECTION 1 : TABLE t_client

-- Afficher tous les clients triés par nom (ordre croissant)
SELECT id_client, nom_client, prenom_client, telephone_client, email_client, date_ins_client
FROM t_client
ORDER BY nom_client ASC;

-- Afficher un seul client en fonction de son identifiant
SELECT id_client, nom_client, prenom_client, telephone_client, email_client
FROM t_client
WHERE id_client = %(id_client)s;

-- Insérer un nouveau client
INSERT INTO t_client (nom_client, prenom_client, telephone_client, email_client)
VALUES (%(nom_client)s, %(prenom_client)s, %(telephone_client)s, %(email_client)s);

-- Mettre à jour un client existant
UPDATE t_client
SET nom_client        = %(nom_client)s,
    prenom_client     = %(prenom_client)s,
    telephone_client  = %(telephone_client)s,
    email_client      = %(email_client)s
WHERE id_client = %(id_client)s;

-- Supprimer un client
DELETE FROM t_client
WHERE id_client = %(id_client)s;

-- Vérifier si un client est associé à des rendez-vous avant suppression
SELECT id_rdv, date_rdv, heure_rdv
FROM t_rendez_vous
WHERE fk_client = %(fk_client)s;


-- SECTION 2 : TABLE t_coiffeur

-- Afficher tous les coiffeurs triés par nom (ordre croissant)
SELECT id_coiffeur, nom_coiffeur, prenom_coiffeur, specialite_coiffeur, date_ins_coiffeur
FROM t_coiffeur
ORDER BY nom_coiffeur ASC;

-- Afficher un seul coiffeur en fonction de son identifiant
SELECT id_coiffeur, nom_coiffeur, prenom_coiffeur, specialite_coiffeur
FROM t_coiffeur
WHERE id_coiffeur = %(id_coiffeur)s;

-- Insérer un nouveau coiffeur
INSERT INTO t_coiffeur (nom_coiffeur, prenom_coiffeur, specialite_coiffeur)
VALUES (%(nom_coiffeur)s, %(prenom_coiffeur)s, %(specialite_coiffeur)s);

-- Mettre à jour un coiffeur existant
UPDATE t_coiffeur
SET nom_coiffeur        = %(nom_coiffeur)s,
    prenom_coiffeur     = %(prenom_coiffeur)s,
    specialite_coiffeur = %(specialite_coiffeur)s
WHERE id_coiffeur = %(id_coiffeur)s;

-- Supprimer un coiffeur
DELETE FROM t_coiffeur
WHERE id_coiffeur = %(id_coiffeur)s;

-- Vérifier si un coiffeur est associé à des rendez-vous avant suppression
SELECT id_rdv, date_rdv, heure_rdv
FROM t_rendez_vous
WHERE fk_coiffeur = %(fk_coiffeur)s;


-- SECTION 3 : TABLE t_prestation

-- Afficher toutes les prestations triées par nom (ordre croissant)
SELECT id_prestation, nom_prestation, duree_prestation, prix_prestation, date_ins_prestation
FROM t_prestation
ORDER BY nom_prestation ASC;

-- Afficher une seule prestation en fonction de son identifiant
SELECT id_prestation, nom_prestation, duree_prestation, prix_prestation
FROM t_prestation
WHERE id_prestation = %(id_prestation)s;

-- Insérer une nouvelle prestation
INSERT INTO t_prestation (nom_prestation, duree_prestation, prix_prestation)
VALUES (%(nom_prestation)s, %(duree_prestation)s, %(prix_prestation)s);

-- Mettre à jour une prestation existante
UPDATE t_prestation
SET nom_prestation   = %(nom_prestation)s,
    duree_prestation = %(duree_prestation)s,
    prix_prestation  = %(prix_prestation)s
WHERE id_prestation = %(id_prestation)s;

-- Supprimer une prestation
DELETE FROM t_prestation
WHERE id_prestation = %(id_prestation)s;

-- Vérifier si une prestation est associée à des rendez-vous avant suppression
SELECT id_rdv, date_rdv, heure_rdv
FROM t_rendez_vous
WHERE fk_prestation = %(fk_prestation)s;


-- SECTION 4 : TABLE t_rendez_vous

-- Afficher tous les rendez-vous avec les infos client, coiffeur et prestation
SELECT rdv.id_rdv,
       rdv.date_rdv,
       rdv.heure_rdv,
       rdv.statut_rdv,
       rdv.retard_rdv,
       rdv.note_rdv,
       cli.nom_client,
       cli.prenom_client,
       coi.nom_coiffeur,
       coi.prenom_coiffeur,
       pre.nom_prestation,
       pre.prix_prestation
FROM t_rendez_vous rdv
JOIN t_client    cli ON rdv.fk_client    = cli.id_client
JOIN t_coiffeur  coi ON rdv.fk_coiffeur  = coi.id_coiffeur
JOIN t_prestation pre ON rdv.fk_prestation = pre.id_prestation
ORDER BY rdv.date_rdv ASC, rdv.heure_rdv ASC;

-- Afficher un seul rendez-vous avec toutes ses informations
SELECT rdv.id_rdv,
       rdv.date_rdv,
       rdv.heure_rdv,
       rdv.statut_rdv,
       rdv.retard_rdv,
       rdv.note_rdv,
       rdv.fk_client,
       rdv.fk_coiffeur,
       rdv.fk_prestation,
       cli.nom_client,
       cli.prenom_client,
       coi.nom_coiffeur,
       pre.nom_prestation
FROM t_rendez_vous rdv
JOIN t_client    cli ON rdv.fk_client    = cli.id_client
JOIN t_coiffeur  coi ON rdv.fk_coiffeur  = coi.id_coiffeur
JOIN t_prestation pre ON rdv.fk_prestation = pre.id_prestation
WHERE rdv.id_rdv = %(id_rdv)s;

-- Insérer un nouveau rendez-vous
INSERT INTO t_rendez_vous (date_rdv, heure_rdv, statut_rdv, retard_rdv, note_rdv, fk_client, fk_coiffeur, fk_prestation)
VALUES (%(date_rdv)s, %(heure_rdv)s, %(statut_rdv)s, %(retard_rdv)s, %(note_rdv)s,
        %(fk_client)s, %(fk_coiffeur)s, %(fk_prestation)s);

-- Mettre à jour un rendez-vous existant
UPDATE t_rendez_vous
SET date_rdv      = %(date_rdv)s,
    heure_rdv     = %(heure_rdv)s,
    statut_rdv    = %(statut_rdv)s,
    retard_rdv    = %(retard_rdv)s,
    note_rdv      = %(note_rdv)s,
    fk_client     = %(fk_client)s,
    fk_coiffeur   = %(fk_coiffeur)s,
    fk_prestation = %(fk_prestation)s
WHERE id_rdv = %(id_rdv)s;

-- Supprimer un rendez-vous
DELETE FROM t_rendez_vous
WHERE id_rdv = %(id_rdv)s;


-- SECTION 5 : REQUÊTES pour les listes déroulantes (SelectField WTF)

-- Liste de tous les clients
SELECT id_client, CONCAT(nom_client, ' ', prenom_client) AS nomcomplet_client
FROM t_client
ORDER BY nom_client ASC;

-- Liste de tous les coiffeurs
SELECT id_coiffeur, CONCAT(nom_coiffeur, ' ', prenom_coiffeur) AS nomcomplet_coiffeur
FROM t_coiffeur
ORDER BY nom_coiffeur ASC;

-- Liste de toutes les prestations
SELECT id_prestation, nom_prestation
FROM t_prestation
ORDER BY nom_prestation ASC;


-- SECTION 6 : REQUÊTES STATISTIQUES

-- Nombre de rendez-vous par coiffeur
SELECT coi.nom_coiffeur, coi.prenom_coiffeur, COUNT(rdv.id_rdv) AS nb_rdv
FROM t_coiffeur coi
LEFT JOIN t_rendez_vous rdv ON rdv.fk_coiffeur = coi.id_coiffeur
GROUP BY coi.id_coiffeur
ORDER BY nb_rdv DESC;

-- Chiffre d'affaires par prestation
SELECT pre.nom_prestation, COUNT(rdv.id_rdv) AS nb_rdv,
       SUM(pre.prix_prestation) AS chiffre_affaires
FROM t_prestation pre
LEFT JOIN t_rendez_vous rdv ON rdv.fk_prestation = pre.id_prestation
GROUP BY pre.id_prestation
ORDER BY chiffre_affaires DESC;

-- Rendez-vous confirmés pour une date donnée
SELECT rdv.date_rdv, rdv.heure_rdv,
       cli.nom_client, cli.prenom_client,
       coi.nom_coiffeur,
       pre.nom_prestation
FROM t_rendez_vous rdv
JOIN t_client    cli ON rdv.fk_client    = cli.id_client
JOIN t_coiffeur  coi ON rdv.fk_coiffeur  = coi.id_coiffeur
JOIN t_prestation pre ON rdv.fk_prestation = pre.id_prestation
WHERE rdv.statut_rdv = 'Confirmé'
  AND rdv.date_rdv = '2026-05-10'
ORDER BY rdv.heure_rdv ASC;
