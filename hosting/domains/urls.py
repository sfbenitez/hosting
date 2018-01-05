# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path
from domains import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),
    path('newdomain', views._new_domain),
]
