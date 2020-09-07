#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      KE.Bijker
#
# Created:     04/07/2020
# Copyright:   (c) KE.Bijker 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import firebirdsql
from tabulate import *
from run_fifa import *

conn = firebirdsql.connect (
    host = IPlocal,
    database = 'c:/programData/Relsql/DB/ffifa.fdb',
    port=13051,
    user=username,
    password = ww
    )

class Playerlist:
    def __init__(self, id, voornamen, achternamen, vollenamen):
        self.id = id
        self.voornamen = voornamen
        self.achternamen = achternamen
        self.vollenamen = vollenamen
        self.id = id

    def loadPlayers(self):

        self.voornamen = []
        self.achternamen =[]
        self.vollenamen =[]
        self.id = []
        self.id = getContentColInt('spelers','id')
        self.voornamen = getContentCol('spelers','voornaam')
        self.achternamen = getContentCol('spelers','achternaam')
        tel = 0
        for voornaam in self.voornamen:
            vollenaam = voornaam + ' ' + self.achternamen[tel]
            self.vollenamen.append(vollenaam)
            tel +=1


    def getPlayerlist(self):
        Playerlist.loadPlayers(self)
        return self.vollenamen

    def delPlayer(self, ide):
        tel = 0
        for i in self.id:
            if i == ide:
                self.id.remove(self.id[tel])
                self.voornamen.remove(self.voornamen[tel])
                self.achternamen.remove(self.achternamen[tel])
            tel +=1

    def addplayer(self, vn, an):
        vollenaam = vn + ' ' + an


class Playerteamlist:
    def __init__(self, team_dict):

        self.team_dict = team_dict


    def unwindTeam(self):


        self.clubs = []
        self.posities = []
        self.marktwaarde_tot = 0

        for k,v in self.team_dict.items():
            self.clubs.append(v[4])
            self.posities.append(v[3])
            self.marktwaarde_tot += v[5]







def classconstrPlayerlist(id1):


    playerlist1 = Playerlist(0,'','','')
    playerlist1.loadPlayers()
    if id1 > 0: playerlist1.delPlayer(id1)
    return playerlist1.getPlayerlist(), playerlist1.voornamen,playerlist1.achternamen


def checkUniekPl(vn,an):
     ''' Hiermee gaan we de uniciteit van een speler controleren. Om redundantie te voorkomen '''
     voornaam = ''

     cur = conn.cursor()
     cur.execute("Select voornaam from spelers where achternaam = '{0}'".format(an))
     tuple1 = cur.fetchall()
     for c in tuple1:
        voornaam = ' '.join(c)
     if voornaam == vn:
        return False
     else: return True

def convertMonth(m):
    dicMonth = {'01':'jan','02':'feb','03':'mar','04':'apr','05':'may','06':'jun','07':'jul','08':'aug','09':'sep','10':'oct','11':'nov','12':'dec'}
    return dicMonth[m]

def convertTextCodeDB(colomn1, table, colomn2, text):
     cur = conn.cursor()
     cur.execute("Select {0} from {1} where {2} = '{3}'".format(colomn1, table, colomn2, text))
     tuple1 = cur.fetchall()
     for c in tuple1:
        text2 = ' '.join(c)
     return text2

def AddPlayer(vn,an,geb_datum,pos,club,mw):


     year = geb_datum[0:4]
     month1 = geb_datum[5:7]
     day = geb_datum[8:10]
     month = convertMonth(month1)
     geboorted = day+'-'+month+'-'+year

     positie = convertTextCodeDB('code','positie','info',pos)
     clubc = convertTextCodeDB('codet','teams','naam',club)

     #print(vn,an,geboorted,positie,clubc,mw)

     cur = conn.cursor()
     NewPlayer = [(vn,an,geboorted,positie,clubc, mw)]

     cur.executemany('Insert into Spelers (Voornaam, Achternaam, Geboortedatum, Positie,Team, Marktwaarde)  Values (?,?,?,?,?,?)',NewPlayer)
     conn.commit()    #invoering definitief maken.

     #cur.execute('Insert into Spelers (Voornaam, Achternaam, Geboortedatum,Positie,Team, Marktwaarde) Values ({0},{1)}, {2},{3},{4},{5})'.format(vn,an,geboorted,positie,clubc,mw))


