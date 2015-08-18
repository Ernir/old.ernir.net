from django.contrib import admin
from blog.models import Entry, Comment, Tag

admin.site.register(Comment)


class EntryAdmin(admin.ModelAdmin):
    exclude = ("slug", )  # these are auto-generated


class TagAdmin(admin.ModelAdmin):
    exclude = ("slug", )

admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag, TagAdmin)