# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request):
    title='CMS List'
    sidebaractive='active'
    topmenu='current'
    context = {
        'title' : title,
        'activeapps' : sidebaractive,
        'currenttopmenu' : topmenu,
    }
    return render(request, 'cmslist.html', context)
