"""FTPClient URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from . import userviews

urlpatterns = [
    path('', userviews.index, name='index'),
    url(r'^directory(?P<path>.+)$', userviews.dir_details, name='dir_details'),
    path('newuser', userviews.new_ftp_user),
    path('upload', userviews.upload_file, name='upload'),
    path('delete', userviews.delete_file, name='delete_file'),
    path('mkremdir', userviews.make_rem_dir, name='mkremdir'),
]
