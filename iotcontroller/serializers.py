from rest_framework import serializers

from iotcontroller.models import IOTDeviceModel


class IOTControllerSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IOTDeviceModel
        fields = ['device_id', 'device_name', 'device_status']