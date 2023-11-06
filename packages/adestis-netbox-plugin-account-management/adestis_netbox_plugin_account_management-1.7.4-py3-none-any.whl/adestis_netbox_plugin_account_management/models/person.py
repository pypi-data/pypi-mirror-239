from django.db import models
from django.urls import reverse
from adestis_netbox_plugin_account_management.models import *

from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from tenancy.models import *

__all__ = (
    'Person',
)

class Person(NetBoxModel):
    
    first_name = models.CharField(
        max_length=130
    )
    
    last_name = models.CharField(
        max_length=130
    )

    class Meta:
        verbose_name_plural = "Persons"
        verbose_name = 'Person'
        ordering = ('last_name', 'first_name',)

