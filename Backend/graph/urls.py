from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("see_nodes/", views.see_nodes, name="see_nodes"),
    path('', views.index, name='index'),  # This will render 'index.html' at the root URL
    path("", include("myapp.urls")),  # Include URLs from myapp
    path("", views.index, name="index"),  # Catch-all route should be last
]