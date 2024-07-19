from django import forms

from accounts.models import CustomUser
from iotcontroller.models import IOTDeviceModel


class IOTControllerFrom(forms.ModelForm):
    class Meta:
        model = IOTDeviceModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(IOTControllerFrom, self).__init__(*args, **kwargs)

        self.fields['author'].queryset = CustomUser.objects.all()
        self.fields['author'].label_from_instance = lambda obj: "%s" % obj.first_name
