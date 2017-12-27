# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),
    path('newuser', views.new_db_user),
    path('newdb', views.new_db),
    path('deldb', views.del_db),
    path('bdlist', views.db_list),
]
