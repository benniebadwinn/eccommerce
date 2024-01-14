from pathlib import Path
from .info import *
import os
import smtplib
from email.message import EmailMessage

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR/'moontag_project'/'templates'
STATIC_DIR = BASE_DIR/'moontag_project'/'static'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0tax$akm$_6h9&!vh=lnf!lv#v@n*ys(6t9qr5ssrk$a5wt$)y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['1063-197-232-61-228.ngrok-free.app']

CSRF_TRUSTED_ORIGINS=['https://1063-197-232-61-228.ngrok-free.app']

SECURE_CROSS_ORIGIN_OPENER_POLICY='same-origin-allow-popups'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'daphne',
    'django.contrib.staticfiles',
    'moontag_app',
    'paypal.standard.ipn',
    'payment',
    'main',
    'crispy_forms',
    'account',
    'social_django',
    'channels',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'moontag_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'moontag_app.template_context.get_filters',
                'moontag_app.context_processors.total_price',
                'moontag_app.context_processors.cart_data',
                'moontag_app.context_processors.wishlist_count',
                'social_django.context_processors.login_redirect',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'moontag_project.wsgi.application'



# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT=os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


CRISPY_TEMPLATE_PACK = 'uni_form'






#mpesa credentials

MPESA_CONSUMER_KEY = '2QvSVG9FS2MtFWfcCfEztbn97QAkTW7d'
MPESA_CONSUMER_SECRET = 'QZTekqqfF8el0nAX'
MPESA_API_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'



AUTHENTICATION_BACKENDS = [
    'moontag_app.backends.CaseInsensitiveModelBackend',
    'social_core.backends.google.GoogleOAuth2',  # Enable Gmail authentication
    # 'social_core.backends.google.GoogleOpenId',  # for Google authentication
    'django.contrib.auth.backends.ModelBackend',
    # ... other backends
]

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         }
#     }
# }

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile']
# SOCIAL_AUTH_GOOGLE_PLUS_AUTH_EXTRA_ARGUMENTS = {
#       'access_type': 'offline'
# }
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {'prompt': 'select_account'}
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
SOCIAL_AUTH_URL_NAMESPACE = 'social'
# LOGIN_REDIRECT_URL = 'http://localhost:8000/auth/complete/google-oauth2/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'http://localhost:8000/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '468041107750-ruqdmubu7oei07lk4lbb5u7983amhfti.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'







SITE_ID = 1

ACCOUNT_UNIQUE_EMAIL =True
ACCOUNT_EMAIL_REQUIRED =True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_SIGNUP_REDIRECT_URL = "/shop/address/create"


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = "benniebadwin@gmail.com"
EMAIL_HOST_PASSWORD = 'xomv oqhb ztwo vgya'
DEFAULT_FROM_EMAIL = 'benniebadwin@gmail.com'



# Set your email credentials and server information
# smtp_server = 'smtp.badwin.online.com'  # Replace with your SMTP server
# port = 587  # Check with your email provider for the correct port number
# login = 'badwin@badwin.online'  # Replace with your email username
# password = 'luckyp@tch3r'  # Replace with your email password



PAYPAL_RECEIVER_EMAIL = 'benniebadwin@gmail.com'
PAYPAL_TEST = True




# settings.py

CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"




CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


ASGI_APPLICATION = "moontag_project.routing.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL = 'payment:pesapal_callback'  # this needs to be a reversible