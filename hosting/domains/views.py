# -*- coding: utf-8 -*-

from django.shortcuts import render
from users.admins import repository

def index(request):
    tittle='Domains'
    sidebaractive='active'
    topmenu='current'
    context = {
        'tittle' : tittle,
        'activedomains' : sidebaractive,
        'currenttopmenu' : topmenu,
    }
    app_user = request.user.username
    domain = 'example.org'
    dom_manager = repository.ManageDomains._new_free_domain(domain, app_user)
    return render(request, 'domains.html', context)
