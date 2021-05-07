from django.contrib import admin

# Register your models here.
from .models import Coin, Condition, user

admin.site.register(Condition)
admin.site.register(Coin)