from django import forms
from django.contrib import admin
from django.db import models
from indexpage.models import Section, SubSection


class SectionAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(attrs={'class': 'ckeditor'})
        },
    }

    class Media:
        css = {"all": ("admin_style.css",)}
        js = ('//cdn.ckeditor.com/4.4.7/standard/ckeditor.js',)


class SubSectionAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(attrs={'class': 'ckeditor'})
        },
    }

    class Media:
        css = {"all": ("admin_style.css",)}
        js = ('//cdn.ckeditor.com/4.4.7/standard/ckeditor.js',)

admin.site.register(Section, SectionAdmin)
admin.site.register(SubSection, SubSectionAdmin)
