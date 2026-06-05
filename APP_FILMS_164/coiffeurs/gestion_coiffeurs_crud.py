"""Gestion des "routes" FLASK et des données pour les coiffeurs.
Fichier : gestion_coiffeurs_crud.py
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
from APP_FILMS_164.coiffeurs.gestion_coiffeurs_wtf_forms import FormWTFAjouterCoiffeur
from APP_FILMS_164.coiffeurs.gestion_coiffeurs_wtf_forms import FormWTFDeleteCoiffeur
from APP_FILMS_164.coiffeurs.gestion_coiffeurs_wtf_forms import FormWTFUpdateCoiffeur


@app.route("/coiffeurs_afficher/<string:order_by>/<int:id_coiffeur_sel>", methods=['GET', 'POST'])
def coiffeurs_afficher(order_by, id_coiffeur_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_coiffeur_sel == 0:
                    strsql_coiffeurs_afficher = """SELECT id_coiffeur, nom_coiffeur, prenom_coiffeur, specialite_coiffeur, date_ins_coiffeur FROM t_coiffeur ORDER BY id_coiffeur ASC"""
                    mc_afficher.execute(strsql_coiffeurs_afficher)
                elif order_by == "ASC":
                    valeur_id_coiffeur_selected_dictionnaire = {"value_id_coiffeur_selected": id_coiffeur_sel}
                    strsql_coiffeurs_afficher = """SELECT id_coiffeur, nom_coiffeur, prenom_coiffeur, specialite_coiffeur, date_ins_coiffeur FROM t_coiffeur WHERE id_coiffeur = %(value_id_coiffeur_selected)s"""
                    mc_afficher.execute(strsql_coiffeurs_afficher, valeur_id_coiffeur_selected_dictionnaire)
                else:
                    strsql_coiffeurs_afficher = """SELECT id_coiffeur, nom_coiffeur, prenom_coiffeur, specialite_coiffeur, date_ins_coiffeur FROM t_coiffeur ORDER BY id_coiffeur DESC"""
                    mc_afficher.execute(strsql_coiffeurs_afficher)

                data_coiffeurs = mc_afficher.fetchall()
                print("data_coiffeurs ", data_coiffeurs, " Type : ", type(data_coiffeurs))

                if not data_coiffeurs and id_coiffeur_sel == 0:
                    flash("""La table "t_coiffeur" est vide. !!""", "warning")
                elif not data_coiffeurs and id_coiffeur_sel > 0:
                    flash(f"Le coiffeur demandé n'existe pas !!", "warning")

        except Exception as Exception_coiffeurs_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{coiffeurs_afficher.__name__} ; "
                                          f"{Exception_coiffeurs_afficher}")

    return render_template("coiffeurs/coiffeurs_afficher.html", data=data_coiffeurs)


@app.route("/coiffeurs_ajouter", methods=['GET', 'POST'])
def coiffeurs_ajouter_wtf():
    form = FormWTFAjouterCoiffeur()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_coiffeur_wtf        = form.nom_coiffeur_wtf.data
                prenom_coiffeur_wtf     = form.prenom_coiffeur_wtf.data
                specialite_coiffeur_wtf = form.specialite_coiffeur_wtf.data

                valeurs_insertion_dictionnaire = {
                    "value_nom_coiffeur":        nom_coiffeur_wtf,
                    "value_prenom_coiffeur":     prenom_coiffeur_wtf,
                    "value_specialite_coiffeur": specialite_coiffeur_wtf,
                }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_coiffeur = """INSERT INTO t_coiffeur (nom_coiffeur, prenom_coiffeur, specialite_coiffeur) VALUES (%(value_nom_coiffeur)s, %(value_prenom_coiffeur)s, %(value_specialite_coiffeur)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_coiffeur, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                return redirect(url_for('coiffeurs_afficher', order_by='DESC', id_coiffeur_sel=0))

        except Exception as Exception_coiffeurs_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{coiffeurs_ajouter_wtf.__name__} ; "
                                            f"{Exception_coiffeurs_ajouter_wtf}")

    return render_template("coiffeurs/coiffeurs_ajouter_wtf.html", form=form)


