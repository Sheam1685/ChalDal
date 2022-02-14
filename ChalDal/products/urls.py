from django.urls import path
from products import views

urlpatterns = [
    path('add_prod/', views.returnAddProduct, name='add_prod'),
    
    path('category/<str:cat_pk>/', views.returnProductCat, name='category'),
]