from constance import config
from django.conf.urls import url
from django.core import serializers
from django.core.paginator import Paginator
from django.http import request, HttpResponse
from django.db.models import F, Q
from django.utils.encoding import uri_to_iri, smart_str

from django.views.generic import TemplateView
from django.views.generic.base import View
from taggit.models import Tag

from core.models import *
from frontend.views import tasks_json

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
            medicine_list = Medicine.objects.filter(status=True).filter(name__icontains=q).order_by("-created_at")
        else:
            medicine_list = Medicine.objects.filter(status=True).order_by("-created_at")

        paginator = Paginator(medicine_list, 12) # Show 25 contacts per page

        page = self.request.GET.get('page')
        medicines = paginator.get_page(page)

        context['medicines'] = medicines
        context['alphabets'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        return context

class MedicineDetailView(TemplateView):
    template_name='frontend/medicine_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        slug = self.kwargs['slug']

        medicine = Medicine.objects.filter(slug__exact=slug).first()
        Medicine.objects.filter(pk=medicine.id).update(views=F('views') + 1)
        context['medicine'] = medicine
        related_objects = medicine.tags.similar_objects()[0:2]
        if not related_objects:
            related_objects = Medicine.objects.filter(status=True).filter(~Q(id = medicine.id)).order_by("-created_at")[0:2]
        context['related_objects'] = related_objects
        return context


class SpecialView(TemplateView):
    template_name='frontend/special_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        q = self.request.GET.get('q')

        if q is not None:
            medicine_list = Special.objects.filter(status=True).filter(name__icontains=q).order_by("-created_at")
        else:
            medicine_list = Special.objects.filter(status=True).order_by("-created_at")

        paginator = Paginator(medicine_list, 12) # Show 25 contacts per page

        page = self.request.GET.get('page')
        medicines = paginator.get_page(page)

        context['medicines'] = medicines
        context['alphabets'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        return context


class SpecialDetailView(TemplateView):
    template_name='frontend/special_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        slug = self.kwargs['slug']

        medicine = Special.objects.filter(slug__exact=slug).first()
        Special.objects.filter(pk=medicine.id).update(views=F('views') + 1)
        context['medicine'] = medicine
        related_objects = medicine.tags.similar_objects()[0:2]
        if not related_objects:
            related_objects = Special.objects.filter(status=True).filter(~Q(id = medicine.id)).order_by("-created_at")[0:2]
        context['related_objects'] = related_objects
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

        paginator = Paginator(medicine_list, 12) # Show 25 contacts per page

        page = self.request.GET.get('page')
        medicines = paginator.get_page(page)

        context['medicines'] = medicines

        return context

class DiseaseDetailView(TemplateView):
    template_name='frontend/disease_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        slug = self.kwargs['slug']

        disease = Disease.objects.filter(slug__exact=slug).first()
        Disease.objects.filter(pk=disease.id).update(views=F('views') + 1)
        context['disease'] = disease
        medicines = Medicine.objects.filter(disease=disease).order_by("-created_at")[0:5]

        context['medicines'] = medicines
        return context

class DrugListView(TemplateView):
    template_name='frontend/drug_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        q = self.request.GET.get('q')

        if q is not None:
            medicine_list = Drug.objects.filter(status=True).filter(name__icontains=q).order_by("-created_at")
        else:
            medicine_list = Drug.objects.filter(status=True).order_by("-created_at")

        paginator = Paginator(medicine_list, 12) # Show 25 contacts per page

        page = self.request.GET.get('page')
        medicines = paginator.get_page(page)

        context['medicines'] = medicines
        context['alphabets'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        return context

class DrugDetailView(TemplateView):
    template_name='frontend/drug_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        slug = self.kwargs['slug']

        drug = Drug.objects.filter(slug__exact=slug).first()
        Drug.objects.filter(pk=drug.id).update(views=F('views') + 1)
        context['drug'] = drug
        related_objects = drug.tags.similar_objects()[0:2]
        if not related_objects:
            related_objects = Drug.objects.filter(status=True).filter(~Q(id = drug.id)).order_by("-created_at")[0:2]
        context['related_objects'] = related_objects

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

        return context
class PostDetailView(TemplateView):
    template_name='frontend/post_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        slug = self.kwargs['slug']

        medicine = Post.objects.filter(slug__exact=slug).first()
        Post.objects.filter(pk=medicine.id).update(views=F('views') + 1)
        context['medicine'] = medicine
        related_objects = medicine.tags.similar_objects()[0:2]
        if not related_objects:
            related_objects = Post.objects.filter(status=True).filter(~Q(id = medicine.id)).order_by("-created_at")[0:2]
        context['related_objects'] = related_objects
        context['latest_objects'] = Post.objects.filter(status=True).filter(~Q(id = medicine.id)).order_by("-created_at")[0:3]
        return context

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),


    url(r'^gioi-thieu\.html$', RecommendView.as_view(), name='recommend'),


    url(r'^tra-cuu-duoc-lieu\.html$', MedicineListView.as_view(), name='medicine_list'),
    url(r'^tra-cuu-theo-danh-luc\.html$', SpecialView.as_view(), name='special_list'),
    url(r'^tra-cuu-theo-benh\.html$', DiseaseListView.as_view(), name='disease_list'),
    url(r'^tra-cuu-theo-bai-thuoc\.html$', DrugListView.as_view(), name='drug_list'),

    url(r'^chuyen-gia-duoc-lieu\.html$', ExpertView.as_view(), name='expert'),
    url(r'^ban-tin-duoc-lieu\.html$', NewsView.as_view(), name='news'),
    url(r'^thong-tin-khoa-hoc\.html$', InfoView.as_view(), name='info'),


    url(r'^bai-viet-(?P<slug>[\w-]+)\.html$', PostDetailView.as_view(), name='post_detail'),

    url(r'^duoc-lieu-(?P<slug>[\w-]+)\.html$', MedicineDetailView.as_view(), name='medicine_detail'),
    url(r'^danh-luc-(?P<slug>[\w-]+)\.html$', SpecialDetailView.as_view(), name='special_detail'),

    url(r'^benh-(?P<slug>[\w-]+)\.html$', DiseaseDetailView.as_view(), name='disease_detail'),
    url(r'^bai-thuoc-(?P<slug>[\w-]+)\.html$', DrugDetailView.as_view(), name='drug_detail'),


    url(r'^tu-khoa-(?P<slug>[\w-]+)\.html$', TagView.as_view(), name='tag'),
    url(r'^tim-kiem\.html$', SearchView.as_view(), name='search'),
    url(r'^api/(?P<content>[\w-]+)$', tasks_json, name='api'),
]