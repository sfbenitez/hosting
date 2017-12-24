# -*- coding: utf-8 -*-

from django.shortcuts import render

def index(request):
    tittle='Domains'
    sidebaractive='active'
    topmenu='current'
    context = {
        'tittle' : tittle,
        'activedomains' : sidebaractive,
        'currenttopmenu' : topmenu,
    }
    return render(request, 'domains.html', context)
