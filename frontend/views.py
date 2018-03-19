from django.core import serializers
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from taggit.models import Tag

from core.models import *
from django.apps import apps

from project import settings


def tasks_json(request, content):
    data = []
    if content == 'medicine':
        data = Medicine.objects.filter(status=True).order_by('name')
    if content == 'special_medicine':
        data = Special.objects.filter(status=True).order_by('name')
    if content == 'tag':
        data = Tag.objects.all()
        if request.GET.get('search_value'):
            data = data.filter(name__istartswith=request.GET.get('search_value'))
    data = serializers.serialize('json', list(data), fields=('name','slug'))
    return HttpResponse(data, content_type='application/json')

def detail_view(request, slug):

    for name in ['Medicine', 'Special', 'Post', 'Drug', 'Disease']:
        model_object = apps.get_model(app_label='core', model_name=name)
        if model_object.objects.filter(slug=slug).exists():
            content = model_object.objects.filter(slug=slug).first()
            model_object.objects.filter(pk=content.id).update(views=F('views') + 1)
            #handle1=open(settings.LOG_FILE,'r+')
            #handle1.write(str(content.id))
            #handle1.close()
            related_objects = content.tags.similar_objects()[0:2]
            if name=='Post':
                if not related_objects:
                    related_objects = model_object.objects.filter(status=True).filter(~Q(id = content.id)).order_by("-created_at")[0:2]
                latest_objects = model_object.objects.filter(status=True).filter(~Q(id = content.id)).order_by("-created_at")[0:3]
                return render(request, 'frontend/post_detail.html', { 'content' : content, 'related_objects' : related_objects, 'latest_objects' : latest_objects })

            if name=='Drug':
                if not related_objects:
                    related_objects = model_object.objects.filter(status=True).filter(~Q(id = content.id)).order_by("-created_at")[0:2]

                return render(request, 'frontend/drug_detail.html', { 'content' : content, 'related_objects' : related_objects })
            if name=='Disease':
                medicines = Medicine.objects.filter(disease=content).order_by("-created_at")[0:5]
                return render(request, 'frontend/disease_detail.html', { 'content' : content, 'medicines' : medicines })

            if name=='Special':
                if not related_objects:
                    related_objects = model_object.objects.filter(status=True).filter(~Q(id = content.id)).order_by("-created_at")[0:2]
                return render(request, 'frontend/special_detail.html', { 'content' : content, 'related_objects' : related_objects,  })

            if name=='Medicine':
                if not related_objects:
                    related_objects = model_object.objects.filter(status=True).filter(~Q(id = content.id)).order_by("-created_at")[0:2]

                return render(request, 'frontend/medicine_detail.html', { 'content' : content, 'related_objects' : related_objects, })

