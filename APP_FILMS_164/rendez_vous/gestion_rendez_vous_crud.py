"""Gestion des "routes" FLASK et des données pour les rendez-vous.
Fichier : gestion_rendez_vous_crud.py
Auteur : OM 2021.03.16 - Adapté GUERID Rayan DEVA 1A
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.rendez_vous.gestion_rendez_vous_wtf_forms import FormWTFAjouterRendezVous
from APP_FILMS_164.rendez_vous.gestion_rendez_vous_wtf_forms import FormWTFDeleteRendezVous
from APP_FILMS_164.rendez_vous.gestion_rendez_vous_wtf_forms import FormWTFUpdateRendezVous


@app.route("/rendez_vous_afficher/<string:order_by>/<int:id_rdv_sel>", methods=['GET', 'POST'])
def rendez_vous_afficher(order_by, id_rdv_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_rdv_sel == 0:
                    strsql_rdv_afficher = """SELECT id_rdv, date_rdv, heure_rdv, statut_rdv, retard_rdv, note_rdv, date_ins_rdv, nom_client, prenom_client, nom_coiffeur, prenom_coiffeur, nom_prestation FROM t_rendez_vous JOIN t_client ON t_rendez_vous.fk_client = t_client.id_client JOIN t_coiffeur ON t_rendez_vous.fk_coiffeur = t_coiffeur.id_coiffeur JOIN t_prestation ON t_rendez_vous.fk_prestation = t_prestation.id_prestation ORDER BY id_rdv ASC"""
                    mc_afficher.execute(strsql_rdv_afficher)
                elif order_by == "ASC":
                    valeur_id_rdv_selected_dictionnaire = {"value_id_rdv_selected": id_rdv_sel}
                    strsql_rdv_afficher = """SELECT id_rdv, date_rdv, heure_rdv, statut_rdv, retard_rdv, note_rdv, date_ins_rdv, nom_client, prenom_client, nom_coiffeur, prenom_coiffeur, nom_prestation FROM t_rendez_vous JOIN t_client ON t_rendez_vous.fk_client = t_client.id_client JOIN t_coiffeur ON t_rendez_vous.fk_coiffeur = t_coiffeur.id_coiffeur JOIN t_prestation ON t_rendez_vous.fk_prestation = t_prestation.id_prestation WHERE id_rdv = %(value_id_rdv_selected)s"""
                    mc_afficher.execute(strsql_rdv_afficher, valeur_id_rdv_selected_dictionnaire)
                else:
                    strsql_rdv_afficher = """SELECT id_rdv, date_rdv, heure_rdv, statut_rdv, retard_rdv, note_rdv, date_ins_rdv, nom_client, prenom_client, nom_coiffeur, prenom_coiffeur, nom_prestation FROM t_rendez_vous JOIN t_client ON t_rendez_vous.fk_client = t_client.id_client JOIN t_coiffeur ON t_rendez_vous.fk_coiffeur = t_coiffeur.id_coiffeur JOIN t_prestation ON t_rendez_vous.fk_prestation = t_prestation.id_prestation ORDER BY id_rdv DESC"""
                    mc_afficher.execute(strsql_rdv_afficher)

                data_rdv = mc_afficher.fetchall()
                print("data_rdv ", data_rdv, " Type : ", type(data_rdv))

                if not data_rdv and id_rdv_sel == 0:
                    flash("""La table "t_rendez_vous" est vide. !!""", "warning")
                elif not data_rdv and id_rdv_sel > 0:
                    flash(f"Le rendez-vous demandé n'existe pas !!", "warning")

        except Exception as Exception_rdv_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{rendez_vous_afficher.__name__} ; "
                                          f"{Exception_rdv_afficher}")

    return render_template("rendez_vous/rendez_vous_afficher.html", data=data_rdv)


@app.route("/rendez_vous_ajouter", methods=['GET', 'POST'])
def rendez_vous_ajouter_wtf():
    form = FormWTFAjouterRendezVous()
    try:
        with DBconnection() as mc:
            mc.execute("SELECT id_client, nom_client, prenom_client FROM t_client ORDER BY nom_client ASC")
            data_clients = mc.fetchall()
            mc.execute("SELECT id_coiffeur, nom_coiffeur, prenom_coiffeur FROM t_coiffeur ORDER BY nom_coiffeur ASC")
            data_coiffeurs = mc.fetchall()
            mc.execute("SELECT id_prestation, nom_prestation FROM t_prestation ORDER BY nom_prestation ASC")
            data_prestations = mc.fetchall()

        form.fk_client_wtf.choices     = [(c['id_client'], f"{c['prenom_client']} {c['nom_client']}") for c in data_clients]
        form.fk_coiffeur_wtf.choices   = [(c['id_coiffeur'], f"{c['prenom_coiffeur']} {c['nom_coiffeur']}") for c in data_coiffeurs]
        form.fk_prestation_wtf.choices = [(p['id_prestation'], p['nom_prestation']) for p in data_prestations]

        if request.method == "POST" and form.validate_on_submit():
            valeurs_insertion_dictionnaire = {
                "value_date_rdv":      form.date_rdv_wtf.data,
                "value_heure_rdv":     form.heure_rdv_wtf.data,
                "value_statut_rdv":    form.statut_rdv_wtf.data,
                "value_retard_rdv":    form.retard_rdv_wtf.data,
                "value_note_rdv":      form.note_rdv_wtf.data,
                "value_fk_client":     form.fk_client_wtf.data,
                "value_fk_coiffeur":   form.fk_coiffeur_wtf.data,
                "value_fk_prestation": form.fk_prestation_wtf.data,
            }
            print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

            strsql_insert_rdv = """INSERT INTO t_rendez_vous (date_rdv, heure_rdv, statut_rdv, retard_rdv, note_rdv, fk_client, fk_coiffeur, fk_prestation) VALUES (%(value_date_rdv)s, %(value_heure_rdv)s, %(value_statut_rdv)s, %(value_retard_rdv)s, %(value_note_rdv)s, %(value_fk_client)s, %(value_fk_coiffeur)s, %(value_fk_prestation)s) """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(strsql_insert_rdv, valeurs_insertion_dictionnaire)

            flash(f"Données insérées !!", "success")
            print(f"Données insérées !!")

            return redirect(url_for('rendez_vous_afficher', order_by='DESC', id_rdv_sel=0))

    except Exception as Exception_rdv_ajouter_wtf:
        raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                        f"{rendez_vous_ajouter_wtf.__name__} ; "
                                        f"{Exception_rdv_ajouter_wtf}")

    return render_template("rendez_vous/rendez_vous_ajouter_wtf.html", form=form)


@app.route("/rendez_vous_update", methods=['GET', 'POST'])
def rendez_vous_update_wtf():
    id_rdv_update = request.values['id_rdv_btn_edit_html']

    form_update = FormWTFUpdateRendezVous()
    try:
        with DBconnection() as mc:
            mc.execute("SELECT id_client, nom_client, prenom_client FROM t_client ORDER BY nom_client ASC")
            data_clients = mc.fetchall()
            mc.execute("SELECT id_coiffeur, nom_coiffeur, prenom_coiffeur FROM t_coiffeur ORDER BY nom_coiffeur ASC")
            data_coiffeurs = mc.fetchall()
            mc.execute("SELECT id_prestation, nom_prestation FROM t_prestation ORDER BY nom_prestation ASC")
            data_prestations = mc.fetchall()

        form_update.fk_client_update_wtf.choices     = [(c['id_client'], f"{c['prenom_client']} {c['nom_client']}") for c in data_clients]
        form_update.fk_coiffeur_update_wtf.choices   = [(c['id_coiffeur'], f"{c['prenom_coiffeur']} {c['nom_coiffeur']}") for c in data_coiffeurs]
        form_update.fk_prestation_update_wtf.choices = [(p['id_prestation'], p['nom_prestation']) for p in data_prestations]

        if request.method == "POST" and form_update.submit.data:
            valeur_update_dictionnaire = {
                "value_id_rdv":        id_rdv_update,
                "value_date_rdv":      form_update.date_rdv_update_wtf.data,
                "value_heure_rdv":     form_update.heure_rdv_update_wtf.data,
                "value_statut_rdv":    form_update.statut_rdv_update_wtf.data,
                "value_retard_rdv":    form_update.retard_rdv_update_wtf.data,
                "value_note_rdv":      form_update.note_rdv_update_wtf.data,
                "value_fk_client":     form_update.fk_client_update_wtf.data,
                "value_fk_coiffeur":   form_update.fk_coiffeur_update_wtf.data,
                "value_fk_prestation": form_update.fk_prestation_update_wtf.data,
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_rdv = """UPDATE t_rendez_vous SET date_rdv = %(value_date_rdv)s,
            heure_rdv = %(value_heure_rdv)s,
            statut_rdv = %(value_statut_rdv)s,
            retard_rdv = %(value_retard_rdv)s,
            note_rdv = %(value_note_rdv)s,
            fk_client = %(value_fk_client)s,
            fk_coiffeur = %(value_fk_coiffeur)s,
            fk_prestation = %(value_fk_prestation)s
            WHERE id_rdv = %(value_id_rdv)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_rdv, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            return redirect(url_for('rendez_vous_afficher', order_by="ASC", id_rdv_sel=id_rdv_update))
        elif request.method == "GET":
            str_sql_id_rdv = "SELECT id_rdv, date_rdv, heure_rdv, statut_rdv, retard_rdv, note_rdv, fk_client, fk_coiffeur, fk_prestation FROM t_rendez_vous WHERE id_rdv = %(value_id_rdv)s"
            valeur_select_dictionnaire = {"value_id_rdv": id_rdv_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_rdv, valeur_select_dictionnaire)
            data_nom_rdv = mybd_conn.fetchone()
            print("data_nom_rdv ", data_nom_rdv, " type ", type(data_nom_rdv))

            form_update.date_rdv_update_wtf.data      = data_nom_rdv["date_rdv"]
            form_update.heure_rdv_update_wtf.data     = data_nom_rdv["heure_rdv"]
            form_update.statut_rdv_update_wtf.data    = data_nom_rdv["statut_rdv"]
            form_update.retard_rdv_update_wtf.data    = data_nom_rdv["retard_rdv"]
            form_update.note_rdv_update_wtf.data      = data_nom_rdv["note_rdv"]
            form_update.fk_client_update_wtf.data     = data_nom_rdv["fk_client"]
            form_update.fk_coiffeur_update_wtf.data   = data_nom_rdv["fk_coiffeur"]
            form_update.fk_prestation_update_wtf.data = data_nom_rdv["fk_prestation"]

    except Exception as Exception_rdv_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{rendez_vous_update_wtf.__name__} ; "
                                      f"{Exception_rdv_update_wtf}")

    return render_template("rendez_vous/rendez_vous_update_wtf.html", form_update=form_update)


