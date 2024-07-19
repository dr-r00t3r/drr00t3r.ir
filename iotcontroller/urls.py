from django.conf.urls import include

from django.urls import path, re_path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
# from rest_framework.urlpatterns import format_suffix_patterns

from iotcontroller.views import IOTDevicesList, ModifiedSingleIOTDevice

router = routers.DefaultRouter()
# router.register(r'get_device_list', views.IOTDevicesList)
# router.register(r'get_single_device/<int:pk>/', modified_single_iotcontroller_detail)
urlpatterns = [
    path('', include(router.urls)),
    path('get_device_list/', IOTDevicesList.as_view()),
    path(r'get_single_device/<int:pk>/', ModifiedSingleIOTDevice.as_view()),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.











