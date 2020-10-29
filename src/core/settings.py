"""
Django settings for core project.
Generated by 'django-admin startproject' using Django 3.1.1.
For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# print(BASE_DIR)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's+1@c*&8(4h&m7k%g^)!exg=(7re4v^gf_sr#4%i$$hen7fz_t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party Apps
    'phonenumber_field',
    'crispy_forms',
    'phone_verify',
    

    # Local Apps
    'accounts',
    'addresses',
    'profiles',
    'vendors',
    'products',
    'orders',
    'billing',
    'home',
    'adminPanel'
]

AUTH_USER_MODEL = 'accounts.User'  # changes the built-in user model to ours
LOGIN_URL = '/auth/login/'
LOGIN_URL_REDIRECT = '/'
LOGOUT_URL = '/auth/logout/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGOUT_REDIRECT_URL = '/auth/login/'
ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath('templates')],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

LOCAL_DATABASE = True
if LOCAL_DATABASE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'dsec-v0-0',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': '',
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'd66vfaflo11guc',
            'USER': 'tugdtckdkddwwk',
            'PASSWORD': '1879cef240bdd39a1c248a43d67b9296446fc7380f61f26ebec6b5ee2f561bcc',
            'HOST': 'ec2-54-156-53-71.compute-1.amazonaws.com',
            'PORT': '5432',
        }
    }

# DATABASE_URL=postgres://{user}:{password}@{hostname}:{port}/{database-name}
# DATABASE_URL = postgres://tugdtckdkddwwk:1879cef240bdd39a1c248a43d67b9296446fc7380f61f26ebec6b5ee2f561bcc@ec2-54-156-53-71.compute-1.amazonaws.com:5432/d66vfaflo11guc


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Settings for phone_verify
PHONE_VERIFICATION = {
    'BACKEND': 'accounts.sms_backends.bdsms.BdsmsBackend',  # Path to the custom backend class which we will be creating in further steps
    'OPTIONS': {
        # define options required for your service
        'BDSMS_TOKEN': 'd7b8a552f6c00b66408a47c00c1191bf',
        'BDSMS_ENDPOINT': 'https://sms.greenweb.com.bd/api.php'
        # 'KEY': 'Fake Key',
        # 'SECRET': 'Fake secret',
        # 'FROM': '+1232328372987',
        # 'SANDBOX_TOKEN': '123456',  # Optional for sandbox utility
    },
    'TOKEN_LENGTH': 6,
    'MESSAGE': 'Welcome to {app}! Please use security code {security_code} to proceed.',
    'APP_NAME': 'DSEC',
    'SECURITY_CODE_EXPIRATION_TIME': 300,  # In seconds only
    'VERIFY_SECURITY_CODE_ONLY_ONCE': True,  # If False, then a security code can be used multiple times for verification
}



# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR.joinpath("staticfiles"),
]

STATIC_ROOT = BASE_DIR.parent.joinpath("static_cdn", "static_root")


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent.joinpath("static_cdn", "media_root")

PROTECTED_ROOT = BASE_DIR.parent.joinpath("static_cdn", "protected_media")
CRISPY_TEMPLATE_PACK = 'bootstrap4'
