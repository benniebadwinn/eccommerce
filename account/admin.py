from django.contrib import admin
from .models import *


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','firstname','lastname','phone')

admin.site.register(UserProfuile)
admin.site.register(subscriptions)
admin.site.register(Wallet)
admin.site.register(Transaction)
