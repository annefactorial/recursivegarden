from pathlib import Path
from django.contrib import messages
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(str(BASE_DIR / '.env'))

DEBUG = env.bool('DEBUG', default=False)
SECRET_KEY = env('SECRET_KEY')

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'widget_tweaks',
    "django_htmx",
    "django_browser_reload",
    "tailwind",
    "theme",
    #"django_watchfiles",

]

DEBUG_APPS = [
    "django_extensions",
    "debug_toolbar",
]

CUSTOM_APPS = [
    'core',
]

if DEBUG:
    INSTALLED_APPS = [] + DJANGO_APPS + THIRD_PARTY_APPS + DEBUG_APPS + CUSTOM_APPS
else:
    INSTALLED_APPS = [] + DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE = []

if DEBUG:
    MIDDLEWARE += [
        "django_browser_reload.middleware.BrowserReloadMiddleware",
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

MIDDLEWARE += [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'ATOMIC_REQUESTS': True,
    }
}

'''
if DEBUG:
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
            "LOCATION": BASE_DIR / '.cache'
        }
    }

    DATABASES = {
        "default": {
            "ENGINE": 'django.db.backends.postgresql_psycopg2',
            "NAME": 'recursivegarden',
            "USER": 'recursivegarden',
            "PASSWORD": env('DB_PASSWORD'),
            "HOST": 'localhost',
            "PORT": "",
            'TEST': {
                'NAME': 'test_recursivegarden',
                'USER': 'recursivegarden',
                'PASSWORD': '',
            },
            'ATOMIC_REQUESTS': True,
        }
    }
'''

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    "127.0.0.1",
]

DJANGO_ADMIN_URL = env('DJANGO_ADMIN_URL', default='admin').strip('/')



# Email
ADMINS = [
    ('David Factorial', 'david@recursivegarden.com'),
]
SERVER_EMAIL = 'david@recursivegarden.com'

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    POSTMARK_API_KEY= env('POSTMARK_API_KEY')

    EMAIL_HOST = 'smtp.postmarkapp.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = POSTMARK_API_KEY
    EMAIL_HOST_PASSWORD = POSTMARK_API_KEY
    EMAIL_USE_TLS = True


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ]
}

TAILWIND_APP_NAME = 'theme'


ALLOWED_HOSTS = [
    "localhost",
    'recursivegarden.com',
    'socialmemorycomplex.io',
    'labyrinth.love',
    'hanjononduality.com',
]

