from ckeditor_uploader.widgets import CKEditorUploadingWidget
from dal import autocomplete

from django import forms
from core.models import *
from project import settings


class PostForm(autocomplete.FutureModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': CKEditorUploadingWidget(),
            'thanhphan': CKEditorUploadingWidget(),
            'dangbaoche': CKEditorUploadingWidget(),
            'chidinh': CKEditorUploadingWidget(),
            'lieudung': CKEditorUploadingWidget(),
            'tags': autocomplete.TaggitSelect2(url='core:tag_autocomplete'),
            'disease': autocomplete.ModelSelect2Multiple(url='core:disease_autocomplete'),
        }
        labels = settings.LABELS

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'content': CKEditorUploadingWidget(),
        }
        labels = settings.LABELS
