from django.shortcuts import render

# Create your views here.
def returnHomepage(request):
    return render(request, 'homeApp/home_page.html')
