"""
    Fichier : gestion_prestations_wtf_forms.py
    Auteur : OM 2021.03.22 - Adapté GUERID Rayan DEVA 1A
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField
from wtforms import SubmitField
from wtforms.validators import Length, NumberRange


class FormWTFAjouterPrestation(FlaskForm):
    nom_prestation_wtf   = StringField("Nom de la prestation", validators=[Length(min=2, max=100, message="min 2 max 100")])
    duree_prestation_wtf = IntegerField("Durée (minutes)", validators=[NumberRange(min=1, max=999, message="min 1 max 999")])
    prix_prestation_wtf  = DecimalField("Prix (CHF)", places=2, validators=[NumberRange(min=0, message="Prix invalide")])
    submit = SubmitField("Enregistrer prestation")


class FormWTFUpdatePrestation(FlaskForm):
    nom_prestation_update_wtf   = StringField("Nom de la prestation", validators=[Length(min=2, max=100, message="min 2 max 100")])
    duree_prestation_update_wtf = IntegerField("Durée (minutes)", validators=[NumberRange(min=1, max=999, message="min 1 max 999")])
    prix_prestation_update_wtf  = DecimalField("Prix (CHF)", places=2, validators=[NumberRange(min=0, message="Prix invalide")])
    submit = SubmitField("Update prestation")


class FormWTFDeletePrestation(FlaskForm):
    nom_prestation_delete_wtf = StringField("Effacer cette prestation")
    submit_btn_del            = SubmitField("Effacer prestation")
    submit_btn_conf_del       = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler        = SubmitField("Annuler")
