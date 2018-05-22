from django.shortcuts import render
from django.http import HttpResponse
from .models import NewsFeed, UserInfo
from .forms import *
from django.urls import reverse_lazy
from django.shortcuts import redirect

def index(request):
    pass

def newsfeed(request):
    if request.session.has_key('id') and request.session['id']!=0:
        id = request.session['id']
    else:
        return redirect('newsfeed:login')
    query = UserInfo.objects.filter(id=id)
    for user in query:
        name = user.name
    all_post = NewsFeed.objects.all()
    context = {
        'name': name,
        'all_post': all_post,
    }
    return render(request, 'newsfeed/index.html', context)
    #return HttpResponse('<h1>You are viewing newsfeed</h1>')

def messages(request):
    pass

def notifcations(request):
    pass

def register(request):
    if request.method == 'POST':
        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            user = UserInfo()
            user.name = registerForm.cleaned_data['name']
            user.username = registerForm.cleaned_data['username']
            user.password = registerForm.cleaned_data['password']
            user.save()
            return redirect('newsfeed:login')
    else:
        form = RegisterForm()
        return render(request, 'newsfeed/register.html', context={'form':form})

def login(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            query = UserInfo.objects.filter(username=loginForm.cleaned_data['username'])
            query = query.filter(password=loginForm.cleaned_data['password'])
            total = query.count()
            if total==1:
                id = 0
                for result in query:
                    id = result.id

                request.session['id'] = id
                return redirect('newsfeed:newsfeed')

    form = LoginForm()
    return render(request, 'newsfeed/login.html', context={'form':form})

def logout(request):
    request.session['id']=0
    return redirect('newsfeed:login')