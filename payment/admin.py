from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Payment)
list_display = ('first_name', 'last_name', 'email','phone', 'amount','description','type','reference')