def getContentCol(table, colomn):

    cur = conn.cursor()
    cur.execute('select {0} from {1}'.format(colomn,table))
    colomnlist = []
    for c in cur.fetchall():
            dbcontent = ' '.join(c)
            colomnlist.append(dbcontent)

    return colomnlist

def getContentColInt(table, colomn):

    cur = conn.cursor()
    cur.execute('select {0} from {1}'.format(colomn,table))
    colomnlist = []
    for c in cur.fetchall():
            dbcontent = c[0]
            colomnlist.append(dbcontent)

    return colomnlist

def CollectPlayerlist():
    '''Haal relevante gegevens van alle spelers op uit DB.'''
    cur = conn.cursor()
    cur.execute('select S.id, S.voornaam, S.achternaam, P.info, T.naam, S.marktwaarde from spelers S inner join teams T on S.team = T.codet inner join positie P on S.positie=P.code ')
    collect_spelers = cur.fetchall()
    #print(collect_spelers)
    playerlist  = []
    playerdic = {}           # formaat {number, player_DB_ fields/tuple}
    playerdicrecords = {}    # formaat {number, playerstring/record}
    count = 1
    for r in collect_spelers:
        record = ''
        playerdic[count] = r

        for field in r:
             record += str(field)
             record += ' '
             # = ' '.join(r)
        count += 1
        playerlist.append(record)
        playerdicrecords[count]= record

    #print(playerdic)
    return playerlist, playerdic, playerdicrecords


def Checkteam(player1,player2,player13,player4,player5,player6,player7):
    ''' Samenstelling spelersteam wordt gecontroleerd op budget en samenstelling.
    Budget is 5 miljoen;
    Samenstelling: spelers moeten van verschillende teams zijn en 2 aanvallers, 2 verdigers, 2 middenvelders en een doelverdediger. '''

    playerlisttot, playerteamdic, playerdicrecords = CollectPlayerlist()
    playerteamlist1 = Playerteamlist(playerteamdic)
    playerteamlist1.unwindTeam()

    #print(playerdicrecords)
    team = [player1,player2,player13,player4,player5,player6,player7]
    codes = []
    checkteam1 = []
    for pl in team:
        if pl not in checkteam1:  checkteam1.append(pl)
        else:
            feedback = 'Speler komt meerdere keren voor in hetzelfde team.'
            return False, feedback, codes

    # numbers = filternumbers(playerteamdic)
    numbers = []
    for key, player in playerdicrecords.items():
        if player in team: numbers.append(key-1)
    #print('numb:',numbers)
    clubs = []
    posities = []
    marktwaardeTot = []

    for k, play in playerteamdic.items():
        if k in numbers:

            clubs.append(play[4])
            posities.append(play[3])
            marktwaardeTot.append(play[5])
            codes.append(play[0])
    checkteam2 = []
    #print('clubs:',clubs)
    for club in clubs:
        if club not in checkteam2: checkteam2.append(club)
        else:
            feedback = 'Meerdere spelers van dezelfde club is niet toegestaan.'
            return False, feedback, codes
    print('pos', posities)
    countAanv = 0
    countMidd = 0
    countVerd = 0
    countKeeper = 0
    for pos in posities:
        if pos == 'Aanvaller': countAanv += 1
        if pos == 'Middenvelder': countMidd +=1
        if pos == 'Verdediger': countVerd += 1
        if pos == 'Doelverdediger': countKeeper += 1
    if countAanv == 2 and countKeeper == 1 and countMidd == 2 and countVerd == 2:
        feedback = 'Samenstelling klopt'
    else:
        feedback = 'Samenstelling is incorrect. Je moet twee aanvallers, twee verdedigers, twee middenvelders en een keeper kiezen.'
        return False, feedback, codes
    budget = 0
    for value in marktwaardeTot:
        budget += value
    if budget > 7000000:
        feedback = 'Budget overschrijding. Teamsamenstelling afgekeurd.'
        return False, feedback, codes

    else: feedback = 'budget akkoord.'
    print('Budget: ',budget)
    #print('check2:',checkteam2)
    return True, 'Team voldoet aan de regels.', codes

