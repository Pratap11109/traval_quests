from django.contrib import admin
from .models import TravelGroup, ExternalUser, ExternalUserManager
# Register your models here.
admin.site.register([ExternalUserManager, TravelGroup, ExternalUser])
