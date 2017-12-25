# -*- coding: utf-8 -*-

from django.shortcuts import render
import psycopg2
from . import repository

def index(request):
    title='DBmanager'
    sidebaractive='active'
    topmenu='current'
    db_manager_repository = repository.DBManagerRepository('sergio.ferrete', 'usuario')
    db_names = db_manager_repository.get_db_names_for_user('sergio.ferrete')

    db_names_list =  [db_name[0] for db_name in db_names]
    context = {
        'title' : title,
        'activedomains' : sidebaractive,
        'currenttopmenu' : topmenu,
        'db_names_list' : db_names_list,
    }
    return render(request, 'databases.html', context)
