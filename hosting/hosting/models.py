from __future__ import unicode_literals
from ldapdb.models.fields import (CharField, ImageField, ListField, IntegerField)
import ldapdb.models
from django.db import models
from django.utils import timezone

class roles(models.Model):
    rol_id = models.IntegerField()
    description = models.CharField(max_length=200)

class Users(models.Model):
    user = models.CharField(max_length=20)
    pg_password = models.CharField(max_length=50)
    ftp_password = models.CharField(max_length=50)
    rol_id = models.ForeignKey(roles, on_delete=models.CASCADE)
    fecha_alta = models.DateTimeField(default=timezone.now)

class AppUserDbUserRelation(models.Model):
    app_user = models.CharField(max_length=50, unique=True, primary_key=True)
    db_user = models.CharField(max_length=50,unique=True)

class AppUserFtpUserRelation(models.Model):
    app_user = models.CharField(max_length=50, unique=True, primary_key=True)
    ftp_user = models.CharField(max_length=50,unique=True)


## Ldap models



class LdapUser(ldapdb.models.Model):
    """
    Class for representing an LDAP user entry.
    """
    # LDAP meta-data
    base_dn = "ou=People,dc=sergio,dc=gonzalonazareno,dc=org"
    object_classes = ['posixAccount', 'shadowAccount', 'inetOrgPerson']

    # inetOrgPerson
    first_name = CharField(db_column='givenName', verbose_name="Prime name")
    last_name = CharField("Final name", db_column='sn')
    full_name = CharField(db_column='cn')
    email = CharField(db_column='mail')
    phone = CharField(db_column='telephoneNumber', blank=True)
    mobile_phone = CharField(db_column='mobile', blank=True)
    photo = ImageField(db_column='jpegPhoto')

    # posixAccount
    uid = IntegerField(db_column='uidNumber', unique=True)
    group = IntegerField(db_column='gidNumber')
    gecos = CharField(db_column='gecos')
    home_directory = CharField(db_column='homeDirectory', default='/srv/hosting/')
    login_shell = CharField(db_column='loginShell', default='/bin/bash')
    username = CharField(db_column='uid', primary_key=True)
    password = CharField(db_column='userPassword')

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.full_name

class LdapGroup(ldapdb.models.Model):
    """
    Class for representing an LDAP group entry.
    """
    # LDAP meta-data
    base_dn = "ou=Group,dc=sergio,dc=gonzalonazareno,dc=org"
    object_classes = ['posixGroup']

    # posixGroup attributes
    gid = IntegerField(db_column='gidNumber', unique=True)
    name = CharField(db_column='cn', max_length=200, primary_key=True)
    usernames = ListField(db_column='memberUid')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
