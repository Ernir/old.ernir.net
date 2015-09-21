from django.conf.urls import patterns, url
from vanciantopsionics import views

urlpatterns = patterns(
    '',
    url(r"^$", views.vtp_index, name="vtp_index"),
    url(r"^chapter/(?P<chapter_number>\d)/$", views.vtp_chapter, name="vtp_chapter"),
    url(r"^spell/(?P<spell_slug>.*?)/$", views.vtp_spell, name="vtp_spell"),
    url(r"^spells/$", views.vtp_spell_index, name="vtp_spell_index")
)