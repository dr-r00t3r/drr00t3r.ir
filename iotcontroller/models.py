import uuid

from django.db import models

from accounts.models import CustomUser


# Create your models here.

class IOTDeviceModel(models.Model):
    DEVICE_STATUS = (
        (0, 'OFF'),
        (1, 'ZOM'),
        (2, 'ON'),
    )
    auther = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, verbose_name='سازنده')
    device_id = models.UUIDField('Unique UUID', default=uuid.uuid4)
    device_name = models.CharField(max_length=255, null=False, blank=False)
    device_status = models.IntegerField(choices=DEVICE_STATUS, default=-1)
    modified_at = models.DateTimeField(auto_now=True, verbose_name='زمان آخرین تغییرات')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد', editable=False)

    class Meta:
        db_table = "iot_controller"

    @property
    def get_user_name(self):
        try:
            if self.auther:
                return CustomUser.objects.get(id=int(self.auther_id)).phone_number
            else:
                return map(lambda c: c.name, CustomUser.objects.all())
        except Exception as e:
            return "Error:%s" % str(e)