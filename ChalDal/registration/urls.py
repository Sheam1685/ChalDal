from django.urls import path
from registration import views

urlpatterns = [
    path('signup/', views.returnSignUp, name='signup'),
    path('seller_signup/', views.returnSellerSignUp, name='seller_signup'),
    path('cus_login/', views.returnLogin, name='cus_login'),
    path('seller_login/', views.returnSellerLogin, name='seller_login'),
    path('employee_login/', views.returnEmployeeLogin, name='employee_login'),
    path('logout/', views.returnLogout, name='logout'),
    path('cus_home/', views.returnCustomerHome, name='cus_home'),
    path('seller_home/', views.returnSellerHome, name='seller_home'),
    path('admin_home/', views.returnAdminHome, name='admin_home'),
    path('hire_cus_care/', views.returnHireCusCare, name='hire_cus_care'),
    path('hire_deliveryguy/', views.returnHireDeliveryGuy, name='hire_deliveryguy'),
    path('cus_care_home/', views.returnCusCareHome, name='cus_care_home'), 
    path('cus_care_reviews/', views.returnCusCarePendingReviews, name='cus_care_reviews'), 
    path('cus_care_past_review/', views.returnCusCarePastReview, name='cus_care_past_review'),
    path('delivery_pending/', views.returnDeliveryPending, name='delivery_pending'),
    path('delivery_guy_home/', views.returnDeliveryHome, name='delivery_guy_home'),
    path('delivery_home_past/', views.returnDeliveryHomePast, name='delivery_home_past'),
    path('seller_products/', views.returnSellerProducts, name='seller_products'),
    path('custlist/', views.returnCustomerList, name="custlist"),
    path('cus_order/', views.returnCusorder, name = 'cus_order'),
    path('cus_review/', views.returnCusReview, name = 'cus_review'),
    path('seller_offers/', views.returnSellerOffers, name = 'seller_offers'),
]