@app.route("/rendez_vous_delete", methods=['GET', 'POST'])
def rendez_vous_delete_wtf():
    data_rdv_delete = None
    btn_submit_del = None
    id_rdv_delete = request.values['id_rdv_btn_delete_html']

    form_delete = FormWTFDeleteRendezVous()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("rendez_vous_afficher", order_by="ASC", id_rdv_sel=0))

            if form_delete.submit_btn_conf_del.data:
                data_rdv_delete = session['data_rdv_delete']
                print("data_rdv_delete ", data_rdv_delete)
                flash(f"Effacer le rendez-vous de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_rdv": id_rdv_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_rdv = """DELETE FROM t_rendez_vous WHERE id_rdv = %(value_id_rdv)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_rdv, valeur_delete_dictionnaire)

                flash(f"Rendez-vous définitivement effacé !!", "success")
                print(f"Rendez-vous définitivement effacé !!")

                return redirect(url_for('rendez_vous_afficher', order_by="ASC", id_rdv_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_rdv": id_rdv_delete}
            print(id_rdv_delete, type(id_rdv_delete))

            str_sql_rdv_delete = """SELECT id_rdv, date_rdv, heure_rdv, statut_rdv, nom_client, prenom_client, nom_coiffeur, prenom_coiffeur, nom_prestation FROM t_rendez_vous JOIN t_client ON t_rendez_vous.fk_client = t_client.id_client JOIN t_coiffeur ON t_rendez_vous.fk_coiffeur = t_coiffeur.id_coiffeur JOIN t_prestation ON t_rendez_vous.fk_prestation = t_prestation.id_prestation WHERE id_rdv = %(value_id_rdv)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_rdv_delete, valeur_select_dictionnaire)
                data_rdv_delete = mydb_conn.fetchall()
                print("data_rdv_delete...", data_rdv_delete)

                session['data_rdv_delete'] = data_rdv_delete

            form_delete.info_rdv_delete_wtf.data = f"RDV #{id_rdv_delete}"
            btn_submit_del = False

    except Exception as Exception_rdv_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{rendez_vous_delete_wtf.__name__} ; "
                                      f"{Exception_rdv_delete_wtf}")

    return render_template("rendez_vous/rendez_vous_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_rdv_delete=data_rdv_delete)
