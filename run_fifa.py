#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      KE.Bijker
#
# Created:     17/06/2020
# Copyright:   (c) KE.Bijker 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#from app import routes
import firebirdsql
import socket
from flask import Flask
from config import Config
from app import *

class User:
    def __init__(self):
        self.un = ''   #gebruikersnaam
        #self.right = 1

    def addUser(self, un, rights):
        self.un = un
        self.rights = rights

    def rightsAdmin2(self):
        self.right = 2

    def rightsAdmin3(self):
        self.right = 3



IPlist = ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1])

for IP in IPlist:
    IPlocal = IP

#app = Flask(__name__)
#app.config.from_object(Config)
username = 'sysdba'
ww = 'masterkey'
user1 = User()
#from app import app

if __name__ == '__main__':
    app.run(IPlocal, 5000, True)
