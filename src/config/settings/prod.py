from .base import *
from .base import env

SECRET_KEY = env.str("DJANGO_SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

FOOD_API_URL = env.str("DJANGO_FOOD_API_URL")