@app.route("/coiffeur_update", methods=['GET', 'POST'])
def coiffeur_update_wtf():
    id_coiffeur_update = request.values['id_coiffeur_btn_edit_html']

    form_update = FormWTFUpdateCoiffeur()
    try:
        if request.method == "POST" and form_update.submit.data:
            nom_coiffeur_update        = form_update.nom_coiffeur_update_wtf.data
            prenom_coiffeur_update     = form_update.prenom_coiffeur_update_wtf.data
            specialite_coiffeur_update = form_update.specialite_coiffeur_update_wtf.data

            valeur_update_dictionnaire = {
                "value_id_coiffeur":         id_coiffeur_update,
                "value_nom_coiffeur":        nom_coiffeur_update,
                "value_prenom_coiffeur":     prenom_coiffeur_update,
                "value_specialite_coiffeur": specialite_coiffeur_update,
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_coiffeur = """UPDATE t_coiffeur SET nom_coiffeur = %(value_nom_coiffeur)s,
            prenom_coiffeur = %(value_prenom_coiffeur)s,
            specialite_coiffeur = %(value_specialite_coiffeur)s
            WHERE id_coiffeur = %(value_id_coiffeur)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_coiffeur, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            return redirect(url_for('coiffeurs_afficher', order_by="ASC", id_coiffeur_sel=id_coiffeur_update))
        elif request.method == "GET":
            str_sql_id_coiffeur = "SELECT id_coiffeur, nom_coiffeur, prenom_coiffeur, specialite_coiffeur FROM t_coiffeur WHERE id_coiffeur = %(value_id_coiffeur)s"
            valeur_select_dictionnaire = {"value_id_coiffeur": id_coiffeur_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_coiffeur, valeur_select_dictionnaire)
            data_nom_coiffeur = mybd_conn.fetchone()
            print("data_nom_coiffeur ", data_nom_coiffeur, " type ", type(data_nom_coiffeur))

            form_update.nom_coiffeur_update_wtf.data        = data_nom_coiffeur["nom_coiffeur"]
            form_update.prenom_coiffeur_update_wtf.data     = data_nom_coiffeur["prenom_coiffeur"]
            form_update.specialite_coiffeur_update_wtf.data = data_nom_coiffeur["specialite_coiffeur"]

    except Exception as Exception_coiffeur_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{coiffeur_update_wtf.__name__} ; "
                                      f"{Exception_coiffeur_update_wtf}")

    return render_template("coiffeurs/coiffeur_update_wtf.html", form_update=form_update)


@app.route("/coiffeur_delete", methods=['GET', 'POST'])
def coiffeur_delete_wtf():
    data_rdv_attribue_coiffeur_delete = None
    btn_submit_del = None
    id_coiffeur_delete = request.values['id_coiffeur_btn_delete_html']

    form_delete = FormWTFDeleteCoiffeur()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("coiffeurs_afficher", order_by="ASC", id_coiffeur_sel=0))

            if form_delete.submit_btn_conf_del.data:
                data_rdv_attribue_coiffeur_delete = session['data_rdv_attribue_coiffeur_delete']
                print("data_rdv_attribue_coiffeur_delete ", data_rdv_attribue_coiffeur_delete)
                flash(f"Effacer le coiffeur de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_coiffeur": id_coiffeur_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_rdv_coiffeur = """DELETE FROM t_rendez_vous WHERE fk_coiffeur = %(value_id_coiffeur)s"""
                str_sql_delete_coiffeur     = """DELETE FROM t_coiffeur WHERE id_coiffeur = %(value_id_coiffeur)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_rdv_coiffeur, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_coiffeur, valeur_delete_dictionnaire)

                flash(f"Coiffeur définitivement effacé !!", "success")
                print(f"Coiffeur définitivement effacé !!")

                return redirect(url_for('coiffeurs_afficher', order_by="ASC", id_coiffeur_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_coiffeur": id_coiffeur_delete}
            print(id_coiffeur_delete, type(id_coiffeur_delete))

            str_sql_coiffeurs_rdv_delete = """SELECT id_rdv, date_rdv FROM t_rendez_vous WHERE fk_coiffeur = %(value_id_coiffeur)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_coiffeurs_rdv_delete, valeur_select_dictionnaire)
                data_rdv_attribue_coiffeur_delete = mydb_conn.fetchall()
                print("data_rdv_attribue_coiffeur_delete...", data_rdv_attribue_coiffeur_delete)

                session['data_rdv_attribue_coiffeur_delete'] = data_rdv_attribue_coiffeur_delete

                str_sql_id_coiffeur = "SELECT id_coiffeur, nom_coiffeur, prenom_coiffeur FROM t_coiffeur WHERE id_coiffeur = %(value_id_coiffeur)s"
                mydb_conn.execute(str_sql_id_coiffeur, valeur_select_dictionnaire)
                data_nom_coiffeur = mydb_conn.fetchone()
                print("data_nom_coiffeur ", data_nom_coiffeur, " type ", type(data_nom_coiffeur))

            form_delete.nom_coiffeur_delete_wtf.data = data_nom_coiffeur["nom_coiffeur"]
            btn_submit_del = False

    except Exception as Exception_coiffeur_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{coiffeur_delete_wtf.__name__} ; "
                                      f"{Exception_coiffeur_delete_wtf}")

    return render_template("coiffeurs/coiffeur_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_rdv_associes=data_rdv_attribue_coiffeur_delete)
