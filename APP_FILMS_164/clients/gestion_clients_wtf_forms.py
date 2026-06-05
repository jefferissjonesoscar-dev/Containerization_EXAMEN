"""
    Fichier : gestion_clients_wtf_forms.py
    Auteur : OM 2021.03.22 - Adapté GUERID Rayan DEVA 1A
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Length, Optional


class FormWTFAjouterClient(FlaskForm):
    nom_client_wtf       = StringField("Nom du client", validators=[Length(min=2, max=100, message="min 2 max 100")])
    prenom_client_wtf    = StringField("Prénom du client", validators=[Length(min=2, max=100, message="min 2 max 100")])
    telephone_client_wtf = StringField("Téléphone", validators=[Optional(), Length(max=20)])
    email_client_wtf     = StringField("Email", validators=[Optional(), Length(max=150)])
    submit = SubmitField("Enregistrer client")


class FormWTFUpdateClient(FlaskForm):
    nom_client_update_wtf       = StringField("Nom du client", validators=[Length(min=2, max=100, message="min 2 max 100")])
    prenom_client_update_wtf    = StringField("Prénom du client", validators=[Length(min=2, max=100, message="min 2 max 100")])
    telephone_client_update_wtf = StringField("Téléphone", validators=[Optional(), Length(max=20)])
    email_client_update_wtf     = StringField("Email", validators=[Optional(), Length(max=150)])
    submit = SubmitField("Update client")


class FormWTFDeleteClient(FlaskForm):
    nom_client_delete_wtf = StringField("Effacer ce client")
    submit_btn_del        = SubmitField("Effacer client")
    submit_btn_conf_del   = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler    = SubmitField("Annuler")
