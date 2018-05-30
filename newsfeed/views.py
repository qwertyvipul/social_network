from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.shortcuts import redirect


def index(request):
    return redirect('newsfeed:newsfeed')

def newsfeed(request):
    if request.session.has_key('user_id') and request.session['user_id']!=0:
        id = request.session['user_id']
    else:
        return redirect('newsfeed:login')
    query = UserInfo.objects.filter(id=id)
    for user in query:
        break
    all_posts = NewsFeed.objects.all().order_by('time').reverse()

    form = StatusForm()
    context = {
        'user': user,
        'all_posts': all_posts,
        'statusForm': form,
    }
    return render(request, 'newsfeed/index.html', context)
    #return HttpResponse('<h1>You are viewing newsfeed</h1>')

def messages(request):
    if request.session.has_key('user_id') and request.session['user_id']!=0:
        id = request.session['user_id']
    else:
        return redirect('newsfeed:login')

    query = UserInfo.objects.filter(id=id)
    for user in query:
        name = user.name

    all_messages = Messages.objects.all()
    context = {
        'name': name,
        'all_messages':all_messages,
    }
    return render(request, 'newsfeed/messages.html', context)

def notifcations(request):
    if request.session.has_key('user_id') and request.session['user_id']!=0:
        id = request.session['user_id']
    else:
        return redirect('newsfeed:login')

    query = UserInfo.objects.filter(id=id)
    for user in query:
        name = user.name
    context = {
        'name': name,
    }
    return render(request, 'newsfeed/notifications.html', context)

def register(request):
    if request.method == 'POST':
        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            user = UserInfo()
            user.name = registerForm.cleaned_data['name']
            user.username = registerForm.cleaned_data['username']
            # You may not want to store plain text password in your database
            # This is just for testing purpose in real life it is not safe
            # You miss they hit!
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

                request.session['user_id'] = id
                return redirect('newsfeed:newsfeed')

    form = LoginForm()
    return render(request, 'newsfeed/login.html', context={'form':form})

def logout(request):
    request.session['user_id']=0
    return redirect('newsfeed:login')

def postStatus(request):
    if request.session.has_key('user_id') and request.session['user_id']!=0:
        id = request.session['user_id']
    else:
        return redirect('newsfeed:login')

    if request.method == "POST":
        statusForm = StatusForm(request.POST)
        if statusForm.is_valid():
            status = NewsFeed()
            query = UserInfo.objects.filter(id=id)
            for user in query:
                status.user = user
                break
            status.title = statusForm.cleaned_data['title']
            status.content = statusForm.cleaned_data['content']
            status.save()

    return redirect('newsfeed:newsfeed')


def uploadPhoto(request):
    pass

def likeStatus(request, status_id):
    if request.session.has_key('user_id') and request.session['user_id']!=0:
        id = request.session['user_id']
    else:
        return redirect('newsfeed:login')

    query = UserInfo.objects.filter(id=id)
    for user in query:
        break

    query = NewsFeed.objects.filter(id=status_id)
    for status in query:
        break

    query = Likes.objects.filter(user=user)
    query = query.filter(newsfeed=status)
    if query.count()>0:
        for like in query:
            if like.has_liked:
                return HttpResponse('<h3>This is post has already been liked by you.</h3>')
            else:
                like.has_liked = True
                return redirect('newsfeed:newsfeed')
    like = Likes()
    like.user = user
    like.newsfeed = status
    like.has_liked = True
    like.save()

    return redirect('newsfeed:newsfeed')

def unlikeStatus(request):
    pass

def profile(request):
    if request.session.has_key('user_id') and request.session['user_id']!=0:
        id = request.session['user_id']
    else:
        return redirect('newsfeed:login')
    query = UserInfo.objects.filter(id=id)
    for user in query:
        break

    query = ProfilePictures.objects.filter(user = user)
    profilePicForm = ProfilePicForm()
    context = {
        'user': user,
        'profilePicForm': profilePicForm,
        'query': query,
    }
    return render(request, 'newsfeed/profile.html', context)

def uploadProfilePic(request):
    if request.session.has_key('user_id') and request.session['user_id']!=0:
        id = request.session['user_id']
    else:
        return redirect('newsfeed:login')

    if request.method == "POST":
        profilePicForm = ProfilePicForm(request.POST, request.FILES)
        if profilePicForm.is_valid():
            profilePic = ProfilePictures()
            query = UserInfo.objects.filter(id=id)
            for user in query:
                profilePic.user = user
                break
            profilePic.profile_pic = profilePicForm.cleaned_data['profile_pic']
            profilePic.save()
            return redirect('newsfeed:profile')
        else:
            print(profilePicForm.errors)
            return HttpResponse(profilePicForm.errors)

    return HttpResponse("<h1>Return</h1>")
    return redirect('newsfeed:profile')