
from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

CORS_ALLOW_ALL_ORIGINS = True


ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
   # 'lecturespaces',
    'mvcapi',
    'rest_framework',
    'django.contrib.sites',
    'corsheaders',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('postgres://api_database_fkxe_user:Xns2OnL587TwFhWLYSWplfzWOiJnH3nO@dpg-cmrq4r7109ks73fjknl0-a.oregon-postgres.render.com/api_database_fkxe'))
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'mvcapi/templates'),  # Add this line for mvcapi templates
            os.path.join(BASE_DIR, 'templates'),  # General project-level templates
            # If you still want to include lecturespaces templates, uncomment the following line
            # os.path.join(BASE_DIR, 'lecturespaces/templates'),
        ],
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