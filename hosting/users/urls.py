# -*- coding: utf-8 -*-

from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('dashboard', views.index),
    path('filemanager/', include('ftpclient.urls')),
    path('domains/', include('domains.urls')),
    path('databases/', include('dbmanager.urls')),
    path('stats', views.stats),
    # path('users',  include(users.urls),
]
