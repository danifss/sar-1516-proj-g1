from django.contrib import admin
from .models import User, Services, PSW

# Register your models here.
admin.site.register(User)
admin.site.register(Services)
admin.site.register(PSW)
