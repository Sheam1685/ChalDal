from django.urls import path
from registration import views

urlpatterns = [
    path('signup/', views.returnSignUp),
]