# Django settings for science_qa project.

from django.utils.translation import ugettext_lazy as _

import os.path
import sys

from ConfigParser import ConfigParser

DJANGO_ENV = os.environ.get('DJANGO_ENV')

if DJANGO_ENV == "production":
    DEBUG = False
else:
    DEBUG = True

TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_MAIN_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
    os.path.pardir)
)

# initialize system config
config = {
    'db': { 'name': None,
            'user': None,
            'password': None },
    'key': { 'secret': None },
    'other': { 'allowed_hosts': None }
}
# if we are in production read config from the productionsystem
if DJANGO_ENV == "production":
    try:
        CONFIG_FILE = '/etc/django/qa_science.conf'
        config_parser = ConfigParser()
        config_parser.read(CONFIG_FILE)
        config['db']['name'] = config_parser.get('db', 'name')
        config['db']['user'] = config_parser.get('db', 'user')
        config['db']['password'] = config_parser.get('db', 'password')
        config['key']['secret'] = config_parser.get('key', 'secret')
        try:
            with open(config['key']['secret']) as f:
                config['key']['secret'] = f.read().strip()
        except Exception:
            print("Failed to read secret key file in %s" % config['key']['secret'])
            print("Make sure it is readable.")
            sys.exit(1)

        allowed_hosts = config_parser.get('other', 'allowed_hosts')
        config['other']['allowed_hosts'] = allowed_hosts.split(',')
    except Exception:
        print("Failed to read configfile in %s" % CONFIG_FILE)
        print("Make sure it is readable.")
        sys.exit(1)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config['db']['name'] or 'science_qa',
        'USER': config['db']['user'] or 'qa_science',
        'PASSWORD': config['db']['password'] or 'dev_test_123',
        'HOST': '',
        'PORT': '',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = config['other']['allowed_hosts'] or []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Copenhagen'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('da', _('Danish')),
    ('en', _('English')),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_MAIN_ROOT, 'locale'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static_serve')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
        os.path.join(PROJECT_ROOT, 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# make sure this folder is writeable by the user running the django instance
ATTACHMENT_ROOT = os.path.join(PROJECT_ROOT, 'attachments')

# Make this unique, and don't share it with anybody.
SECRET_KEY = config['key']['secret'] or '5-v%(r#pd+mr&(81@%cmpr(hm&7b3^@ormcfh@_sokijh0j!)v'

# List of callables that know how to import templates from various sources.
if DEBUG:
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
    )
else:
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    #     'django.template.loaders.eggs.Loader',
    )

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

if DEBUG:
    MIDDLEWARE_CLASSES += ( 'crossxhr.XsSharing', )

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    # "django.contrib.auth.context_processors.PermWrapper",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)

ROOT_URLCONF = 'science_qa.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'science_qa.wsgi.application'

TEMPLATE_DIRS = (
        os.path.join(PROJECT_ROOT, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'south',
    'compressor',
    'bootstrap3',

    # apps
    'qa',
    'api_key_manager',
    'emaillist',
)

if DEBUG:
    INSTALLED_APPS += ( 'debug_toolbar', )

# django-compress
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

COMPRESS_ENABLED = not DEBUG
COMPRESS_OFFLINE = not DEBUG

# LOGIN URL
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
