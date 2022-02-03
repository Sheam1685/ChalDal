from django.urls import path
from registration import views

urlpatterns = [
    path('signup/', views.returnSignUp, name="signup"),
    path('seller_signup/', views.returnSellerSignUp, name="seller_signup"),
    path('cus_login/', views.returnLogin, name="cus_login"),
    path('custlist/', views.returnCustomerList, name="custlist"),
    
]