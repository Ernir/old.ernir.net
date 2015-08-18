from django.conf.urls import patterns, url
from indexpage import views

urlpatterns = patterns(
    '',
    url(r"^$", views.main_index, name="main_index"),
)