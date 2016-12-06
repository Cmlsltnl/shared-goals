from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sharedgoals',
        'USER': 'admin',
        'PASSWORD': 'blah',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8fbc%#p8369y4%9wqky9a9d7+4m7183@)vz4#)9y#h8p)r7d(t'

ALLOWED_HOSTS += ['52.36.175.255', ]
