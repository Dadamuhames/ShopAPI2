from django.contrib import admin
from .models import User
from rest_framework.authtoken.models import Token
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = [it.name for it in User._meta.fields if it.name != 'password']
    filter_horizontal = ('groups', 'user_permissions')

    class Meta:
        models = User



admin.site.register(User, UserAdmin)