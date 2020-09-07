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
from flask import Flask
from flask import render_template, request, flash, redirect, url_for
from app import app
from app.forms import *
import firebirdsql
from tabulate import *
from fifa_functions import *
from run_fifa import *




conn = firebirdsql.connect (
    host = IPlocal,
    database = 'c:/programData/Relsql/DB/ffifa.fdb',
    port=13051,
    user=username,
    password = ww
    )



@app.route('/')


@app.route('/index', methods=['GET','POST'])
def index():
    username = user1.un
    if len(username) >1: feedback = f'Gebruiker {username} is ingelogd.'
    else:
        user1.addUser('onbekend',0)
        user1.right = 0
        feedback = 'Inloggen is verplicht.'
    #print('Home:', username)
    return render_template('index.html', title='Home', username = username, feedback =feedback)

@app.route('/login', methods=['GET','POST'])
def login():
    username = ''
    username = user1.un
    if username == '':
       username = 'onbekend'
       password = 'false'
       feedback = 'Als je nog niet geregisteerd bent, ga dit dan eerst doen.'
    else: feedback = 'Je hebt blijkbaar niet te rechten om de vorige site te zien.'
    check = False
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if form.is_submitted():
           check2 = UserExits(username)
           if check2:
              check, rights = CheckUser(username,password)
              if check:
                feedback = f"User {username} is ingelogd."
                user1.addUser(username, rights)
                print('username:', user1.un, 'Rechten:', user1.rights)
                #if user1.un == 'KBijker': user1.rightsAdmin3()

              else:
                 feedback = f"Inloggen mislukt. wachtwoord is fout."
           else: feedback = "Gebruikersnaam bestaat niet"


    return render_template('login.html', title='Sign In', form=form, feedback = feedback, username = username)

@app.route('/register', methods=['GET','POST'])
def register():

    form = registerForm()
    feedback =''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        bankaccount = request.form['bankaccount']

        if form.is_submitted():
           if UserExits(username): feedback = 'Gebruikersnaam wordt al door iemand anders gebruikt.'
           else:
               if PasswordCheck(password):

                  if E_mailCheck(email):
                     RegisterUser(username,password,email,bankaccount)
                     feedback = f"User {username} is succesvol toegevoegd."
                  else: feedback = 'Gegeven e-mail is al gebruikt of niet geldig'
               else: feedback = 'Wachtwoord voldoet niet aan de eisen (minimaal 7 karakters, een hoofdletter en een cijfer)'
        else: feedback = f"Registeren mislukt."
    return render_template('register.html', title='Register', form=form, feedback =feedback)


@app.route('/admin', methods=['GET','POST'])
def admin():
    #rights = 0
    username = user1.un
    rights = user1.rights
    feedback = 'Voor deze optie moet je als admin ingelogd zijn.'
    if username == '' or username == 'onbekend':
        return redirect(url_for('login'))
    if rights < 3:
        return redirect(url_for('index'))

    return render_template('admin.html', title='Administratie', feedback =feedback, username = username)

@app.route('/newplayer', methods=['GET','POST'])
def newplayer():
    #rights = 0
    username = user1.un
    rights = user1.rights
    feedback = 'Voor deze optie moet je als admin ingelogd zijn.'
    if username == '' or username == 'onbekend':
        return redirect(url_for('login'))
    if rights < 2:
        return redirect(url_for('index'))
    form = NewPlayer()
    if request.method == 'POST' and rights > 1:
        voornaam = request.form['voornaam']
        achternaam = request.form['achternaam']
        geb_datum = request.form['geb_datum']
        teams = request.form['teams']
        positie = request.form['positie']
        marktwaarde = request.form['marktwaarde']
        if voornaam != '' and achternaam != '': check = checkUniekPl(voornaam,achternaam)
        else: feedback = 'Vul alle velden in.'
        if form.is_submitted() and check:
           AddPlayer(voornaam,achternaam,geb_datum,positie,teams,marktwaarde)
           feedback = f"Speler {achternaam} is succesvol toegevoegd."
           fullnames, voornamen, achternamen = classconstrPlayerlist(0)
        else: feedback = f"Opslaan mislukt. Speler {voornaam} {achternaam} bestaat al in de DB."
    else: feedback = 'Voor deze actie heb je Admin-rechten nodig.'

    return render_template('newplayer.html', title='Nieuwe speler invoeren', form=form, feedback = feedback, username=username)


