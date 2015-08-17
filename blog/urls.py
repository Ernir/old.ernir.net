from django.conf.urls import patterns, url
from blog import views

urlpatterns = \
    patterns(
        '',
        # Actual pages
        url(r"^$", views.index, name="index")
    )
