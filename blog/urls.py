from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^(?P<language_filter>\w\w)/$", views.index, name="filtered_index"),
    url(r"^tag/(?P<tag_slug>.+)/$", views.by_tag, name="by_tag"),
    url(r"^entry/(?P<blog_slug>.+)/$", views.entry, name="entry"),
]
