from django.contrib.auth import authenticate, login, logout, models
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'auth/login.html', {'message': None})

    context = {
        'user': request.user
    }
    return render(request, 'orders/index.html', context)

def login_view(request):
    if request.method == 'GET':
        return render(request, 'auth/login.html', {'message': None})

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is None:
        return render(request, 'auth/login.html', {'message': 'Invalid credentials.'})

    login(request, user)
    return HttpResponseRedirect(reverse('index'))

def logout_view(request):
    logout(request)
    return render(request, 'auth/login.html', {'message': 'Logged out.'})

def signup_view(request):
    if request.method == 'GET':
        return render(request, 'auth/signup.html', {'message': None})

    username = request.POST['username']
    email    = request.POST['email']
    password = request.POST['password']

    try:
        user = models.User.objects.create_user(username, email, password)
    except IntegrityError:
        return render(request, 'auth/signup.html', {'message': 'Username taken.'})

    login(request, user)
    return HttpResponseRedirect(reverse('index'))
