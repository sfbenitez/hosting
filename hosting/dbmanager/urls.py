# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),
    path('newuser', views.new_db_user),
    path('access', views.db_list),
]
