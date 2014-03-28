from django.contrib.auth import logout

from django.core.exceptions import ImproperlyConfigured

from hydra_auth_backend.auth import settings, Hydra


class HydraUserMiddleware(object):
    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        if request.user.is_authenticated():
            if settings.HYDRA_SESSION_KEY in request.session:
                request.hydra = Hydra(
                    access_token=request.session[settings.HYDRA_SESSION_KEY])
                return
            else:
                logout(request)