def teamSaveToDB(teamnaam, teambaas, codespelers):

    cur = conn.cursor()
    NewPlayerTeam = [(teamnaam, teambaas, 0, codespelers[0],codespelers[1],codespelers[2],codespelers[3],codespelers[4], codespelers[5], codespelers[6])]

    cur.executemany('Insert into fifateams (naam,teambaas,punten,player1,player2,player3,player4,player5,player6,player7) Values (?,?,?,?,?,?,?,?,?,?)',NewPlayerTeam)
    conn.commit()    #invoering definitief maken.


def RegisterUser(un,pw,email,ba):

    cur = conn.cursor()
    NewUser = [(un,pw,email,ba)]

    cur.executemany('Insert into Users (gebruikersnaam, wachtwoord, email, bankrekening)  Values (?,?,?,?)',NewUser)
    conn.commit()


def deleteUser(user):

    cur = conn.cursor()
    cur.execute("delete from users where gebruikersnaam = '{0}'".format(user))
    conn.commit()
    return f'Gebruiker {user} is verwijderd uit de DB'


def getUsersTeam():
    ''' Gebruikersnamen ophalen uit de DB.'''
    userteams = {}

    cur = conn.cursor()
    cur.execute('select U.gebruikersnaam, F.naam from users U left outer join fifateams F on U.gebruikersnaam = F.teambaas')
    for un in cur.fetchall():

        userteams[un[0]] = un[1]
    print('ut=',userteams)

    return userteams


def userInfo(user):
    info_string = ''
    cur = conn.cursor()
    cur.execute("select U.gebruikersnaam, U.rechten, F.naam from users U inner join fifateams F on U.gebruikersnaam = F.teambaas where U.gebruikersnaam = '{0}'".format(user))
    for info in cur.fetchall():
        info_string = f' Gebruikersnaam: {info[0]}; rechten {str(info[1])}; Manager van team {info[2]}'
        print('I:',info_string)
    return info_string

def SaveRightsDB(username, rights):

    cur = conn.cursor()
    cur.execute("update users set rechten = {0} where gebruikersnaam = '{1}'".format(rights,username))
    conn.commit()


def resetPassword(user):

    result = ''
    cur = conn.cursor()
    cur.execute("update users set wachtwoord = 'Welkom123' where gebruikersnaam = '{0}'".format(user))
    cur.execute("select email from users where gebruikersnaam = '{0}'".format(user))
    for email in cur.fetchall():
        res1 = email[0]
    result = f'Wachtwoord van gebruiker {user} is veranderd in "Welkom123" en kan verstuurd worden naar {res1}.'
    conn.commit()
    return result

def UserExits(username):
    ''' Bestaat de username wel in de DB?'''
    un2 = ''
    cur = conn.cursor()
    cur.execute("select gebruikersnaam from users where gebruikersnaam in ('{0}') ".format(username))
    for un1 in cur.fetchall():
        if un1 == None: return False
        else:  un2 = un1[0]    #tuple uitpellen
    if username == un2: return True
    else: return False


def PasswordCheck(password):

    check1 = False
    check2 = False
    hoofdletters = 'ABCDEFGHIJKLMNOPQRSTVUVWXYZ'
    if len(password) > 6:
        for l in password:
            if l in hoofdletters:
                check1 = True
            if l.isnumeric():
                check2 = True
        if check1 and check2:
            return True
    else: return False



