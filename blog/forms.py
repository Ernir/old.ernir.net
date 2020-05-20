from django import forms
from django.template.defaultfilters import mark_safe


class CommentForm(forms.Form):

    content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))
