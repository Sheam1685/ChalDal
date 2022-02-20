from django.urls import path
from products import views

urlpatterns = [
    path('add_prod/', views.returnAddProduct, name='add_prod'),
    path('category/<str:cat_pk>/', views.returnProductCat, name='category'),
    path('product_details/<str:prod_pk>/', views.returnProductDetails, name='product_details'),
    path('add_offer/', views.returnAddOffer, name = 'add_offer'),
    path('checkout/<str:prod_pk>/', views.returnCheckOut, name = 'checkout'),
]