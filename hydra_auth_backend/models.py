# -*- coding: utf-8 -*-
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from hydra_auth_backend.auth import settings


class AbstractHydraUser(PermissionsMixin, models.Model):
    last_login = models.DateTimeField(_('last login'), default=timezone.now)
    username = models.CharField(_('username'), max_length=50, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_(
                                       'Designates whether the user can log '
                                       'into this admin '
                                       'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_(
                                        'Designates whether this user should '
                                        'be treated as '
                                        'active. Unselect this instead of '
                                        'deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    hydra_id = models.CharField(max_length=32)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    class Meta:
        abstract = True

    def get_username(self):
        "Return the identifying username for this User"
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.hydra_id

    def natural_key(self):
        return (self.get_username(),)

    def is_anonymous(self):
        """
        Always returns False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        raise NotImplementedError()

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        raise NotImplementedError()

    def get_full_name(self):
        return self.get_username()

    def get_short_name(self):
        return self.get_username()


def set_access_token(sender, request, user, **kwargs):
    request.session[settings.HYDRA_SESSION_KEY] = user.access_token

user_logged_in.connect(set_access_token)