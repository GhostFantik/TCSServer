from django.contrib import admin
from Repairs.models import Tag, RepairRequest, Repair, TypeRepair

admin.site.register(Tag)
admin.site.register(RepairRequest)
admin.site.register(Repair)
admin.site.register(TypeRepair)
