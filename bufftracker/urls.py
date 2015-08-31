from django.conf.urls import patterns, url
from bufftracker import views

urlpatterns = patterns(
    '',
    url(r"^$", views.index, name="index"),
    url(r"^behind-the-scenes/statistics/$", views.get_statistics, name="stats"),
    url(r"^behind-the-scenes/bonuses/$", views.calculate_bonuses,
        name="bonuses"),
)
