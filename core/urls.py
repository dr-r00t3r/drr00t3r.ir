from django.urls import path

from core.views import Home

urlpatterns = [
    path(r'', Home.as_view()),
]
