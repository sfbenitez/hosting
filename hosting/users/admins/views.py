# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import repository

@login_required
def appusers(request):
    tittle='App User Management'
    sidebaractive='active'
    topmenu='current'
    context = {
        'tittle' : tittle,
        'activeappusers' : sidebaractive,
        'currenttopmenu' : topmenu
    }
    user_repository = repository.UsersRepository()
    common_users, premium_users = user_repository.get_users()
    context['common_users'] = common_users
    context['premium_users'] = premium_users

    return render(request, 'admin/appusers.html', context)
