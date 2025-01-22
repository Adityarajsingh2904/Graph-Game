from django import forms
from django.core import validators
from myapp.models import Node


class FormName(forms.ModelForm):
    class Meta:
        model = Node
        fields = "__all__"