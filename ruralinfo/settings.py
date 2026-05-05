"""
settings.py — Configurações do projeto ruralinfo
Gerado para Django 5.x — Python 3.11+

INSTRUÇÕES DE USO:
1. Copie este arquivo para ruralinfo/settings.py
2. Substitua SECRET_KEY por um valor único gerado com:
       python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
3. Em produção, leia as variáveis sensíveis de variáveis de ambiente (os.environ).
"""

from pathlib import Path

# Diretório raiz do projeto (onde está manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent


# =============================================================================
# SEGURANÇA — NUNCA commitar o SECRET_KEY real no git
# =============================================================================
SECRET_KEY = '-diezdh$1s11m#73665y^&(07fgw=(i69i(^dnm3$f$@#hmp4d'

DEBUG = True  # Mude para False em produção

ALLOWED_HOSTS = []  # Em produção: ['ruralinfo.ufrpe.br', 'www.ruralinfo.ufrpe.br']


# =============================================================================
# APPS INSTALADOS
# =============================================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps do projeto Ruralinfo
    'accounts',
    'mural',
    'campus',
    'transporte'
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
        # DIRS: diz ao Django onde encontrar os templates globais (base.html etc.)
        'DIRS': [BASE_DIR / 'templates'],
        # APP_DIRS: também busca templates dentro de cada app/templates/
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


# =============================================================================
# BANCO DE DADOS
# =============================================================================
# SQLite para desenvolvimento — substitua por PostgreSQL em produção:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'ruralinfo_db',
#         'USER': 'postgres',
#         'PASSWORD': os.environ.get('DB_PASSWORD'),
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =============================================================================
# ★ MODEL DE USUÁRIO CUSTOMIZADO — CONFIGURAÇÃO CRÍTICA ★
#
# DEVE ser definido ANTES de rodar o primeiro `migrate`.
# Se definido depois, será necessário resetar o banco de dados completo.
# Referencia o model Usuario no app accounts usando a notação 'app.Model'.
# =============================================================================
AUTH_USER_MODEL = 'accounts.Usuario'


# =============================================================================
# AUTENTICAÇÃO — Redirecionamentos
# =============================================================================
# Para onde redirecionar usuários não autenticados quando acessam uma view
# protegida por @login_required
LOGIN_URL = 'accounts:login'

# Para onde redirecionar após login bem-sucedido (se não houver ?next=)
LOGIN_REDIRECT_URL = 'mural:lista'

# Para onde redirecionar após logout
LOGOUT_REDIRECT_URL = 'accounts:login'


# =============================================================================
# ARQUIVOS ESTÁTICOS (CSS, JS, imagens do projeto)
# =============================================================================
STATIC_URL = '/static/'
# Em produção, após `collectstatic`:
# STATIC_ROOT = BASE_DIR / 'staticfiles'


# =============================================================================
# ★ ARQUIVOS DE MÍDIA (uploads de usuários — imagens dos avisos) ★
#
# MEDIA_URL:  URL pública para acessar os uploads (ex: /media/mural/img.jpg)
# MEDIA_ROOT: Caminho físico no servidor onde os arquivos são salvos.
#             O ImageField usa `upload_to` para criar subpastas dentro de MEDIA_ROOT.
# =============================================================================
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# =============================================================================
# INTERNACIONALIZAÇÃO
# =============================================================================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Recife'
USE_I18N = True
USE_TZ = True  # Armazena datas em UTC no banco, exibe no TIME_ZONE local


# =============================================================================
# VALIDADORES DE SENHA (painel admin)
# =============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =============================================================================
# SISTEMA DE MENSAGENS (flash messages)
# Mapeamos os levels do Django para as classes do Bootstrap 5
# =============================================================================
from django.contrib.messages import constants as messages_constants

MESSAGE_TAGS = {
    messages_constants.DEBUG:   'secondary',
    messages_constants.INFO:    'info',
    messages_constants.SUCCESS: 'success',
    messages_constants.WARNING: 'warning',
    messages_constants.ERROR:   'danger',  # Bootstrap usa 'danger', Django usa 'error'
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'