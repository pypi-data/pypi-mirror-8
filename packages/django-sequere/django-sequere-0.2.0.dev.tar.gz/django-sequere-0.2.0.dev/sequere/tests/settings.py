DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SITE_ID = 1
DEBUG = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'sequere.backends.database',
    'sequere.backends.redis',
    'sequere.tests',
    'sequere.contrib.user',
    'sequere.contrib.timeline',
    'sequere',
]

SECRET_KEY = 'blabla'

ROOT_URLCONF = 'sequere.tests.urls'

TEST_RUNNER = 'sequere.tests.runner.DjangoTestSuiteRunner'

BROKER_BACKEND = 'memory'

CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

SEQUERE_TIMELINE_NYDUS_CONNECTION = {
    'backend': 'nydus.db.backends.redis.Redis',
    'router': 'nydus.db.routers.keyvalue.PartitionRouter',
    'hosts': {
        0: {'db': 0},
        1: {'db': 1},
        2: {'db': 2},
    }
}
