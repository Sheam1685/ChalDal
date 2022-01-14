from django.urls import path
from registration import views

urlpatterns = [
    path('signup/', views.returnSignUp, name="signup"),
    path('custlist/', views.returnCustomerList, name="custlist"),
]