def E_mailCheck(email):

    ''' Bestaat de email al in de DB?'''
    em2 = ''
    cur = conn.cursor()
    cur.execute("select email from users where email in ('{0}') ".format(email))
    for em1 in cur.fetchall():
        if em1 == None: return False
        else:  em2 = em1[0]    #tuple uitpellen
    if email == em2: return False
    else: return True


def CheckUser(username,password):

    pw2 = ''
    cur = conn.cursor()
    cur.execute("select wachtwoord, rechten from users where gebruikersnaam ='{0}' ".format(username))
    for pw1 in cur.fetchall():
        pw2 = pw1[0]    #tuple uitpellen
    if password == pw2: return True, pw1[1]
    else: return False, 0


def profileInfo(user):

    cur = conn.cursor()
    cur.execute("select email,bankrekening,rechten from users where gebruikersnaam = '{0}'".format(user))
    for info in cur.fetchall():
        email = info[0]
        ba = info[1]
        re = info[2]
    return f'Gebruiker {user} heeft als e-mail {email} en als bankrekening {ba} geregisteerd en heeft als privilege niveau {re}'


def ChangeBankaccount(user, value):

    cur = conn.cursor()
    cur.execute("update users set bankrekening = '{0}' where gebruikersnaam = '{1}'".format(value,user))
    conn.commit()
    return f'Bankrekening is veranderd in {value}'

def ChangeEmail(user, email):

    if E_mailCheck(email):
        UpdateDB('email', email, user)
        return 'Email is gewijzigd.'
    else: return 'Email bestaat al in onze DB.'


def ChangePassword(user, password):

    if PasswordCheck(password):
        UpdateDB('wachtwoord', password, user)
        return 'Wachtwoord is gewijzigd.'
    else: return 'Wachtwoord voldoet niet aan de eisen; Minimaal 7 karakters, een hoofdletter en een cijfer'

def UpdateDB(field, value, user):

    cur = conn.cursor()
    cur.execute("update users set {0} = '{1}' where gebruikersnaam = '{2}'".format(field,value,user))
    conn.commit()

def getnameplayers():

    voornamen = []
    achternamen =[]
    vollenamen =[]

    voornamen = getContentCol('spelers','voornaam')
    achternamen = getContentCol('spelers','achternaam')
    tel = 0
    for voornaam in voornamen:
        vollenaam = voornaam + ' ' + achternamen[tel]
        vollenamen.append(vollenaam)
        tel +=1
    return vollenamen, voornamen, achternamen



def deletePlayerDB(vn,an):

    cur = conn.cursor()

    #print('delete vn:', vn)
    cur.execute("select id from spelers where voornaam ='{0}' and achternaam ='{1}'".format(vn,an))
    for id1 in cur.fetchall():
        id2 = id1[0]    #tuple uitpellen

    cur.execute("delete from spelers where id = {0}".format(id2))
    conn.commit()
    return id2




def Positie():

     posities = []
     cur = conn.cursor()
     cur.execute('select info from positie')
     for p in cur.fetchall():
          po = ' '.join(p)
          posities.append(po)
     return posities

def selectTeams():

     clubs = []
     cur = conn.cursor()
     cur.execute('select naam from teams')
     for c in cur.fetchall():
          cl = ' '.join(c)
          clubs.append(cl)
     return clubs

def showtable(table):
      table_header = []
      records = []
      cur = conn.cursor()
      #print('Table {}:'.format(table))
      dicColm = ColomnsOfTable(table)
      for colm in dicColm.values():
           table_header.append(colm)
      cur.execute('select * from {0}'.format(table))
      for c in cur.fetchall():
         records.append(c)

      #print(tabulate(records, table_header))

