from django.urls import path  # Import path instead of url
from . import views  # Ensure you import your views

urlpatterns = [
    path("formpage/", views.form_name_view, name="form_name_view"),
    path("reactdata/", views.collect_from_react, name="collect_from_react"),
    path("bollymovies/", views.bollymovies, name="bollymovies"),
    path("mutuals/", views.collect_mutuals, name="collect_mutuals"),
    path("collect-all/", views.collect_all, name="collect_all"),
    path("collect-bolly/", views.collect_bolly, name="collect_bolly"),
    path("adduser/", views.adduser, name="adduser"),
    path("nametolink/", views.collect_node_given_name, name="nametolink"),
    path("friendrecs/", views.friendrecs, name="friendrecs"),
]
