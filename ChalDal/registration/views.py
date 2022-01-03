from django.shortcuts import render

# Create your views here.
def returnSignUp(request):
    return render(request, 'registration/signup.html')