from django.urls import path
from homeApp import views

urlpatterns = [
    path('', views.returnHomepage, name='home'),
]