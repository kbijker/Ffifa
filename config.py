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


import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'YWN-guess'