@app.route('/profile', methods=['GET','POST'])
def profile():
    teamselection = ''
    info = ''
    username = user1.un
    rights = user1.rights
    feedback = 'Voor deze optie moet je als admin ingelogd zijn.'
    info = profileInfo(username)
    form = ProfileForm()
    if request.method == 'POST' and rights > 0:
        password = request.form['password']
        email = request.form['email']
        bankaccount = request.form['bankaccount']
        action = request.form['action']
        if form.is_submitted() and action == 'wachwoord wijzigen' :
           feedback = ChangePassword(username, password)
        if form.is_submitted() and action == 'bankrekening wijzigen' :
           feedback = ChangeBankaccount(username, bankaccount)
        if form.is_submitted() and action == 'email wijzigen' :
           feedback = ChangeEmail(username, email)
    return render_template('profile.html', title='Gebruikers onderhoud', form=form, feedback = feedback, username=username, info =info)

@app.route('/users', methods=['GET','POST'])
def users():
    teamselection = ''
    username = user1.un
    rights = user1.rights
    feedback = 'Voor deze optie moet je als admin ingelogd zijn.'
    if username == '' or username == 'onbekend':
        return redirect(url_for('login'))
    if rights < 2:
        return redirect(url_for('index'))
    form = UsersForm()
    if request.method == 'POST' and rights > 1:
        userchoice = request.form['userchoice']
        rechten = request.form['rechten']
        actie = request.form['actie']
        userTeams = getUsersTeam()
        teamselection = userTeams[userchoice]

        if form.is_submitted() and actie == 'rechten toewijzen' :
           SaveRightsDB(userchoice, rechten)
           feedback = f'werkzaamheid: {userchoice} privilege {rechten} toegewezen.'
        if form.is_submitted() and actie == 'verwijderen' :
           feedback =deleteUser(userchoice)
        if form.is_submitted() and actie == 'overzicht gebruikersgegevens' :
           feedback = userInfo(userchoice)
        if form.is_submitted() and actie == 'wachtwoord resetten' :
           feedback = resetPassword(userchoice)
    else: feedback = 'Voor deze actie heb je Admin-rechten nodig.'

    return render_template('users.html', title='Gebruikers onderhoud', form=form, feedback = feedback, username=username, teamselection = teamselection)

@app.route('/newplayerteam', methods=['GET','POST'])
def newplayerteam():
    rights = 0
    username = 'onbekend'
    username = user1.un
    rights = user1.rights
    if username == '' or username == 'onbekend' or rights == 0:
        return redirect(url_for('login'))

    teambaas = user1.un
    feedback = 'Budget is 5 miljoen; Samenstelling: spelers moeten van verschillende teams zijn en 2 aanvallers, 2 verdigers, 2 middenvelders en een doelverdediger.'
    form = NewPlayerTeam()
    if request.method == 'POST' and rights>0:
        naam = request.form['naam']

        player1 = request.form['player1']
        player2 = request.form['player2']
        player3 = request.form['player3']
        player4 = request.form['player4']
        player5 = request.form['player5']
        player6 = request.form['player6']
        player7 = request.form['player7']

        if form.is_submitted():
           check, fout, codeplayers = Checkteam(player1,player2,player3,player4,player5,player6,player7)

           if check:
               teamSaveToDB(naam, teambaas, codeplayers)
               feedback = f"Team {naam} is succesvol toegevoegd."
           else: feedback = fout
           #fullnames, voornamen, achternamen = classconstrPlayerlist(0)
        else: feedback = f"Opslaan mislukt. Speler {voornaam} {achternaam} bestaat al in de DB."
    else: feedback = 'Je moet eerst ingelogd zijn en mag maar één team aanmaken per gebruiker.'

    return render_template('newplayerteam.html', title='Nieuw team samenstellen', form=form, feedback = feedback, username=username)


