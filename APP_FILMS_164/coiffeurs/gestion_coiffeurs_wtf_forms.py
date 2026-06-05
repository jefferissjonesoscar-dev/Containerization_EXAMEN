"""
    Fichier : gestion_coiffeurs_wtf_forms.py
    Auteur : OM 2021.03.22 - Adapté GUERID Rayan DEVA 1A
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Length, Optional


class FormWTFAjouterCoiffeur(FlaskForm):
    nom_coiffeur_wtf        = StringField("Nom du coiffeur", validators=[Length(min=2, max=100, message="min 2 max 100")])
    prenom_coiffeur_wtf     = StringField("Prénom du coiffeur", validators=[Length(min=2, max=100, message="min 2 max 100")])
    specialite_coiffeur_wtf = StringField("Spécialité", validators=[Optional(), Length(max=100)])
    submit = SubmitField("Enregistrer coiffeur")


class FormWTFUpdateCoiffeur(FlaskForm):
    nom_coiffeur_update_wtf        = StringField("Nom du coiffeur", validators=[Length(min=2, max=100, message="min 2 max 100")])
    prenom_coiffeur_update_wtf     = StringField("Prénom du coiffeur", validators=[Length(min=2, max=100, message="min 2 max 100")])
    specialite_coiffeur_update_wtf = StringField("Spécialité", validators=[Optional(), Length(max=100)])
    submit = SubmitField("Update coiffeur")


class FormWTFDeleteCoiffeur(FlaskForm):
    nom_coiffeur_delete_wtf = StringField("Effacer ce coiffeur")
    submit_btn_del          = SubmitField("Effacer coiffeur")
    submit_btn_conf_del     = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler      = SubmitField("Annuler")
