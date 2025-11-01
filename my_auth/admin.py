from django.contrib import admin

from my_auth.models import CustomUser

admin.site.register(CustomUser)
