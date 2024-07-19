from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from accounts.models import CustomUser, RegionalInformation, State, City


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # self.fields['state'].queryset = State.objects.all()
        # self.fields['state'].label_from_instance = lambda obj: "%s" % obj.name_of_state
        # self.fields['city'].queryset = City.objects.all()
        # self.fields['city'].label_from_instance = lambda obj: "%s" % obj.name_of_city

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        # self.fields['state'].queryset = State.objects.all()
        # self.fields['state'].label_from_instance = lambda obj: "%s" % obj.name_of_state
        # self.fields['city'].queryset = City.objects.all()
        # self.fields['city'].label_from_instance = lambda obj: "%s" % obj.name_of_city

    class Meta:
        model = CustomUser
        fields = ("username",
                  # "state"
                  )


class RegionalInformationFrom(forms.ModelForm):
    databaseRegionalInformation = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 100}))

    class Meta:
        model = RegionalInformation
        fields = '__all__'
