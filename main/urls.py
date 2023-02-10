from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home page"),
    path("offer/<int:id>", views.base, name="base"),
    path("search_bar", views.search_bar, name="search_bar"),
    path("saved/<int:id>", views.saved, name="saved"),
]