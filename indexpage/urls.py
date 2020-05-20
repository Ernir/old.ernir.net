from django.conf.urls import url
from indexpage import views

urlpatterns = [
    url(r"^$", views.main_index, name="main_index"),
]
