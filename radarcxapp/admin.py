from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Condition)
admin.site.register(Coin)
admin.site.register(UserToken)
