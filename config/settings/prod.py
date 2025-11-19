from .base import *

# Production settings
DEBUG = False
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "example.com").split(",")
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set in production")

# Additional production-specific settings can be added here
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQLDATABASE"),
        "USER": os.getenv("MYSQLUSER"),
        "PASSWORD": os.getenv("MYSQLPASSWORD"),
        "HOST": os.getenv("MYSQLHOST"),
        "PORT": os.getenv("MYSQLPORT", "3306"),
    }
}
