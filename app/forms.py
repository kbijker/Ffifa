#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      KE.Bijker
#
# Created:     04/07/2020
# Copyright:   (c) KE.Bijker 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
from fifa_functions import *
from app.routes import *





class LoginForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    remember_me = BooleanField('Onthouden')
    submit = SubmitField('Inloggen')

class registerForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    email = StringField('e-mail', validators=[DataRequired()])
    bankaccount = IntegerField('Bankrekening', validators=[DataRequired()])
    #remember_me = BooleanField('Remember Me')
    #recaptcha = RecaptchaField()
    submit = SubmitField('Register')

class ProfileForm(FlaskForm):

    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    email = StringField('e-mail', validators=[DataRequired()])
    bankaccount = IntegerField('Bankrekening', validators=[DataRequired()])
    keuze = ['email wijzigen','wachwoord wijzigen','bankrekening wijzigen']
    action = SelectField('Actie:', [DataRequired()], choices=keuze)
    submit = SubmitField('Wijzigingen bevestigen')

class UsersForm(FlaskForm):

    userTeams = getUsersTeam()
    users = list(userTeams.keys())
    teams = list(userTeams.values())
    keuze2 = [0,1,2,3]
    keuze3 = ['rechten toewijzen','verwijderen','wachtwoord resetten', 'overzicht gebruikersgegevens','teamselectie verwijderen']
    userchoice = SelectField('Gebruikers:', [DataRequired()], choices=users)
    rechten = SelectField('Rechten:', [DataRequired()], choices=keuze2)
    actie = SelectField('Actie:', [DataRequired()], choices=keuze3)
    submit = SubmitField('Uitvoeren')

class NewPlayer(FlaskForm):
    clubs = selectTeams()
    posities = Positie()

    voornaam = StringField('Voornaam', validators=[DataRequired()])
    achternaam = StringField('Achternaam', validators=[DataRequired()])
    geb_datum = DateField('Geboortedatum')
    teams = SelectField('Club:', [DataRequired()], choices=clubs)
    positie = SelectField('Positie:', [DataRequired()], choices=posities)
    marktwaarde = IntegerField('Marktwaarde', validators=[DataRequired()])
    submit = SubmitField('Opslaan speler')

class NewPlayerTeam(FlaskForm):

    players, playerdic, playerdicrecords = CollectPlayerlist()
    naam = StringField('Naam team', validators=[DataRequired()])

    player1 = SelectField('Speler 1:', [DataRequired()], choices=players)
    player2 = SelectField('Speler 2:', [DataRequired()], choices=players)
    player3 = SelectField('Speler 3:', [DataRequired()], choices=players)
    player4 = SelectField('Speler 4:', [DataRequired()], choices=players)
    player5 = SelectField('Speler 5:', [DataRequired()], choices=players)
    player6 = SelectField('Speler 6:', [DataRequired()], choices=players)
    player7 = SelectField('Speler 7:', [DataRequired()], choices=players)

    submit = SubmitField('Opslaan spelersteam')

class NewTeam(FlaskForm):

    naam = StringField('Naam', validators=[DataRequired()])
    plaats = StringField('Plaats', validators=[DataRequired()])
    submit = SubmitField('Opslaan team')

class addRecords(FlaskForm):
     keuze = ['Nieuwe speler','Nieuw team']
     choice = SelectField('Keuze:',validators=[DataRequired()], choices=keuze )
     submit = SubmitField('naar invoeren')

class DeleteRecords(FlaskForm):
     keuze = ['Verwijder speler','Verwijder club']
     choice = SelectField('Keuze:',validators=[DataRequired()], choices=keuze )
     submit = SubmitField('Kies')

class DeletePlayer(FlaskForm):

      namen,vn,an = classconstrPlayerlist(0)

      naam = SelectField('Spelers:', validators=[DataRequired()], choices = namen)
      submit = SubmitField('Verwijder Speler')


class DeleteTeam(FlaskForm):
      namen = selectTeams()
      naam = SelectField('Team:', validators={DataRequired()}, choices = namen)
      submit = SubmitField('Verwijder team')



class TableChoice(FlaskForm):
    tlist= ShowAvailableTables()
    tables = []
    for t in tlist:
        tuple1 = (t,t)
        tables.append(tuple1)
        if 'USERS' in tuple1: tables.remove(tuple1)
    print('tables = ',tables)
    table = SelectField('Kies tabel:', [DataRequired()], choices=tables)
    submit = SubmitField('toon')
