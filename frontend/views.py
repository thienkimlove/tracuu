from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from core.models import *


def tasks_json(request, content):
    data = []
    if content == 'medicine':
        data = Medicine.objects.filter(status=True)
    if content == 'special_medicine':
        data = Special.objects.filter(status=True)
    data = serializers.serialize("json", data)
    return HttpResponse(data, content_type='application/json')
