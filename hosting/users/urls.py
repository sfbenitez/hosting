# -*- coding: utf-8 -*-

from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('dashboard', views.index),
    path('filemanager', views.filemanager),
    path('domains/', include('domains.urls')),
    path('databases', views.databases),
    path('stats', views.stats),
    # path('users',  include(users.urls),
]
