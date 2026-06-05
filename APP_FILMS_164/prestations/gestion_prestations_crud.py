"""Gestion des "routes" FLASK et des données pour les prestations.
Fichier : gestion_prestations_crud.py
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
from APP_FILMS_164.prestations.gestion_prestations_wtf_forms import FormWTFAjouterPrestation
from APP_FILMS_164.prestations.gestion_prestations_wtf_forms import FormWTFDeletePrestation
from APP_FILMS_164.prestations.gestion_prestations_wtf_forms import FormWTFUpdatePrestation


@app.route("/prestations_afficher/<string:order_by>/<int:id_prestation_sel>", methods=['GET', 'POST'])
def prestations_afficher(order_by, id_prestation_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_prestation_sel == 0:
                    strsql_prestations_afficher = """SELECT id_prestation, nom_prestation, duree_prestation, prix_prestation, date_ins_prestation FROM t_prestation ORDER BY id_prestation ASC"""
                    mc_afficher.execute(strsql_prestations_afficher)
                elif order_by == "ASC":
                    valeur_id_prestation_selected_dictionnaire = {"value_id_prestation_selected": id_prestation_sel}
                    strsql_prestations_afficher = """SELECT id_prestation, nom_prestation, duree_prestation, prix_prestation, date_ins_prestation FROM t_prestation WHERE id_prestation = %(value_id_prestation_selected)s"""
                    mc_afficher.execute(strsql_prestations_afficher, valeur_id_prestation_selected_dictionnaire)
                else:
                    strsql_prestations_afficher = """SELECT id_prestation, nom_prestation, duree_prestation, prix_prestation, date_ins_prestation FROM t_prestation ORDER BY id_prestation DESC"""
                    mc_afficher.execute(strsql_prestations_afficher)

                data_prestations = mc_afficher.fetchall()
                print("data_prestations ", data_prestations, " Type : ", type(data_prestations))

                if not data_prestations and id_prestation_sel == 0:
                    flash("""La table "t_prestation" est vide. !!""", "warning")
                elif not data_prestations and id_prestation_sel > 0:
                    flash(f"La prestation demandée n'existe pas !!", "warning")

        except Exception as Exception_prestations_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{prestations_afficher.__name__} ; "
                                          f"{Exception_prestations_afficher}")

    return render_template("prestations/prestations_afficher.html", data=data_prestations)


@app.route("/prestations_ajouter", methods=['GET', 'POST'])
def prestations_ajouter_wtf():
    form = FormWTFAjouterPrestation()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_prestation_wtf   = form.nom_prestation_wtf.data
                duree_prestation_wtf = form.duree_prestation_wtf.data
                prix_prestation_wtf  = form.prix_prestation_wtf.data

                valeurs_insertion_dictionnaire = {
                    "value_nom_prestation":   nom_prestation_wtf,
                    "value_duree_prestation": duree_prestation_wtf,
                    "value_prix_prestation":  prix_prestation_wtf,
                }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_prestation = """INSERT INTO t_prestation (nom_prestation, duree_prestation, prix_prestation) VALUES (%(value_nom_prestation)s, %(value_duree_prestation)s, %(value_prix_prestation)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_prestation, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                return redirect(url_for('prestations_afficher', order_by='DESC', id_prestation_sel=0))

        except Exception as Exception_prestations_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{prestations_ajouter_wtf.__name__} ; "
                                            f"{Exception_prestations_ajouter_wtf}")

    return render_template("prestations/prestations_ajouter_wtf.html", form=form)


