# Generated by Django 2.0 on 2017-12-27 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0003_auto_20171226_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrelations',
            name='bd_user',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='userrelations',
            name='ftp_user',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]