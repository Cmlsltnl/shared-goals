from .settings import *

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails.txt")

INSTALLED_APPS += [
    'django_dominate',
]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
