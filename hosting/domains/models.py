# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from hosting.models import Users

class domains(models.Model):
    domain_name = models.CharField(max_length=200)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
