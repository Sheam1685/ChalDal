from django.urls import path
from registration import views

urlpatterns = [
    path('signup/', views.returnSignUp, name='signup'),
    path('seller_signup/', views.returnSellerSignUp, name='seller_signup'),
    path('cus_login/', views.returnLogin, name='cus_login'),
    path('logout/', views.returnLogout, name='logout'),
    path('cus_home/', views.returnCustomerHome, name='cus_home'),
    path('custlist/', views.returnCustomerList, name="custlist"),
    
]