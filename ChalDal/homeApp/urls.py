from django.urls import path
from homeApp import views

urlpatterns = [
    path('', views.returnHomepage, name='home'),
    path('productSearch/<str:searchT>/', views.searchProduct, name='productSearch'),
    path('offers/',views.returnOffers,name='offers'),
]