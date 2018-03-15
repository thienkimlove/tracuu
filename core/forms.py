from dal import autocomplete
from django import forms
from django.forms import Textarea

from core.models import *

class PostForm(autocomplete.FutureModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': Textarea(attrs={'rows': 20, 'class' : 'editor'}),
            'tags': autocomplete.TaggitSelect2(url='core:tag_autocomplete'),
        }

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'
        widgets = {
            'content': Textarea(attrs={'rows': 20, 'class' : 'editor'}),
            'tags': autocomplete.TaggitSelect2(url='core:tag_autocomplete'),
        }
        field_order = ('name', 's_name', 'other_name', 'last_name', 'desc', 'seo_name', 'seo_desc', 'status' , 'image', 'galery_image1', 'galery_image2', 'galery_image3', 'content', 'disease', 'tags')

class SpecialForm(forms.ModelForm):
    class Meta:
        model = Special
        fields = '__all__'
        widgets = {
            'content': Textarea(attrs={'rows': 20, 'class' : 'editor'}),
            'tags': autocomplete.TaggitSelect2(url='core:tag_autocomplete'),
        }

class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = '__all__'
        widgets = {
            'content': Textarea(attrs={'rows': 20, 'class' : 'editor'}),
            'tags': autocomplete.TaggitSelect2(url='core:tag_autocomplete'),
        }
        field_order = ('name', 's_name', 'desc', 'seo_name', 'seo_desc', 'status' , 'image', 'content', 'tags')


class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = '__all__'
        widgets = {
            'content': Textarea(attrs={'rows': 20, 'class' : 'editor'}),
            'thanhphan': Textarea(attrs={'rows': 20, 'class' : 'editor'}),
            'dangbaoche': Textarea(attrs={'rows': 20, 'class' : 'editor'}),
            'chidinh': Textarea(attrs={'rows': 20, 'class' : 'editor'}),
            'lieudung': Textarea(attrs={'rows': 20, 'class' : 'editor'}),
            'tags': autocomplete.TaggitSelect2(url='core:tag_autocomplete'),
        }
