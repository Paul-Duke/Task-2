from django.urls import path

from . import views


app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>/", views.entry, name='entry'),
    path("search/", views.search, name='search'),
    path("random/", views.random, name='random'),
    path("new_entry/", views.new_entry, name='new_entry'),
    path("wiki/<str:entryHead>/edit/", views.edit_page, name='edit_page')
]
