from config_secret import *

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_DISABLE_RATE_LIMITS = True

DEBUG = True

SQL_ECHO = False

# Google OAuth2 config (except GOOGLE_CLIENT_SECRET which must be set in config_secret.py)
GOOGLE_BASE_URL                     = 'https://www.google.com/accounts/'
GOOGLE_AUTH_URI                     = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_URI                    = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_CLIENT_EMAIL                 = '133082872359@developer.gserviceaccount.com'
GOOGLE_CLIENT_ID                    = '133082872359.apps.googleusercontent.com'
GOOGLE_AUTH_PROVIDER_X509_CERT_URL  = 'https://www.googleapis.com/oauth2/v1/certs'
GOOGLE_AUTH_SCOPE                   = 'https://www.googleapis.com/auth/userinfo.email'
GOOGLE_USERINFO_URI                 = 'https://www.googleapis.com/oauth2/v1/userinfo'
GOOGLE_REDIRECT_URI                 = 'http://localhost:5000/auth/google'
GOOGLE_JAVASCRIPT_ORIGIN            = 'http://localhost:5000'

# Twitter OAuth2 config
TWITTER_AUTH_URI                    = 'https://api.twitter.com/oauth/request_token'
