from constance import config
from dal import autocomplete
from django.conf.urls import url
from django.core import serializers
from django.core.paginator import Paginator
from django.http import request, HttpResponse
from django.db.models import F, Q, ExpressionWrapper, BooleanField
from django.utils.encoding import uri_to_iri, smart_str

from django.views.generic import TemplateView
from django.views.generic.base import View
from taggit.models import Tag

from core.models import *
from frontend.views import tasks_json, detail_view

import logging

# Standard instance of a logger with __name__
stdlogger = logging.getLogger(__name__)

app_name = "frontend"

class IndexView(TemplateView):
    template_name="frontend/index.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['most_search'] = Medicine.objects.filter(status=True).order_by('-views')[0:12]
        context['experts'] = Expert.objects.filter(status=True)[0:3]
        return context

class RecommendView(TemplateView):
    template_name='frontend/recommend.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['experts'] = Expert.objects.filter(status=True)[0:3]
        context['videos'] = Video.objects.filter(status=True)[0:3]
        return context

class MedicineListView(TemplateView):
    template_name='frontend/medicine_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        q = self.request.GET.get('q')

        if q is not None:
            medicine_list = Medicine.objects.filter(status=True).filter(Q(name__istartswith=q) or Q(name__icontains=q))

        else:
            medicine_list = Medicine.objects.filter(status=True).order_by("-created_at")



        paginator = Paginator(medicine_list, 12) # Show 25 contacts per page

        page = self.request.GET.get('page')
        medicines = paginator.get_page(page)

        path = ''
        path += "%s" % "&".join(["%s=%s" % (key, value) for (key, value) in self.request.GET.items() if not key=='page' ])

        context['path'] = path

        context['medicines'] = medicines
        context['alphabets'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        return context


class SpecialView(TemplateView):
    template_name='frontend/special_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        q = self.request.GET.get('q')

        if q is not None:
            medicine_list = Special.objects.filter(status=True).filter(Q(name__istartswith=q) or Q(name__icontains=q))
        else:
            medicine_list = Special.objects.filter(status=True).order_by("-created_at")

        paginator = Paginator(medicine_list, 12) # Show 25 contacts per page

        path = ''
        path += "%s" % "&".join(["%s=%s" % (key, value) for (key, value) in self.request.GET.items() if not key=='page' ])

        context['path'] = path

        page = self.request.GET.get('page')
        medicines = paginator.get_page(page)

        context['medicines'] = medicines
        context['alphabets'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        return context


class TagView(TemplateView):

    template_name='frontend/tag.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        slug = self.kwargs['slug']
        tag = Tag.objects.get(slug__exact=slug)

        medicines = Medicine.objects.filter(Q(status=True) & Q(tags=tag)).order_by("-created_at")[0:12]
        context['medicines'] = medicines
        context['tag'] = tag
        return context

class SearchView(TemplateView):
    template_name='frontend/search.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        search_value = self.request.GET.get('search_value')
        medicines = Medicine.objects.filter(status=True).filter(name__icontains=search_value).order_by("-created_at")[0:12]
        context['medicines'] = medicines

        return context


class DiseaseListView(TemplateView):
    template_name='frontend/disease_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        q = self.request.GET.get('q')

        if q is not None:
            medicine_list = Disease.objects.filter(status=True).filter(name__icontains=q).order_by("-created_at")
        else:
            medicine_list = Disease.objects.filter(status=True).order_by("-created_at")


        context['medicines'] = medicine_list

        return context


class DrugListView(TemplateView):
    template_name='frontend/drug_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        q = self.request.GET.get('q')

        if q is not None:
            medicine_list = Drug.objects.filter(status=True).filter(Q(name__istartswith=q) or Q(name__icontains=q))
        else:
            medicine_list = Drug.objects.filter(status=True).order_by("-created_at")

        paginator = Paginator(medicine_list, 12) # Show 25 contacts per page

        page = self.request.GET.get('page')
        medicines = paginator.get_page(page)

        path = ''
        path += "%s" % "&".join(["%s=%s" % (key, value) for (key, value) in self.request.GET.items() if not key=='page' ])

        context['path'] = path
        context['medicines'] = medicines
        context['alphabets'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        return context



class ExpertView(TemplateView):
    template_name='frontend/expert.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['experts'] = Expert.objects.filter(status=True)[0:3]
        context['videos'] = Video.objects.filter(status=True)[0:3]
        return context

class NewsView(TemplateView):
    template_name='frontend/news.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        category = Category.objects.get(pk=2)

        medicine_list = Post.objects.filter(Q(status=True) & Q(category=category)).order_by("-created_at")

        paginator = Paginator(medicine_list, 12) # Show 25 contacts per page

        page = self.request.GET.get('page')
        medicines = paginator.get_page(page)

        context['medicines'] = medicines
        context['category'] = category

        return context
class InfoView(TemplateView):
    template_name='frontend/info.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        category = Category.objects.get(pk=3)

        medicine_list = Post.objects.filter(Q(status=True) & Q(category=category)).order_by("-created_at")

        paginator = Paginator(medicine_list, 12) # Show 25 contacts per page

        page = self.request.GET.get('page')
        medicines = paginator.get_page(page)

        context['medicines'] = medicines
        context['category'] = category

        return context


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),


    url(r'^gioi-thieu$', RecommendView.as_view(), name='recommend'),


    url(r'^tra-cuu-duoc-lieu$', MedicineListView.as_view(), name='medicine_list'),
    url(r'^tra-cuu-theo-danh-luc$', SpecialView.as_view(), name='special_list'),
    url(r'^tra-cuu-theo-benh$', DiseaseListView.as_view(), name='disease_list'),
    url(r'^tra-cuu-theo-bai-thuoc$', DrugListView.as_view(), name='drug_list'),

    url(r'^chuyen-gia-duoc-lieu$', ExpertView.as_view(), name='expert'),
    url(r'^ban-tin-duoc-lieu$', NewsView.as_view(), name='news'),
    url(r'^thong-tin-khoa-hoc$', InfoView.as_view(), name='info'),


    url(r'^tu-khoa-(?P<slug>[\w-]+)$', TagView.as_view(), name='tag'),
    url(r'^tim-kiem$', SearchView.as_view(), name='search'),
    url(r'^api/(?P<content>[\w-]+)$', tasks_json, name='api'),
    url(r'^(?P<slug>[\w-]+)\.html$', detail_view, name='content_detail'),
]