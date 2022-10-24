from django.urls import path
from . import views


urlpatterns = [
    path('', views.flight_search, name='flight_search'),
]
