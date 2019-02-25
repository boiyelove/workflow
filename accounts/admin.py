from django.contrib import admin
from .models import UserProfile, DonateMethod
# Register your models here.


admin.site.register(UserProfile)
admin.site.register(DonateMethod)