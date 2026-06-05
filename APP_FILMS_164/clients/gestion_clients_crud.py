"""Gestion des "routes" FLASK et des données pour les clients.
Fichier : gestion_clients_crud.py
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
from APP_FILMS_164.clients.gestion_clients_wtf_forms import FormWTFAjouterClient
from APP_FILMS_164.clients.gestion_clients_wtf_forms import FormWTFDeleteClient
from APP_FILMS_164.clients.gestion_clients_wtf_forms import FormWTFUpdateClient


@app.route("/clients_afficher/<string:order_by>/<int:id_client_sel>", methods=['GET', 'POST'])
def clients_afficher(order_by, id_client_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_client_sel == 0:
                    strsql_clients_afficher = """SELECT id_client, nom_client, prenom_client, telephone_client, email_client, date_ins_client FROM t_client ORDER BY id_client ASC"""
                    mc_afficher.execute(strsql_clients_afficher)
                elif order_by == "ASC":
                    valeur_id_client_selected_dictionnaire = {"value_id_client_selected": id_client_sel}
                    strsql_clients_afficher = """SELECT id_client, nom_client, prenom_client, telephone_client, email_client, date_ins_client FROM t_client WHERE id_client = %(value_id_client_selected)s"""
                    mc_afficher.execute(strsql_clients_afficher, valeur_id_client_selected_dictionnaire)
                else:
                    strsql_clients_afficher = """SELECT id_client, nom_client, prenom_client, telephone_client, email_client, date_ins_client FROM t_client ORDER BY id_client DESC"""
                    mc_afficher.execute(strsql_clients_afficher)

                data_clients = mc_afficher.fetchall()
                print("data_clients ", data_clients, " Type : ", type(data_clients))

                if not data_clients and id_client_sel == 0:
                    flash("""La table "t_client" est vide. !!""", "warning")
                elif not data_clients and id_client_sel > 0:
                    flash(f"Le client demandé n'existe pas !!", "warning")

        except Exception as Exception_clients_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{clients_afficher.__name__} ; "
                                          f"{Exception_clients_afficher}")

    return render_template("clients/clients_afficher.html", data=data_clients)


@app.route("/clients_ajouter", methods=['GET', 'POST'])
def clients_ajouter_wtf():
    form = FormWTFAjouterClient()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_client_wtf       = form.nom_client_wtf.data
                prenom_client_wtf    = form.prenom_client_wtf.data
                telephone_client_wtf = form.telephone_client_wtf.data
                email_client_wtf     = form.email_client_wtf.data

                valeurs_insertion_dictionnaire = {
                    "value_nom_client":       nom_client_wtf,
                    "value_prenom_client":    prenom_client_wtf,
                    "value_telephone_client": telephone_client_wtf,
                    "value_email_client":     email_client_wtf,
                }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_client = """INSERT INTO t_client (nom_client, prenom_client, telephone_client, email_client) VALUES (%(value_nom_client)s, %(value_prenom_client)s, %(value_telephone_client)s, %(value_email_client)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_client, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                return redirect(url_for('clients_afficher', order_by='DESC', id_client_sel=0))

        except Exception as Exception_clients_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{clients_ajouter_wtf.__name__} ; "
                                            f"{Exception_clients_ajouter_wtf}")

    return render_template("clients/clients_ajouter_wtf.html", form=form)


