from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(UserAdmin):
    fields = ('is_superuser', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Driver)
admin.site.register(Mechanic)
admin.site.register(Admin)
admin.site.register(Car)
