# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
def filemanager(request):
    tittle='File Manager'
    sidebaractive='active'
    topmenu='current'
    context = {
        'tittle' : tittle,
        'activefilemanager' : sidebaractive,
        'currenttopmenu' : topmenu,
    }
    return render(request, 'filemanager.html', context)

@login_required
def databases(request):
    tittle='DB Manager'
    sidebaractive='active'
    topmenu='current'
    context = {
        'tittle' : tittle,
        'activedatabases' : sidebaractive,
        'currenttopmenu' : topmenu,
    }
    return render(request, 'databases.html', context)

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
    return render(request, 'stats.html', context)
