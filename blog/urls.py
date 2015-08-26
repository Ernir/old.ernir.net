from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns(
    '',
    url(r"^$", views.index, name="index"),
    url(r"^(?P<language_filter>.+)/$", views.index, name="filtered_index"),
    url(r"^tag/(?P<tag_slug>.+)/$", views.by_tag, name="by_tag"),
    url(r"^entry/(?P<blog_slug>\w+)/$", views.entry, name="entry"),
)