def showtableRaw(table):
      table_header = []
      records = []
      cur = conn.cursor()
      #print('Table {}:'.format(table))
      dicColm = ColomnsOfTable(table)
      for colm in dicColm.values():
           table_header.append(colm)
      cur.execute('select * from {0}'.format(table))
      for c in cur.fetchall():
         records.append(c)

      return records, table_header

def FirstColomn(table):

      cur = conn.cursor()
      print('Kolomnamen van Tabel {}:'.format(table))
      cur.execute("SELECT RDB$FIELD_NAME FROM RDB$RELATION_FIELDS where RDB$RELATION_NAME = '{0}' ".format(table))
      c = cur.fetchall()
      FirstColomn = ' '.join(c[0])
      return FirstColomn

def ColomnsOfTable(table):
    ''' Uit de tabel worden de kolommen als strings gedestileerd en in een dictionaire gezet met een nummer voor elke kolom.
    Met als doel dat de gerbuiker een nummer kiest (is effectiever/ sneller en minder kan op typfouten) '''

    cur = conn.cursor()
    print('Kolomnamen van Tabel {}:'.format(table))
    cur.execute("SELECT RDB$FIELD_NAME FROM RDB$RELATION_FIELDS where RDB$RELATION_NAME = '{0}' ".format(table))
    colomns = cur.fetchall()
    dicColomns = {}
    t = 0
    for colomn in colomns:
        print(t,' '.join(colomn))
        colomnstr =  ' '.join(colomn)
        dicColomns[t] =  colomnstr
        t += 1
    return dicColomns


def ShowAvailableTablesRaw():
    cur = conn.cursor()
    #print('Overzicht tabellen:')
    cur.execute('select rdb$relation_name from rdb$relations where rdb$view_blr is null and (rdb$system_flag is null or rdb$system_flag = 0);')
    tables = cur.fetchall()
    return tables



def ShowAvailableTables():
    cur = conn.cursor()
    #print('Overzicht tabellen:')
    cur.execute('select rdb$relation_name from rdb$relations where rdb$view_blr is null and (rdb$system_flag is null or rdb$system_flag = 0);')
    tables = cur.fetchall()
    #print(tables)
    #print(type(tables[0]), tables[0])
    tableList  = []
    count = 0
    for t in tables:
        count += 1
        table = ' '.join(t)
        print(count,table)
        tableList.append(table)
    return tableList


def AddNewTeam(name,place):
    ''' Invoeren van een record, betekent eigenlijk werken met een Tuple '''
    code1 = ''
    for i in range(3):
        if name[i].isalpha(): code1 += name[i]
    code = (code1+place[0:3]).upper()
    NewTeam = [(code,name,place)]
    print(NewTeam)
    cur = conn.cursor()
    cur.executemany('insert into Teams (CODET,NAAM, PLAATS) values (?,?,?)',NewTeam)
    conn.commit()    #invoering definitief maken.




def DeleteRecord(table,colomn1,selectObj):

    cur = conn.cursor()
    selectobjDatatype = int(selectObj)
    print('data:',table,selectobjDatatype)
    cur.execute("delete from {0} where {1} = {2}".format(table, colomn, selectobjDatatype))
    conn.commit()



def UpdateRecord(table,colomn1,selectObj):
    ''' Gebruiker kan zelf met nummers de juiste tabel en kolom kiezen, waarin iets gewijzigd moet worden '''

    cur = conn.cursor()
    selectobjDatatype = int(selectObj)
    dicColTable= ColomnsOfTable(table)
    colomnNr = int(input('Welke kolomnummer wil je wijzigen?'))
    colomnUpdate = dicColTable[colomnNr]
    ValueUpdate = input('In welke waarde moet dit veranderd worden?')
    # Aanpassen datatypes integers of strings of dates.
    #print('data:',table,selectobjDatatype)
    cur.execute("update {0} set {1} = {2} where {3} = {4}".format(table, colomnUpdate, ValueUpdate, colomn1, selectobjDatatype))
    conn.commit()