from django.contrib import admin

from iotcontroller.models import IOTDeviceModel


# Register your models here.
@admin.register(IOTDeviceModel)
class IOTControllerAdmin(admin.ModelAdmin):
    # fields = ['', 'device_name', 'device_status']
    list_display = ['id', 'device_name', 'device_status', 'modified_at']
