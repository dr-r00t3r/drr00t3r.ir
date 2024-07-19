"""
URL configuration for drr00t3r project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings as django_settings, settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    path('iotcontroller/', include('iotcontroller.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # path('', include('core.urls')),
    # path(
    #     "sitemap.xml",
    #     TemplateView.as_view(template_name="sitemap.xml", content_type="text/xml"),
    # ),
    # path(
    #     "robots.txt",
    #     TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    # ),
    # path(
    #     "OneSignalSDKWorker.js",
    #     TemplateView.as_view(
    #         template_name="OneSignalSDKWorker.js", content_type="text/javascript"
    #     ),
    # ),
]
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(django_settings.MEDIA_URL, document_root=django_settings.MEDIA_ROOT)

handler400 = 'core.views.bad_request'
handler403 = 'core.views.permission_denied'
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)
