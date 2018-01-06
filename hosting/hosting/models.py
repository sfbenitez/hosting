# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone


class appuserdomains(models.Model):
    app_user = models.CharField(max_length=50)
    domain_name = models.CharField(max_length=200, primary_key=True)

class appusersubdomains(models.Model):
    domain_name = models.ForeignKey(appuserdomains,
        on_delete=models.CASCADE)
    subdomain_name = models.CharField(max_length=200, primary_key=True)
    path = models.CharField(max_length=200, default='/')

class AppUserDbUserRelation(models.Model):
    app_user = models.CharField(max_length=50, unique=True, primary_key=True)
    db_user = models.CharField(max_length=50,unique=True)

class AppUserFtpUserRelation(models.Model):
    app_user = models.CharField(max_length=50, unique=True, primary_key=True)
    ftp_user = models.CharField(max_length=50,unique=True)
