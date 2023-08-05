import os


ADMIN_MEDIA_PREFIX = '/static/admin/'
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
AUTH_PROFILE_MODULE = 'django_pci_auth.UserProfile'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django_pci_auth.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
DEBUG = True
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # add 'django_admin_bootstrapped' into the INSTALLED_APPS list before
    # 'django.contrib.admin'
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # Django PCI Auth
    'axes',  # django-axes
    'dajaxice',  # django-dajaxice
    'django_pci_auth',
    'password_policies',  #django-password-policies,
)
LANGUAGE_CODE = 'en-us'
LOGIN_URL = '/admin/'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
MANAGERS = ADMINS
MEDIA_ROOT = ''
MEDIA_URL = ''
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'axes.middleware.FailedLoginMiddleware',
)
ROOT_URLCONF = 'django_pci_auth.urls'
SITE_ID = 1
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'dajaxice.finders.DajaxiceFinder',
)
SECRET_KEY = 'abc123'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # http://django-dajaxice.readthedocs.org/en/latest/installation.html
    # #installing-dajaxice
    'django.template.loaders.eggs.Loader',
)
# http://django-dajaxice.readthedocs.org/en/latest/installation.html\
# #installing-dajaxice
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
)
TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True


# Django PCI Auth Settings
PASSWORD_HASHERS = (  # Django 1.4 password hashing algorithms
    # From https://docs.djangoproject.com/en/1.4/topics/auth/:
    # "[redacted] This means that Django will use the first hash in the list
    # to store all passwords, but will support checking passwords stored with
    # the rest of the hashes in the list. If you remove a hash from the list
    # it will no longer be supported.
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

# From https://docs.djangoproject.com/en/1.4/topics/http/sessions/
SESSION_COOKIE_AGE = 7200

# django-axes defaults
AXES_LOGIN_FAILURE_LIMIT = 4
AXES_LOCK_OUT_AT_FAILURE = True
AXES_USE_USER_AGENT = False
AXES_COOLOFF_TIME = None
#AXES_LOGGER = axes.watch_login
AXES_LOCKOUT_TEMPLATE = None
AXES_LOCKOUT_URL = None
AXES_VERBOSE = True

# how many old password do you want to store, so they can't be reused.
OLD_PASSWORD_STORAGE_NUM = 4

# django-passwords defaults
PASSWORD_MIN_LENGTH = 6 # Defaults to 6
#PASSWORD_MAX_LENGTH = 120 # Defaults to None
#PASSWORD_DICTIONARY = "/usr/share/dict/words" # Defaults to None
#PASSWORD_MATCH_THRESHOLD = 0.9 # Defaults to 0.9, should be 0.0 - 1.0 where 1.0 means exactly the same.
#PASSWORD_COMMON_SEQUENCES = [] # Should be a list of strings, see passwords/validators.py for default
#PASSWORD_COMPLEXITY = { # You can ommit any or all of these for no limit for that particular set
#    "UPPER": 1,       # Uppercase
#    "LOWER": 1,       # Lowercase
#    "DIGITS": 1,      # Digits
#    "PUNCTUATION": 1, # Punctuation (string.punctuation)
#    "NON ASCII": 1,   # Non Ascii (ord() >= 128)
#    "WORDS": 1        # Words (substrings seperates by a whitespace)
#}
