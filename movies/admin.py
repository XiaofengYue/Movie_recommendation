from django.contrib import admin

# Register your models here.

from .models import Rate,Info,User

admin.site.register(Rate)
admin.site.register(Info)
admin.site.register(User)