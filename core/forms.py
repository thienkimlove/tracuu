from ckeditor_uploader.widgets import CKEditorUploadingWidget
from dal import autocomplete

from django import forms
from core.models import *
from project import settings


class PostForm(autocomplete.FutureModelForm):
    disease = forms.ModelChoiceField(Post.objects.filter(category__slug__exact='tra-cuu-theo-benh'))
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
        }
        labels = settings.LABELS
