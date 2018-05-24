from django.db import models
from django.utils.timezone import now

class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=60)

class NewsFeed(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.CharField(max_length=1000)
    time = models.DateTimeField(default=now)

class Comments(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    newsfeed = models.ForeignKey(NewsFeed, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)
    time = models.DateTimeField(auto_now_add=True)

class Likes(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    newsfeed = models.ForeignKey(NewsFeed, on_delete=models.CASCADE)
    has_liked = models.BooleanField(default=False)

class Messages(models.Model):
    sender = models.ForeignKey(UserInfo, related_name='message_sender', blank=True, null=True, on_delete=models.SET_NULL)
    receiver = models.ForeignKey(UserInfo, related_name='message_receiver', blank=True, null=True, on_delete=models.SET_NULL)
    text = models.CharField(max_length=250)
    time = models.DateTimeField(auto_now_add=True)

class Notifications(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    content = models.CharField(max_length=250)


'''
'>> python manage.py migrate newsfeed --fake
'''