from django.db import models

class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=60)

class NewsFeed(models.Model):
    title = models.CharField(max_length=250)
    content = models.CharField(max_length=1000)
