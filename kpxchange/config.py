
import os
from sys import exit
if not os.environ.get("RECAPTCHA_SECRET_KEY"): exit("Unable to find RECAPTCHA_SECRET_KEY environment variable")

class Config(object):
    DEBUG              = False
    TESTING            = False
    CSRF_ENABLED       = True
    SECRET_KEY         = os.urandom(24)
    VAULT_PATH         = 'vault'
    MAX_VAULT_SIZE     = 1024*1024*1.44  #1.44MB limit
    MAX_CONTENT_LENGTH = MAX_VAULT_SIZE

    RECAPTCHA_ENABLED    = True
    RECAPTCHA_SITE_KEY   = '6LdWMBwUAAAAAESQQbFke65TMSxXqJ_XnMVX4hQh'
    RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")

class ProductionConfig(Config):
    HOST       = '0.0.0.0'

class DevelopmentConfig(Config):
    HOST ='127.0.0.1'
    DEBUG    = True
    TESTING  = True

config = DevelopmentConfig()
