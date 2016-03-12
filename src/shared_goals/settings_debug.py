from .settings import *

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails.txt")

INSTALLED_APPS += [
    'django_dominate',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8fbc%#p8369y4%9wqky9a9d7+4m7183@)vz4#)9y#h8p)r7d(t'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
