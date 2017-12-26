# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
import psycopg2
from . import repository

def index(request):
    title='DBmanager'
    sidebaractive='active'
    topmenu='current'
    context = {
        'title' : title,
        'activedatabases' : sidebaractive,
        'currenttopmenu' : topmenu,
    }
    app_user=request.user.username
    print(app_user)
    try:
        db_user = repository.get_db_user_for_app_user(app_user)
        print('Funciona: ' + db_user)
    except:
        db_user = None

    if db_user is None:
        db_user_not_exist = True
        context['db_user_not_exist'] = db_user_not_exist

    context['db_user'] = db_user
    context['password_required'] = True
    return render(request, 'databases.html', context)

def db_list(request):
    title='DB List'
    sidebaractive='active'
    topmenu='current'
    context = {
        'title' : title,
        'activedatabases' : sidebaractive,
        'currenttopmenu' : topmenu,
    }
    try:
        app_user=request.user.username
        db_user = repository.get_db_user_for_app_user(app_user)
        db_password=request.POST['password']
        print(db_user)
        print(db_password)
        db_manager_repository = repository.DBManagerRepository(db_user, db_password)
        db_names = db_manager_repository.get_db_names_for_user(db_user)
        db_names_list =  [db_name[0] for db_name in db_names]
        context['db_names_list'] = db_names_list
    except:
        db_user_error = 'Error al autenticar con la base de datos'
        context['db_user_error'] = db_user_error
    return render(request, 'databases.html', context)


def new_db_user(request):
    title='New DBmanager User'
    sidebaractive='active'
    topmenu='current'
    context = {
        'title' : title,
        'activedatabases' : sidebaractive,
        'currenttopmenu' : topmenu,
    }
    app_user=request.user.username
    db_user=request.POST['username']
    db_password=request.POST['password']
    init_create_db_user = repository.CreateDBUser()
    create_db_user = init_create_db_user.create_db_user_for_app_user(app_user, db_user, db_password)

    return redirect('/user/databases')
