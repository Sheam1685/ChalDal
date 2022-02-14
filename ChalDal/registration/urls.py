from django.urls import path
from registration import views

urlpatterns = [
    path('signup/', views.returnSignUp, name='signup'),
    path('seller_signup/', views.returnSellerSignUp, name='seller_signup'),
    path('cus_login/', views.returnLogin, name='cus_login'),
    path('seller_login/', views.returnSellerLogin, name='seller_login'),
    path('logout/', views.returnLogout, name='logout'),
    path('cus_home/', views.returnCustomerHome, name='cus_home'),
    path('seller_home/', views.returnSellerHome, name='seller_home'),
    path('seller_products/', views.returnSellerProducts, name='seller_products'),
    path('custlist/', views.returnCustomerList, name="custlist"),
    path('cus_order/', views.returnCusorder, name = 'cus_order'),
    path('cus_review/', views.returnCusReview, name = 'cus_review'),
    path('seller_offers/', views.returnSellerOffers, name = 'seller_offers'),
]