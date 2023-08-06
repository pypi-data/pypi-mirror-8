import os
local_path = lambda path: os.path.join(os.path.dirname(__file__), path)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST_NAME': ':memory:'
    }
}

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.admin',
    'pipeline',
    'tests',
    'tests.tests'
]

ROOT_URLCONF = 'tests.urls'

MEDIA_URL = '/media/'

MEDIA_ROOT = local_path('media')

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
STATIC_ROOT = local_path('static/')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    ('pipeline', local_path('assets/')),
    local_path('assets2/'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

SECRET_KEY = "django-pipeline"

TEMPLATE_DIRS = (
    local_path('templates'),
)

PIPELINE_CSS = {
    'screen': {
        'source_filenames': (
            'pipeline/css/first.css',
            'pipeline/css/second.css',
            'pipeline/css/urls.css'
        ),
        'output_filename': 'screen.css'
    }
}
PIPELINE_JS = {
    'scripts': {
        'source_filenames': (
            'pipeline/js/first.js',
            'pipeline/js/second.js',
            'pipeline/js/application.js',
            'pipeline/templates/**/*.jst'
        ),
        'output_filename': 'scripts.js'
    },
    'scripts_async': {
        'source_filenames': (
            'pipeline/js/first.js',
            'pipeline/js/second.js',
            'pipeline/js/application.js',
            'pipeline/templates/**/*.jst'
        ),
        'output_filename': 'scripts_async.js',
        'extra_context': {
            'async': True,
        }
    },
    'scripts_defer': {
        'source_filenames': (
            'pipeline/js/first.js',
            'pipeline/js/second.js',
            'pipeline/js/application.js',
            'pipeline/templates/**/*.jst'
        ),
        'output_filename': 'scripts_defer.js',
        'extra_context': {
            'defer': True,
        }
    },
    'scripts_async_defer': {
        'source_filenames': (
            'pipeline/js/first.js',
            'pipeline/js/second.js',
            'pipeline/js/application.js',
            'pipeline/templates/**/*.jst'
        ),
        'output_filename': 'scripts_async_defer.js',
        'extra_context': {
            'async': True,
            'defer': True,
        }
    }
}
