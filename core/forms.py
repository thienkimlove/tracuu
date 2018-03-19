from ckeditor_uploader.widgets import CKEditorUploadingWidget
from dal import autocomplete
from django import forms
from django.forms import Textarea

from core.models import *

class PostForm(autocomplete.FutureModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': CKEditorUploadingWidget(),
            'tags': autocomplete.TaggitSelect2(url='core:tag_autocomplete'),
        }


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        widgets = {
            'content': CKEditorUploadingWidget(),
            'tags': autocomplete.TaggitSelect2(url='core:tag_autocomplete'),
        }
        fields = ('name', 's_name', 'other_name', 'last_name', 'desc', 'seo_name', 'seo_desc', 'status' , 'image', 'galery_image1', 'galery_image2', 'galery_image3', 'content', 'disease', 'tags')

class SpecialForm(forms.ModelForm):
    class Meta:
        model = Special
        widgets = {
            'content': CKEditorUploadingWidget(),
            'tags': autocomplete.TaggitSelect2(url='core:tag_autocomplete'),
        }
        fields = ('name', 's_name', 'other_name', 'last_name', 'desc', 'seo_name', 'seo_desc', 'status' , 'image', 'galery_image1', 'galery_image2', 'galery_image3', 'content', 'disease', 'tags')

class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = '__all__'
        widgets = {
            'content': CKEditorUploadingWidget(),
            'tags': autocomplete.TaggitSelect2(url='core:tag_autocomplete'),
        }


class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = '__all__'
        widgets = {
            'content': CKEditorUploadingWidget(),
            'thanhphan': CKEditorUploadingWidget(),
            'dangbaoche': CKEditorUploadingWidget(),
            'chidinh': CKEditorUploadingWidget(),
            'lieudung': CKEditorUploadingWidget(),
            'tags': autocomplete.TaggitSelect2(url='core:tag_autocomplete'),
        }
