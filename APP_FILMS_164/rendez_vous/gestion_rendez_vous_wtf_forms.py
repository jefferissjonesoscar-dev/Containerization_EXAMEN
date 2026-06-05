"""
    Fichier : gestion_rendez_vous_wtf_forms.py
    Auteur : OM 2021.03.22 - Adapté GUERID Rayan DEVA 1A
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TimeField, SelectField
from wtforms import SubmitField
from wtforms.validators import Length, Optional, NumberRange


class FormWTFAjouterRendezVous(FlaskForm):
    date_rdv_wtf      = DateField("Date du rendez-vous")
    heure_rdv_wtf     = TimeField("Heure du rendez-vous")
    statut_rdv_wtf    = SelectField("Statut", choices=[("En attente", "En attente"), ("Confirmé", "Confirmé"), ("Annulé", "Annulé")])
    retard_rdv_wtf    = IntegerField("Retard (minutes)", validators=[NumberRange(min=0, max=999)], default=0)
    note_rdv_wtf      = StringField("Note", validators=[Optional(), Length(max=255)])
    fk_client_wtf     = SelectField("Client", coerce=int)
    fk_coiffeur_wtf   = SelectField("Coiffeur", coerce=int)
    fk_prestation_wtf = SelectField("Prestation", coerce=int)
    submit = SubmitField("Enregistrer rendez-vous")


class FormWTFUpdateRendezVous(FlaskForm):
    date_rdv_update_wtf      = DateField("Date du rendez-vous")
    heure_rdv_update_wtf     = TimeField("Heure du rendez-vous")
    statut_rdv_update_wtf    = SelectField("Statut", choices=[("En attente", "En attente"), ("Confirmé", "Confirmé"), ("Annulé", "Annulé")])
    retard_rdv_update_wtf    = IntegerField("Retard (minutes)", validators=[NumberRange(min=0, max=999)], default=0)
    note_rdv_update_wtf      = StringField("Note", validators=[Optional(), Length(max=255)])
    fk_client_update_wtf     = SelectField("Client", coerce=int)
    fk_coiffeur_update_wtf   = SelectField("Coiffeur", coerce=int)
    fk_prestation_update_wtf = SelectField("Prestation", coerce=int)
    submit = SubmitField("Update rendez-vous")


class FormWTFDeleteRendezVous(FlaskForm):
    info_rdv_delete_wtf = StringField("Effacer ce rendez-vous")
    submit_btn_del      = SubmitField("Effacer rendez-vous")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler  = SubmitField("Annuler")
