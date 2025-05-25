# backend/app/settings.py

from pathlib import Path
import os # Para variables de entorno

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Asegúrate de que esta clave sea única y secreta en producción.
# Puedes generar una nueva con: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-CAMBIA_ESTA_CLAVE_SECRETA_POR_UNA_NUEVA_Y_ALEATORIA')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS_STRING = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STRING.split(',') if host.strip()]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken', # Para la autenticación por token
    'corsheaders',            # Para manejar CORS
    'core_app',               # Tu aplicación principal
    # ... otras apps
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # Asegúrate que esté antes de CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core_app', 'templates')],
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# !!! IMPORTANTE: REVISA CUIDADOSAMENTE ESTOS VALORES !!!
# El error UnicodeDecodeError suele ocurrir si alguno de estos valores
# (especialmente PASSWORD, pero también NAME, USER, HOST) contiene caracteres
# especiales (como tildes: ó, á, ñ, etc.) que no son ASCII puros.
#
# 1. Si usas variables de entorno (os.environ.get), verifica los valores
#    en tu archivo .env o en la configuración de tu sistema.
# 2. Si NO usas variables de entorno, REEMPLAZA los valores de ejemplo
#    ('tu_basedatos', 'tu_usuario', 'tu_contraseña') con tus credenciales REALES.
# 3. TEMPORALMENTE, para diagnosticar, intenta usar una contraseña de base de datos
#    que SÓLO contenga letras (a-z, A-Z) y números (0-9), sin símbolos ni tildes.
#    Si esto soluciona el UnicodeDecodeError, el problema estaba en los caracteres
#    de tu contraseña o algún otro parámetro de conexión.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'data_arsenal_nueva',
        'USER': 'arsenal_user_nuevo',
        'PASSWORD': 'NuevaClave123',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}
# Para desarrollo local rápido con SQLite (si no tienes PostgreSQL configurado o para probar):
# Descomenta las siguientes líneas y comenta la configuración de PostgreSQL de arriba.
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Modelo de Usuario Personalizado
AUTH_USER_MODEL = 'core_app.User'


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-ve' # Español Venezuela como ejemplo

TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# STATIC_ROOT es para 'collectstatic' en producción.
STATIC_ROOT = BASE_DIR / 'staticfiles_collected'

# STATICFILES_DIRS es para encontrar estáticos durante el desarrollo.
# El warning (staticfiles.W004) indica que el directorio 'backend/static' no existe.
# Crea este directorio o ajusta la ruta si tus estáticos están en otro lugar.
STATICFILES_DIRS = [
    BASE_DIR / "static", # Busca una carpeta 'static' en el directorio 'backend/'
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de Django REST framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10
}

# Configuración de CORS
# Asegúrate que los orígenes de tu frontend estén aquí.
CORS_ALLOWED_ORIGINS_STRING = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS_STRING.split(',') if origin.strip()]
CORS_ALLOW_CREDENTIALS = True
# Para mayor seguridad en producción, considera usar CORS_ALLOWED_ORIGIN_REGEXES
# o especificar los orígenes exactos en lugar de depender de un string separado por comas si es complejo.

# Configuración de Email (usando Resend como en tu email_utils.py)
# Asegúrate de que estas variables de entorno estén configuradas correctamente.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # O un backend personalizado si usas Resend directamente
RESEND_API_KEY = os.environ.get('RESEND_API_KEY') # Obtener desde el entorno
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'oswaldoleon72@example.com') # Cambia a tu email
ALERT_EMAIL_RECIPIENTS_STRING = os.environ.get('ALERT_EMAIL_RECIPIENTS', 'alerts@example.com')
ALERT_EMAIL_RECIPIENTS = [email.strip() for email in ALERT_EMAIL_RECIPIENTS_STRING.split(',') if email.strip()]


# Configuración de Logging (Básico)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': { # Añadido para un formato más detallado
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple', # Usar formato simple para la consola
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.db.backends': { # Para ver queries SQL si es necesario
            'handlers': ['console'],
            'level': 'INFO', # Cambia a DEBUG para ver queries
            'propagate': False,
        },
        'core_app': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

