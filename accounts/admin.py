import json

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from accounts.forms import CustomUserChangeForm, CustomUserCreationForm, RegionalInformationFrom
from accounts.models import CustomUser, LogAccess, State, City, RegionalInformation


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password',
                           # 'user_type'
                           )}),
        (
            _('Personal info'),
            {'fields': ('username', 'IMEI', 'first_name', 'last_name',
                        # 'city', 'state',
                        'picture_profile', 'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       # 'city', 'state',
                       # 'user_type',
                       )}
         ),
    )

    model = CustomUser
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('id', 'username', 'email', 'IMEI', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    # raw_id_fields = ('state', 'city',)
    # autocomplete_fields = ('state', 'city',)


@admin.register(LogAccess)
class LogAccessAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'user_token', 'verify_code', 'ip_address')
    search_fields = ('phone_number', 'user_token', 'verify_code')
    ordering = ('phone_number',)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_of_state', 'name_of_briefly')
    search_fields = ('id', 'name_of_state',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_of_city', 'name_of_briefly', 'get_state_name')
    search_fields = ('id', 'name_of_city',)


@admin.register(RegionalInformation)
class RegionalInformationAdmin(admin.ModelAdmin):
    fields = ['databaseRegionalInformation']
    form = RegionalInformationFrom

    def save_model(self, request, obj, form, change):
        provinc_json = json.loads(obj.databaseRegionalInformation)
        for i in range(len(provinc_json)):
            name_of_state_of_briefly = i
            name_of_state = provinc_json[i]['name']
            State.objects.create(name_of_briefly=name_of_state_of_briefly, name_of_state=provinc_json[i]['name'])

            for j in range(len(provinc_json[i]['Cities'])):
                name_of_city_of_briefly = j
                name_of_city = provinc_json[i]['Cities'][j]['name']
                print(State.objects.get(name_of_briefly=name_of_state_of_briefly))
                City.objects.create(state=State.objects.get(name_of_briefly=name_of_state_of_briefly),
                                    name_of_briefly=name_of_city_of_briefly, name_of_city=name_of_city)
                # print(provinc_json[i]['Cities'][j]['name'])
            # print(name_of_state_of_briefly, name_of_state, "\n")
        # for i in provinc_json:
        #     # received_json=json.loads(i)
        #     print(i)
        #     obj.databaseRegionalInformation = UploadCategory.objects.get(id=int(obj.category.pk)).name
        #     Tags.objects.all().filter(video=UploadManager.objects.get(id=obj.id)).update(
        #         video=UploadManager.objects.get(id=obj.id), tag_keys=obj.tag)
        # else:
        #     obj.tag_of_name = UploadCategory.objects.get(id=int(obj.category.pk)).name
        super(RegionalInformationAdmin, self).save_model(request, obj, form, change)
        # if Tags.objects.values().filter(video=UploadManager.objects.get(id=obj.id)):
        #     pass
        # else:
        #     Tags.objects.all().filter(video=UploadManager.objects.get(id=obj.id)).create(
        #         video=UploadManager.objects.get(id=obj.id), tag_keys=obj.tag)

# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(LogAccess, LogAccessAdmin)
# admin.site.register(State, StateAdmin)
# admin.site.register(City, CityAdmin)
# admin.site.register(RegionalInformation, RegionalInformationAdmin)
# admin.site.register(MyHairdressers, MyHairdressersAdmin)
# admin.site.register(Customer, CustomerAdmin)
