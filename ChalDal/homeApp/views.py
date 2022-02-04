from django.shortcuts import render

# Create your views here.
def returnHomepage(request):
    isLoggedIn=False
    if request.session.has_key('cus_email'):
        isLoggedIn=True
    return render(request, 'homeApp/home_page.html', context={'isLoggedIn':isLoggedIn})
