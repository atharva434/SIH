from dataclasses import fields
import django_filters

from .models import *

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model=MonumentTicket
        fields=['city', 'verified', ]
        

class DetailFilter(django_filters.FilterSet):
    class Meta:
        model=MonumentTicket
        fields=['date']
        