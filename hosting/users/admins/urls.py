# -*- coding: utf-8 -*-

from django.conf.urls import url,include
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('dashboard', views.index),
    path('appusers/', views.appusers),
    path('newuser/', views._adduser, name = 'add_user'),
    path('deluser/', views._deluser, name = 'del_user'),
    # path('domains/', include('domains.urls')),
    # path('dbmanager/', include('dbmanager.urls')),
    # path('stats', views.stats),
    # path('users',  include(users.urls),
]