@app.route('/newteam', methods=['GET','POST'])
def newteam():
    rights = 0
    username = user1.un
    rights = user1.rights
    feedback = 'Voor deze slide moet als admin ingelogd zijn.'
    if username == '' or username == 'onbekend':
        return redirect(url_for('login'))
    if rights < 2:
        return redirect(url_for('index'))
    naam = ""
    form = NewTeam()
    plaats = ''
    feedback =''
    if request.method == 'POST' and rights > 1:
        naam = request.form['naam']
        plaats = request.form['plaats']
    else: feedback = 'Voor deze actie heb je Admin-rechten nodig.'
    missing = list()

    if plaats == "":
      k = 'Plaats'
      missing.append(k)
    if naam == "":
      k = 'Naam'
      missing.append(k)
    if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
    else:
        feedback = f"Team {naam} is succesvol ingevoerd."
        AddNewTeam(naam,plaats)
    return render_template('newteam.html', title='Nieuw team invoeren', form=form, feedback=feedback, username = username)

@app.route('/addrecord', methods=['GET','POST'])
def addrecord():
    username = user1.un
    form = addRecords()
    choice =''
    if request.method == 'POST':
        choice = request.form['choice']
    if choice =='Nieuwe speler':

        return redirect(url_for('newplayer'))

    if choice == 'Nieuw team':
        print('team gekozen')
        return redirect(url_for('newteam'))
    return render_template('addrecord.html', title='Nieuwe records aanmaken', form=form, username = user1.un)

@app.route('/showTable', methods=['GET','POST'])
def showTable():
    username = user1.un
    tlist= ShowAvailableTables()
    table1 =''
    tabeltitel = ''
    records =''
    table_header = ''
    streep = ''
    form = TableChoice()

    if request.method == 'POST':
            table1 = request.form['table']
    if form.validate_on_submit():
        table2 = showtable(table1)
        records, table_header = showtableRaw(table1)
        for t in table_header:
            tabeltitel += t
            tabeltitel += '  |  '
        corr = int(len(tabeltitel)*1.05)
        for i in range(len(tabeltitel)+corr):
            streep += '-'
    return render_template('showTable.html', form = form, records =records, tabeltitel =tabeltitel, streep =streep, username = username)

@app.route('/deleteteam', methods=['GET','POST'])
def deleteteam():

    rights = 0
    username = user1.un
    rights = user1.rights
    feedback = 'Voor deze slide moet als admin ingelogd zijn.'
    if username == '' or username == 'onbekend':
        return redirect(url_for('login'))
    if rights < 2:
        return redirect(url_for('index'))
    form = DeleteTeam()
    if request.method =='POST' and rights > 1:
          naam = request.form['Naam']
    else: feedback = 'Voor deze actie heb je Admin-rechten nodig.'
    return render_template('deleteteam.html', form = form, feedback = feedback, username = username)

id_names = getnameplayers()

@app.route('/deleteplayer', methods=['GET','POST'])
def deleteplayer():
    rights = 0
    username = user1.un
    rights = user1.rights
    feedback = 'Voor deze slide moet als admin ingelogd zijn.'
    if username == '' or username == 'onbekend':
        return redirect(url_for('login'))
    if rights < 2:
        return redirect(url_for('index'))
    fullnames, voornamen, achternamen = classconstrPlayerlist(0)
    form = DeletePlayer()
    form.namen = fullnames

    feedback = 'Verwijderen is definitief. dus geen "Undo" meer mogelijk.'
    if request.method =='POST':
        naam = request.form['naam']  #volledige naam
    if form.is_submitted() and rights > 1:

        tel = 0
        for name in fullnames:
            if name == naam:
               id1 = deletePlayerDB(voornamen[tel],achternamen[tel])
               fullnames, voornamen, achternamen = classconstrPlayerlist(id1)
               print('fullnames:', fullnames)
            tel += 1

        feedback = 'Speler: '+ naam + ' succesvol verwijderd.'
    else: feedback = 'Voor deze actie heb je Admin-rechten nodig.'
    return render_template('deleteplayer.html', form = form, feedback = feedback, username = username)

@app.route('/deleterecords', methods=['GET','POST'])
def deleterecords():
    rights = 0
    username = user1.un
    rights = user1.rights
    feedback = 'Voor deze slide moet als admin ingelogd zijn.'
    if username == '' or username == 'onbekend':
        return redirect(url_for('login'))
    if rights < 2:
        return redirect(url_for('index'))
    form = DeleteRecords()
    choice =''
    if request.method =='POST':
       choice = request.form['choice']
    if choice =='Verwijder speler':
        return redirect(url_for('deleteplayer'))

    if choice == 'Verwijder club':
        return redirect(url_for('deleteteam'))


    return render_template('deleterecords.html', form = form, username = username)

conn.close()