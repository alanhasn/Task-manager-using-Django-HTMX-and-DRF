import os
from pathlib import Path

from decouple import config

# ==================== [ BASE DIR ] ====================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==================== [ GENERAL SETTINGS ] ====================
SECRET_KEY = config("SECRET_KEY", default="django-insecure-production-secret-key")
DEBUG = config("DEBUG", default=True, cast=bool)
ENVIRONMENT = config("ENVIRONMENT", default="development")

ALLOWED_HOSTS = []

# ==================== [ INSTALLED APPS ] ====================
CUSTOM_APPS = [ 
    "todo",
    "accounts",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_spectacular",
    "widget_tweaks",
    # Auth
    'social_django',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

# ==================== [ MIDDLEWARE ] ====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # In prod
    'project.middleware.RestrictAdminMiddleware'
]

# ==================== [ URLS & TEMPLATES ] ====================
ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# ==================== [ DATABASE ] ====================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==================== [ AUTHENTICATION / ACCOUNTS ] ====================
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GITHUB_KEY = config("GITHUB_CLIENT_ID")
SOCIAL_AUTH_GITHUB_SECRET = config("GITHUB_CLIENT_SECRET")

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config("GOOGLE_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config("GOOGLE_CLIENT_SECRET")

# =================== [Email Verfication] =====================
EXPIRE_AFTER = "1d" # Link expires after one day
MAX_RETRIES = 4 # 4 retries for resend the email verfication

# ==================== [ PASSWORD VALIDATORS ] ====================
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

# ==================== [ INTERNATIONALIZATION ] ====================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==================== [ STATIC FILES ] ====================
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# ==================== [ DJANGO DEFAULTS ] ====================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

# ==================== [ REST FRAMEWORK ] ====================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # Throttling
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'list_tasks': '60/hour',
        'todo_edit': '30/hour',
        'user_info': '20/hour',
    },

    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# ==================== [ DRF SPECTACULAR ] ====================
SPECTACULAR_SETTINGS = {
    'TITLE': 'TODO List Manager',
    'DESCRIPTION': 'TODO List API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# ==================== [ EMAIL SETTINGS ] ====================
if ENVIRONMENT == "production":
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
    EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

