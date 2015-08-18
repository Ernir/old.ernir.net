from django.conf.urls import patterns, url
from vanciantopsionics import views

urlpatterns = patterns(
    '',
    url(r"^$", views.vtp_index, name="vtp_index"),
)