from django.db import models
from django.utils import timezone

# Tabla Users:
#   user
#   pg_password
#   ftp_password
#   fecha_alta
#   rol_id
#
# Tabla roles:
#   rol_id
#   description
#
# Tabla dominios:
#   domain_name
#   user

class Users(models.Model):
    user = models.CharField(max_length=20)
    pg_password = models.CharField(max_length=50)
    ftp_password = models.CharField(max_length=50)
    rol_id = models.IntegerField(max_length=2, default=1)
    fecha_alta = models.DateTimeField(default=timezone.now)

class roles(models.Model):
    rol_id = models.IntegerField(max_length=2)
    description = models.CharField(max_length=200)

class domains(models.Model):
    domain_name = models.CharField(max_length=200)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
