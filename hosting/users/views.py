# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from users.admins.repository import get_users_avatar
from users.admins.ftprepository import get_ftp_user_for_app_user
from users.admins.dbrepository import get_db_user_for_app_user
@login_required
def index(request):
    tittle='Dashboard'
    sidebaractive='active'
    topmenu='current'
    context = {
        'tittle' : tittle,
        'activedashboard' : sidebaractive,
    }
    return render(request, 'index.html', context)

@login_required
def user_profile(request):
    tittle='Dashboard'
    sidebaractive='active'
    topmenu='current'
    context = {
        'tittle' : tittle,
        'activedashboard' : sidebaractive,
    }
    context['avatar_url'] = get_users_avatar(request.user.email)
    context['ftp_user'] = get_ftp_user_for_app_user(request.user.username)
    context['db_user'] = get_db_user_for_app_user(request.user.username)
    return render(request, 'profile.html', context)

@login_required
def stats(request):
    tittle='Web Statistics'
    sidebaractive='active'
    topmenu='current'
    context = {
        'tittle' : tittle,
        'activestats' : sidebaractive,
        'currenttopmenu' : topmenu,
    }
    app_user = request.user.username
    listadom = repository.get_users_domains(app_user)
    context['domain'] = 'www.' + listadom[0]
    return render(request, 'stats.html', context)
