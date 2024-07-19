from rest_framework import serializers

from accounts.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = 'username', 'phone_number', 'email', 'IMEI'


# class AgentsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AgentsModel
#         fields = 'agents_admin', 'name_agents', 'city_agents'