@app.route("/client_update", methods=['GET', 'POST'])
def client_update_wtf():
    id_client_update = request.values['id_client_btn_edit_html']

    form_update = FormWTFUpdateClient()
    try:
        if request.method == "POST" and form_update.submit.data:
            nom_client_update       = form_update.nom_client_update_wtf.data
            prenom_client_update    = form_update.prenom_client_update_wtf.data
            telephone_client_update = form_update.telephone_client_update_wtf.data
            email_client_update     = form_update.email_client_update_wtf.data

            valeur_update_dictionnaire = {
                "value_id_client":        id_client_update,
                "value_nom_client":       nom_client_update,
                "value_prenom_client":    prenom_client_update,
                "value_telephone_client": telephone_client_update,
                "value_email_client":     email_client_update,
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_client = """UPDATE t_client SET nom_client = %(value_nom_client)s,
            prenom_client = %(value_prenom_client)s,
            telephone_client = %(value_telephone_client)s,
            email_client = %(value_email_client)s
            WHERE id_client = %(value_id_client)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_client, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            return redirect(url_for('clients_afficher', order_by="ASC", id_client_sel=id_client_update))
        elif request.method == "GET":
            str_sql_id_client = "SELECT id_client, nom_client, prenom_client, telephone_client, email_client FROM t_client WHERE id_client = %(value_id_client)s"
            valeur_select_dictionnaire = {"value_id_client": id_client_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_client, valeur_select_dictionnaire)
            data_nom_client = mybd_conn.fetchone()
            print("data_nom_client ", data_nom_client, " type ", type(data_nom_client))

            form_update.nom_client_update_wtf.data       = data_nom_client["nom_client"]
            form_update.prenom_client_update_wtf.data    = data_nom_client["prenom_client"]
            form_update.telephone_client_update_wtf.data = data_nom_client["telephone_client"]
            form_update.email_client_update_wtf.data     = data_nom_client["email_client"]

    except Exception as Exception_client_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{client_update_wtf.__name__} ; "
                                      f"{Exception_client_update_wtf}")

    return render_template("clients/client_update_wtf.html", form_update=form_update)


@app.route("/client_delete", methods=['GET', 'POST'])
def client_delete_wtf():
    data_rdv_attribue_client_delete = None
    btn_submit_del = None
    id_client_delete = request.values['id_client_btn_delete_html']

    form_delete = FormWTFDeleteClient()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("clients_afficher", order_by="ASC", id_client_sel=0))

            if form_delete.submit_btn_conf_del.data:
                data_rdv_attribue_client_delete = session['data_rdv_attribue_client_delete']
                print("data_rdv_attribue_client_delete ", data_rdv_attribue_client_delete)
                flash(f"Effacer le client de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_client": id_client_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_rdv_client = """DELETE FROM t_rendez_vous WHERE fk_client = %(value_id_client)s"""
                str_sql_delete_client     = """DELETE FROM t_client WHERE id_client = %(value_id_client)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_rdv_client, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_client, valeur_delete_dictionnaire)

                flash(f"Client définitivement effacé !!", "success")
                print(f"Client définitivement effacé !!")

                return redirect(url_for('clients_afficher', order_by="ASC", id_client_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_client": id_client_delete}
            print(id_client_delete, type(id_client_delete))

            str_sql_clients_rdv_delete = """SELECT id_rdv, date_rdv FROM t_rendez_vous WHERE fk_client = %(value_id_client)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_clients_rdv_delete, valeur_select_dictionnaire)
                data_rdv_attribue_client_delete = mydb_conn.fetchall()
                print("data_rdv_attribue_client_delete...", data_rdv_attribue_client_delete)

                session['data_rdv_attribue_client_delete'] = data_rdv_attribue_client_delete

                str_sql_id_client = "SELECT id_client, nom_client, prenom_client FROM t_client WHERE id_client = %(value_id_client)s"
                mydb_conn.execute(str_sql_id_client, valeur_select_dictionnaire)
                data_nom_client = mydb_conn.fetchone()
                print("data_nom_client ", data_nom_client, " type ", type(data_nom_client))

            form_delete.nom_client_delete_wtf.data = data_nom_client["nom_client"]
            btn_submit_del = False

    except Exception as Exception_client_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{client_delete_wtf.__name__} ; "
                                      f"{Exception_client_delete_wtf}")

    return render_template("clients/client_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_rdv_associes=data_rdv_attribue_client_delete)
