from django.urls import path
from .import views

app_name = 'newsfeed'

urlpatterns = [
    path('', views.index, name='index'),
    path('newsfeed/', views.newsfeed, name='newsfeed'),
    path('messages/', views.messages, name='messages'),
    path('notifications/', views.notifcations, name='notifications'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('status-update/', views.postStatus, name='postStatus'),
    path('upload-photo/', views.uploadPhoto, name='uploadPhoto'),
]