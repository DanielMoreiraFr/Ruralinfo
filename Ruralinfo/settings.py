"""
ruralinfo/settings.py — Configurações do projeto Ruralinfo Django
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-SUBSTITUA-ANTES-DE-QUALQUER-DEPLOY'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Biblioteca para estilizar widgets de form com Bootstrap via template
    'widget_tweaks',

    # Apps do Ruralinfo
    'accounts',
    'mural',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ruralinfo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'ruralinfo.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ★ CRÍTICO: deve ser definido ANTES do primeiro migrate
AUTH_USER_MODEL = 'accounts.Usuario'

# Redirecionamentos de autenticação
LOGIN_URL          = 'accounts:login'
LOGIN_REDIRECT_URL = 'mural:index'
LOGOUT_REDIRECT_URL = 'mural:index'

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE     = 'America/Recife'
USE_I18N      = True
USE_TZ        = True

# Arquivos estáticos
STATIC_URL = '/static/'

# ★ Arquivos de mídia (imagens dos avisos via ImageField)
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Mapeamento de mensagens → classes Bootstrap
from django.contrib.messages import constants as msg
MESSAGE_TAGS = {
    msg.DEBUG:   'secondary',
    msg.INFO:    'info',
    msg.SUCCESS: 'success',
    msg.WARNING: 'warning',
    msg.ERROR:   'danger',
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'