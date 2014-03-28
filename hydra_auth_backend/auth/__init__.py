from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from hydra_auth_backend.auth.hydra import Hydra


class HydraBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        client = Hydra()
        if not client.authenticate(username, password):
            return None
        model = get_user_model()
        hydra_account = client.account()
        print(hydra_account)
        try:
            user = model.objects.get(hydra_id=hydra_account['id'])
        except model.DoesNotExist:
            user = model()
            user.hydra_id = hydra_account['id']
            user.username = hydra_account['identity']['username']
            user.save()


        user.access_token = client.access_token
        return user
