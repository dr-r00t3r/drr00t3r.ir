from django.shortcuts import render

from django.views.generic import TemplateView


# Create your views here.
class Home(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='core/index.html')
        pass

