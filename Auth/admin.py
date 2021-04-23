from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User, UserAdmin)
admin.site.register(Driver)
admin.site.register(Mechanic)
admin.site.register(Admin)
admin.site.register(Car)
