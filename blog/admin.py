from django.contrib import admin
from blog.models import Entry, Comment

admin.site.register(Comment)


class EntryAdmin(admin.ModelAdmin):
    exclude = ("slug", "excerpt", "tags")  # these are auto-generated


admin.site.register(Entry, EntryAdmin)