from django import forms
from django.forms import Textarea
from core.models import *


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': Textarea(attrs={'rows': 20, 'class' : 'editor'}),
        }

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'
        widgets = {
            'content': Textarea(attrs={'rows': 20, 'class' : 'editor'}),
        }

class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = '__all__'
        widgets = {
            'content': Textarea(attrs={'rows': 20, 'class' : 'editor'}),
        }

class ExpertForm(forms.ModelForm):
    class Meta:
        model = Expert
        fields = '__all__'
        widgets = {
            'content': Textarea(attrs={'rows': 20, 'class' : 'editor'}),
        }

class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = '__all__'
        widgets = {
            'thanhphan': Textarea(attrs={'rows': 20, 'class' : 'editor'}),
            'dangbaoche': Textarea(attrs={'rows': 20, 'class' : 'editor'}),
            'chidinh': Textarea(attrs={'rows': 20, 'class' : 'editor'}),
            'lieudung': Textarea(attrs={'rows': 20, 'class' : 'editor'}),
        }