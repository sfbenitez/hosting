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
    listadom = repository.ManageDomains.get_users_domains(app_user)
    context['domains'] = listadom
    return render(request, 'domains.html', context)

def _new_domain(request):
    app_user = request.user.username
    domain = 'ferrete.org'
    dom_manager = repository.ManageDomains.new_domain(domain, app_user)
    return index(request)
