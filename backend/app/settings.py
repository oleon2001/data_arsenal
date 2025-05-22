# app/settings.py

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx') # Asegúrate de tener una variable de entorno para esto en producción

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*'] # Sé más específico en producción


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'core_app',
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Asegúrate de que esta línea exista si tienes plantillas a nivel de proyecto
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'data_arsenal_v1'),
        'USER': os.environ.get('DB_USER', 'arsenal_user_v1'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'OS22122001'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-ve' # Cambiado a Español - Venezuela

TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = True # Para desarrollo, sé más restrictivo en producción
# O puedes usar CORS_ALLOWED_ORIGINS si conoces los orígenes específicos
# CORS_ALLOWED_ORIGINS = [
# "http://localhost:3000", # Ejemplo para un frontend React en desarrollo
# "http://127.0.0.1:3000",
# ]

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Aquí puedes añadir clases de autenticación si las necesitas, ej: TokenAuthentication
        # 'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny', # O sé más restrictivo según tus necesidades
    )
}

# Resend Configuration
RESEND_API_KEY = os.environ.get('RESEND_API_KEY', 'YOUR_RESEND_API_KEY_HERE') # ¡MUY IMPORTANTE! Usa variables de entorno en producción.
DEFAULT_FROM_EMAIL = 'Data Arsenal <onboarding@resend.dev>' # Cambia esto por tu email verificado en Resend
ALERT_EMAIL_RECIPIENTS = ['tu_correo_de_alerta@example.com'] # Lista de correos para recibir alertas

# Umbrales para datos de dispositivos
# Puedes expandir esto según sea necesario
DEVICE_DATA_THRESHOLDS = {
    'temperature': {'min': 5.0, 'max': 35.0},    # Grados Celsius
    'humidity':    {'min': 30.0, 'max': 70.0},   # Porcentaje
    'pressure':    {'min': 950.0, 'max': 1050.0}, # hPa
    # Ejemplo para un nuevo tipo de dato, si lo añades a DeviceData.DATA_TYPE_CHOICES
    # 'co2':         {'min': 300, 'max': 1000},    # ppm
}

# Logging (opcional, pero útil para depurar)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO', # Cambia a DEBUG para más detalle
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'core_app': { # Logger específico para tu app
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

AUTH_USER_MODEL = 'core_app.User'
