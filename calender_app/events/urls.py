from unicodedata import name
from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name="home"),
    path('events', views.all_events, name="list-events"),
    path('add_venue', views.add_venue, name="add_venue"),
    path('list_venues', views.list_venues, name="list_venues"),
    path('show_venue/<venue_id>', views.show_venue, name="show_venue"),
    path('search_venues', views.search_venues, name="search_venues"),
    path('update_venue/<venue_id>', views.update_venue, name="update_venue"),
]