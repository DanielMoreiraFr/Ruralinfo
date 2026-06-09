from pathlib import Path
from dotenv import load_dotenv
import os


load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega o arquivo .env da raiz do projeto


# ★ Lidos do .env — nunca hardcoded no código
SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Lê ALLOWED_HOSTS do .env — separa por vírgula se houver mais de um
_hosts = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h.strip() for h in _hosts.split(',') if h.strip()]

# Em desenvolvimento com DEBUG=True o Django já aceita localhost automaticamente,
# mas adicionamos explicitamente para evitar erros:
if DEBUG:
    ALLOWED_HOSTS += ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'mural',
    'locais',
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

# ★ Model de usuário customizado
AUTH_USER_MODEL = 'accounts.Usuario'

# Redirecionamentos de autenticação
LOGIN_URL           = 'accounts:login'
LOGIN_REDIRECT_URL  = 'mural:index'
LOGOUT_REDIRECT_URL = 'mural:index'

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE     = 'America/Recife'
USE_I18N      = True
USE_TZ        = True

# Arquivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Arquivos de mídia (uploads)
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
EMAIL_BACKEND       = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST          = os.environ.get('EMAIL_HOST')
EMAIL_PORT          = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL  = os.environ.get('DEFAULT_FROM_EMAIL')