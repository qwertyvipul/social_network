from django.contrib import admin
from .models import *

admin.site.register(UserInfo)
admin.site.register(NewsFeed)
admin.site.register(Comments)
admin.site.register(Likes)
admin.site.register(Messages)
admin.site.register(Notifications)
