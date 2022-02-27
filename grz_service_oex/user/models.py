from django.db import models
from ks_shared.django.model import AbstractWXMPUser
from ks_shared.django.model_utils import BaseModelSoftDeletable
from model_utils import Choices
from model_utils.fields import StatusField


class User(AbstractWXMPUser):
    ROLE_CHOICES = Choices(
        ('user', 'User'),
        ('storekeeper', 'Storekeeper'),
    )
    role = StatusField(choices_name='ROLE_CHOICES', default=ROLE_CHOICES.user)


class Config(BaseModelSoftDeletable):
    key = models.CharField(max_length=255)
    value = models.JSONField(default=dict)

    def __str__(self):
        return self.key
