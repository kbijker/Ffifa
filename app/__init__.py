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
from config import Config
from run_fifa import IPlocal


app = Flask(__name__)
app.config.from_object(Config)


from app import routes


if __name__ == '__main__':
    app.run('192.168.2.89', 5000, True)