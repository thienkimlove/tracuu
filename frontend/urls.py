from django.conf.urls import url
from django.views.generic import TemplateView

app_name = "frontend"

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="frontend/index.html"), name='index'),
]