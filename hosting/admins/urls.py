# -*- coding: utf-8 -*-

from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path
from admins import views
from users import admins

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('dashboard', views.index),
    path('appusers/', admins.views.appusers),
    path('newuser/', admins.views._adduser, name = 'add_user'),
    path('deluser/', admins.views._deluser, name = 'del_user'),
    # path('domains/', include('domains.urls')),
    # path('dbmanager/', include('dbmanager.urls')),
    # path('stats', views.stats),
    # path('users',  include(users.urls),
]
