from urllib.parse import unquote, urlparse, parse_qs

import requests
import urllib3

from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from taggit.models import Tag
from core.models import *

def load(url):
    urllib3.disable_warnings()
    session = requests.session()
    session.max_redirects = 10
    session.verify = False
    session.timeout = (60, 30)

    url = unquote(url)
    o = urlparse(url)
    query = parse_qs(o.query, True)
    url_short = o._replace(query=None).geturl()
    query['limit']=10000
    if 'user' in query and 'pass' in query:
        g = session.get(url_short, params=query, auth=(query['user'][0], query['pass'][0]))
    else:
        g = session.get(url_short, params=query)
    return g.content.decode('utf-8').replace('\0', '')

def quan_api(request):
    data=[]
    if request.GET.get('site'):
        data = load(request.GET.get('site'))
    return HttpResponse(data, content_type='application/json')


def tasks_json(request, content):
    data = []
    if content == 'medicine':
        data = Post.objects.filter(status=True).filter(category__template='medicine').order_by('name')
    if content == 'special_medicine':
        data = Post.objects.filter(status=True).filter(category__template='special').order_by('name')
    if content == 'tag':
        data = Tag.objects.all()
        if request.GET.get('search_value'):
            data = data.filter(name__istartswith=request.GET.get('search_value'))
    data = serializers.serialize('json', list(data), fields=('name','slug'))
    return HttpResponse(data, content_type='application/json')

def detail_view(request, slug):
    if Post.objects.filter(slug=slug).exists():
        content = Post.objects.filter(slug=slug).first()
        Post.objects.filter(pk=content.id).update(views=F('views') + 1)
        related_objects = content.tags.similar_objects()[0:2]
        latest_objects = Post.objects.filter(status=True).filter(category=content.category).filter(~Q(id = content.id)).order_by("-created_at")[0:3]
        return render(request, 'frontend/'+content.category.template+'_detail.html', { 'content' : content, 'related_objects' : related_objects, 'latest_objects' : latest_objects })


def category_view(request, slug):
    category = Category.objects.filter(slug__exact=slug).first()
    if category:

        q = request.GET.get('q')

        if q is not None:
            posts = Post.objects.filter(Q(status=True) & Q(category=category)).filter(Q(name__istartswith=q) or Q(name__icontains=q)).order_by("-created_at")
        else:
            posts = Post.objects.filter(Q(status=True) & Q(category=category)).order_by("-created_at")

        if category.template != 'disease':
            paginator = Paginator(posts, 12)
            page = request.GET.get('page')
            posts = paginator.get_page(page)

        path = ''
        path += "%s" % "&".join(["%s=%s" % (key, value) for (key, value) in request.GET.items() if not key=='page' ])
        alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        experts = Expert.objects.filter(status=True)[0:3]
        videos = Video.objects.filter(status=True)[0:3]

        if category.is_static:
            template = 'frontend/static.html'
        else:
            template = 'frontend/'+category.template+'_list.html'
        return render(request, template, { 'category' : category, 'posts' : posts, 'path' : path, 'alphabets' : alphabets, 'experts' : experts, 'videos' : videos})