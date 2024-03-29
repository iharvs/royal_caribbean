from django.contrib import admin

# Register your models here.
from .models import TZDBErrorLog, TZDBTimezone, TZDBZoneDetail

admin.site.register(TZDBErrorLog)
admin.site.register(TZDBTimezone)
admin.site.register(TZDBZoneDetail)
