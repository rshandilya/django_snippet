####### CUSTOM USER ########
# settings.py
AUTH_USER_MODEL = 'myapp.MyUser'

# myapp.models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

# myapp.admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
