from pathlib import Path
import os
import dj_database_url

# Optional: load local .env (keeps secrets out of code)
try:
    import environ

    env = environ.Env()
    _env_path = Path(__file__).resolve().parent.parent / '.env'
    if _env_path.exists():
        environ.Env.read_env(str(_env_path))
except Exception:
    # If django-environ isn't installed or .env missing, fall back to normal os.environ
    pass

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Yahan humne environment ko "development" set kar diya hai manually
ENVIRONMENT = "development"

# SECURITY WARNING: keep the secret key used in production secret!
# Ab aapko .env ki zaroorat nahi, yahan apni key likh dein
SECRET_KEY = 'django-insecure-aapka-koi-bhi-lamba-secret-text-yahan'

# DEBUG mode on rahega kyunki hum development mein hain
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

CSRF_TRUSTED_ORIGINS = ['http://localhost:*', 'http://127.0.0.1:*']

# Application definition
INSTALLED_APPS = [
    'daphne', # Daphne ko sabse upar rehne dein
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_cleanup.apps.CleanupConfig',
    'cloudinary_storage',
    'cloudinary',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_htmx',
    'a_home',
    'a_users',
    'a_rtchat',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]


# Cloudinary settings verify karein (Images ke liye)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUD_NAME'),
    'API_KEY': os.environ.get('API_KEY'),
    'API_SECRET': os.environ.get('API_SECRET'),
}



ROOT_URLCONF = 'a_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ], # Root templates folder use hoga
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

ASGI_APPLICATION = 'a_core.asgi.application'

# Render ya Railway par ye variables environment se uthayenge
REDIS_URL = os.environ.get('REDIS_URL')

# Local/dev: don't depend on Redis (prevents WS disconnects when Redis isn't running).
if os.environ.get('ENVIRONMENT') == 'production' and REDIS_URL:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [REDIS_URL],
            },
        },
    }
else:
    # Note: InMemory channel layer works only within a single process.
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }

# Agar Render par ho toh DATABASE_URL use karo, warna local SQLite
if os.environ.get('ENVIRONMENT') == 'production':
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
# Static & Media Files
# Use leading slashes so URLs resolve correctly from nested routes (e.g. /chat/room/...)
STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]
STATIC_ROOT = BASE_DIR / 'staticfiles' 

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Chat upload limits
# Override if needed (e.g., for production):
# - CHAT_UPLOAD_LIMIT_PER_ROOM: max uploads per user per room
# - CHAT_UPLOAD_MAX_BYTES: max single file size
CHAT_UPLOAD_LIMIT_PER_ROOM = 20
CHAT_UPLOAD_MAX_BYTES = 10 * 1024 * 1024

# Agora (Voice/Video Calls)
# IMPORTANT: Do not hardcode your Agora certificate in git.
# Set these via environment variables or a local .env file.
AGORA_APP_ID = os.environ.get('AGORA_APP_ID', '')
AGORA_APP_CERTIFICATE = os.environ.get('AGORA_APP_CERTIFICATE', '')
AGORA_TOKEN_EXPIRE_SECONDS = int(os.environ.get('AGORA_TOKEN_EXPIRE_SECONDS', '3600'))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'

# Email settings
# - If EMAIL_HOST_USER + EMAIL_HOST_PASSWORD are set, send real emails via Gmail SMTP.
# - Otherwise, fall back to console backend (emails printed in runserver terminal).
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Ye purani settings ab aise likhi jati hain
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_LOGIN_METHODS = {'email', 'username'}

# Allauth: use custom styled forms (Tailwind classes)
ACCOUNT_FORMS = {
    'login': 'a_users.allauth_forms.CustomLoginForm',
    'signup': 'a_users.allauth_forms.CustomSignupForm',
    'reset_password': 'a_users.allauth_forms.CustomResetPasswordForm',
    'reset_password_from_key': 'a_users.allauth_forms.CustomResetPasswordKeyForm',
}