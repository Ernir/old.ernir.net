from django.contrib import admin
from blog.models import Entry, Comment, Tag
from django.db import models
from django import forms

admin.site.register(Comment)


class EntryAdmin(admin.ModelAdmin):
    exclude = ("slug", )  # these are auto-generated
    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(attrs={'class': 'ckeditor'})
        },
    }

    class Media:
        css = {"all": ("admin_style.css",)}
        js = ('//cdn.ckeditor.com/4.4.7/standard/ckeditor.js',)


class TagAdmin(admin.ModelAdmin):
    exclude = ("slug", )

admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag, TagAdmin)