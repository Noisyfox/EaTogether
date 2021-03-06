import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = PACKAGE_ROOT

DEBUG = True
DEPLOY = False

if DEPLOY:
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            'NAME': 'DB NAME',
            'USER': 'DB USER',
            'PASSWORD': 'DB PSW',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.spatialite",
            "NAME": "dev.db",
        }
    }

ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "UTC"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = int(os.environ.get("SITE_ID", 2 if DEPLOY else 1))

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/site_media/static/"

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static", "dist"),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = "w!a&k2%%#06qn6wnzav%=k#^y2u5vq*qzc!%vcoj+oq@qtba%z"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_ROOT, "ET", "templates"),
            os.path.join(PROJECT_ROOT, "ET_Cust", "templates"),
            os.path.join(PROJECT_ROOT, "ET_Owner", "templates"),
            os.path.join(PROJECT_ROOT, "ET_Cour", "templates"),
            os.path.join(PROJECT_ROOT, "ET_Admin", "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "pinax_theme_bootstrap.context_processors.theme",
            ],
        },
    },
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "ET.middleware.UserAccountScopeMiddleware",
]

ROOT_URLCONF = "ET.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "ET.wsgi.application"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.gis",

    # theme
    "pinax_theme_bootstrap",
    'crispy_forms',

    # project
    "ET",
    "ET_Admin",
    "ET_Cour",
    "ET_Cust",
    "ET_Owner",

    "location_field",
    'djcelery',

    'bootstrap3_duration',
    'captcha',

    # tools
    "mathfilters",
    "paypal.standard.ipn",
]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    }
}

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

AUTHENTICATION_BACKENDS = [
    'ET.auth_backends.UniversalAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SPATIALITE_LIBRARY_PATH = 'mod_spatialite'

GOOGLE_MAPS_V3_APIKEY = 'AIzaSyD8yC2qzzlufDZva6mc_d1QXi94XiMgu5k'
GOOGLE_MAPS_LIBRARIES = ['places']
GOOGLE_MAPS_LANGUAGE = 'en-AU'
GOOGLE_MAPS_REGION = 'AU'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Change the serializer of the session
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Celery settings
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Paypal setting
PAYPAL_TEST = True

NOCAPTCHA = True
RECAPTCHA_PUBLIC_KEY = '6LdqiwoUAAAAAHgHxbVWUf64pcdm5LvLyv29pkfg'
RECAPTCHA_PRIVATE_KEY = '6LdqiwoUAAAAAHKeO6SbUOdCSvBOZikVWuYUy2eT'