@app.route("/prestation_update", methods=['GET', 'POST'])
def prestation_update_wtf():
    id_prestation_update = request.values['id_prestation_btn_edit_html']

    form_update = FormWTFUpdatePrestation()
    try:
        if request.method == "POST" and form_update.submit.data:
            nom_prestation_update   = form_update.nom_prestation_update_wtf.data
            duree_prestation_update = form_update.duree_prestation_update_wtf.data
            prix_prestation_update  = form_update.prix_prestation_update_wtf.data

            valeur_update_dictionnaire = {
                "value_id_prestation":   id_prestation_update,
                "value_nom_prestation":  nom_prestation_update,
                "value_duree_prestation": duree_prestation_update,
                "value_prix_prestation": prix_prestation_update,
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_prestation = """UPDATE t_prestation SET nom_prestation = %(value_nom_prestation)s,
            duree_prestation = %(value_duree_prestation)s,
            prix_prestation = %(value_prix_prestation)s
            WHERE id_prestation = %(value_id_prestation)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_prestation, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            return redirect(url_for('prestations_afficher', order_by="ASC", id_prestation_sel=id_prestation_update))
        elif request.method == "GET":
            str_sql_id_prestation = "SELECT id_prestation, nom_prestation, duree_prestation, prix_prestation FROM t_prestation WHERE id_prestation = %(value_id_prestation)s"
            valeur_select_dictionnaire = {"value_id_prestation": id_prestation_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_prestation, valeur_select_dictionnaire)
            data_nom_prestation = mybd_conn.fetchone()
            print("data_nom_prestation ", data_nom_prestation, " type ", type(data_nom_prestation))

            form_update.nom_prestation_update_wtf.data   = data_nom_prestation["nom_prestation"]
            form_update.duree_prestation_update_wtf.data = data_nom_prestation["duree_prestation"]
            form_update.prix_prestation_update_wtf.data  = data_nom_prestation["prix_prestation"]

    except Exception as Exception_prestation_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{prestation_update_wtf.__name__} ; "
                                      f"{Exception_prestation_update_wtf}")

    return render_template("prestations/prestation_update_wtf.html", form_update=form_update)


@app.route("/prestation_delete", methods=['GET', 'POST'])
def prestation_delete_wtf():
    data_rdv_attribue_prestation_delete = None
    btn_submit_del = None
    id_prestation_delete = request.values['id_prestation_btn_delete_html']

    form_delete = FormWTFDeletePrestation()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("prestations_afficher", order_by="ASC", id_prestation_sel=0))

            if form_delete.submit_btn_conf_del.data:
                data_rdv_attribue_prestation_delete = session['data_rdv_attribue_prestation_delete']
                print("data_rdv_attribue_prestation_delete ", data_rdv_attribue_prestation_delete)
                flash(f"Effacer la prestation de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_prestation": id_prestation_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_rdv_prestation = """DELETE FROM t_rendez_vous WHERE fk_prestation = %(value_id_prestation)s"""
                str_sql_delete_prestation     = """DELETE FROM t_prestation WHERE id_prestation = %(value_id_prestation)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_rdv_prestation, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_prestation, valeur_delete_dictionnaire)

                flash(f"Prestation définitivement effacée !!", "success")
                print(f"Prestation définitivement effacée !!")

                return redirect(url_for('prestations_afficher', order_by="ASC", id_prestation_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_prestation": id_prestation_delete}
            print(id_prestation_delete, type(id_prestation_delete))

            str_sql_prestations_rdv_delete = """SELECT id_rdv, date_rdv FROM t_rendez_vous WHERE fk_prestation = %(value_id_prestation)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_prestations_rdv_delete, valeur_select_dictionnaire)
                data_rdv_attribue_prestation_delete = mydb_conn.fetchall()
                print("data_rdv_attribue_prestation_delete...", data_rdv_attribue_prestation_delete)

                session['data_rdv_attribue_prestation_delete'] = data_rdv_attribue_prestation_delete

                str_sql_id_prestation = "SELECT id_prestation, nom_prestation FROM t_prestation WHERE id_prestation = %(value_id_prestation)s"
                mydb_conn.execute(str_sql_id_prestation, valeur_select_dictionnaire)
                data_nom_prestation = mydb_conn.fetchone()
                print("data_nom_prestation ", data_nom_prestation, " type ", type(data_nom_prestation))

            form_delete.nom_prestation_delete_wtf.data = data_nom_prestation["nom_prestation"]
            btn_submit_del = False

    except Exception as Exception_prestation_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{prestation_delete_wtf.__name__} ; "
                                      f"{Exception_prestation_delete_wtf}")

    return render_template("prestations/prestation_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_rdv_associes=data_rdv_attribue_prestation_delete)
