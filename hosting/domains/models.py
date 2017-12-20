from django.db import models
from django.utils import timezone
from users.models import Users

class domains(models.Model):
    domain_name = models.CharField(max_length=200)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
