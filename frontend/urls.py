from django.conf.urls import url
from django.db.models import Q

from django.views.generic import TemplateView
from taggit.models import Tag

from core.models import *
from frontend.views import tasks_json, detail_view, category_view, quan_api

import logging

# Standard instance of a logger with __name__
from project.settings import LOG_FILE

stdlogger = logging.getLogger(__name__)

app_name = "frontend"

def debug(msg):
    with open(LOG_FILE, 'r') as original: data = original.read()
    with open(LOG_FILE, 'w') as modified: modified.write(data +str(repr(msg))+"\n")

class IndexView(TemplateView):
    template_name="frontend/index.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['most_search'] = Post.objects.filter(status=True).filter(category__template='medicine').order_by('-views')[0:12]
        context['experts'] = Expert.objects.filter(status=True)[0:3]
        return context

class TagView(TemplateView):

    template_name='frontend/tag.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        slug = self.kwargs['slug']
        tag = Tag.objects.get(slug__exact=slug)

        posts = Post.objects.filter(Q(status=True) & Q(tags=tag)).order_by("-created_at")[0:12]
        context['posts'] = posts
        context['tag'] = tag
        return context

class SearchView(TemplateView):
    template_name='frontend/search.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        search_value = self.request.GET.get('search_value')
        posts = Post.objects.filter(status=True).filter(Q(name__icontains=search_value) | Q(tags__name__icontains=search_value)).distinct()[0:12]
        #debug(posts.query.__str__())
        context['posts'] = posts

        return context



urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),

    url('^browser$', quan_api, name='quan_api'),
    url(r'^tu-khoa-(?P<slug>[\w-]+)$', TagView.as_view(), name='tag'),
    url(r'^tim-kiem$', SearchView.as_view(), name='search'),
    url(r'^api/(?P<content>[\w-]+)$', tasks_json, name='api'),
    url(r'^(?P<slug>[\w-]+)\.html$', detail_view, name='content_detail'),
    url(r'^(?P<slug>[\w-]+)$', category_view, name='category'),
]