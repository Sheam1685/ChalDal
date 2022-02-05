from operator import truediv
from django.shortcuts import render

# Create your views here.

def returnHomepage(request):
    isLoggedIn=False
    acType=""
    if request.session.has_key('cus_email'):
        isLoggedIn=True
        acType="customer"
    if request.session.has_key('seller_email'):
        isLoggedIn=True
        acType="seller"
    return render(request, 'homeApp/home_page.html', context={'isLoggedIn':isLoggedIn, 'acType':acType})
