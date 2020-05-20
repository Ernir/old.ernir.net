from django.conf.urls import url
from vanciantopsionics import views

urlpatterns = [
    url(r"^$", views.vtp_index, name="vtp_index"),
    url(r"^chapter/(?P<chapter_number>\d+?)/$", views.vtp_chapter, name="vtp_chapter"),
    url(r"^spell/(?P<spell_slug>.*?)/$", views.vtp_spell, name="vtp_spell"),
    url(r"^class/(?P<class_slug>.*?)/$", views.vtp_class, name="vtp_class"),
    url(r"^spells/$", views.vtp_spell_index, name="vtp_spell_index"),
    url(r"^classes/$", views.vtp_class_index, name="vtp_class_index"),
]
