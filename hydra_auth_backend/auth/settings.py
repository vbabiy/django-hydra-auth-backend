from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


HYDRA_API_KEY = getattr(settings, 'HYDRA_API_KEY', None)
if not HYDRA_API_KEY:
    raise ImproperlyConfigured("A HYDRA_API_KEY is required, in your settings.")

HYDRA_URL = getattr(settings, 'HYDRA_URL', "https://api.hydra.agoragames.com")


HYDRA_SESSION_KEY = getattr(settings, 'HYDRA_SESSION_KEY', 'HYDRA_SESSION')