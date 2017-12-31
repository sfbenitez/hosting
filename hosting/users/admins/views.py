# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
    return render(request, 'admin/appusers.html', context)
