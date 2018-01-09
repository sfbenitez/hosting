# -*- coding: utf-8 -*-

from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path
from admins import views
from users import admins

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),

]
