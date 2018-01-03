# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import psycopg2
from . import repository

@login_required
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

@login_required
def db_list(request):
    title='DB List'
    sidebaractive='active'
    topmenu='current'
    context = {
        'title' : title,
        'activedatabases' : sidebaractive,
        'currenttopmenu' : topmenu,
    }
    db_password=request.POST['password']
    app_user=request.user.username
    db_user = repository.get_db_user_for_app_user(app_user)
    context['db_user'] = db_user
    context['db_password'] = db_password[:2]
    # try:
    print(db_user)
    print(db_password)
    db_manager_repository = repository.DBManagerRepository(db_user, db_password)
    db_names = db_manager_repository.get_db_names_for_user(db_user)
    db_names_list =  [db_name[0] for db_name in db_names]
    context['db_number'] = len(db_names_list)
    context['db_names_list'] = db_names_list
    # except:
    #     db_user_error = 'Error al autenticar con la base de datos'
    #     context['db_user_auth_error'] = db_user_error
    return render(request, 'databases.html', context)

@login_required
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
    db_password=request.POST['pwd']
    init_create_db_user = repository.CreateDBUser()
    create_db_user = init_create_db_user.create_db_user_for_app_user(app_user, db_user, db_password)
    context['db_user'] = db_user
    context['new_user'] = True
    return render(request, 'databases.html', context)

@login_required
def new_db(request):
    db_password=request.POST['password']
    db_name=request.POST['newdbname']
    app_user=request.user.username
    db_user = repository.get_db_user_for_app_user(app_user)
    db_manager_repository = repository.DBManagerRepository(db_user, db_password)
    create_db = db_manager_repository.create_new_db_for_user(db_user, db_name)
    if create_db == "Database already exist":
        print('Error al crear la base de datos {}_{}'.format(db_user, db_name))
        return redirect('/user/databases')
    else:
        return redirect('/user/databases')

@login_required
def del_db(request):
    db_password=request.POST['password']
    db_name=request.POST['deletedatabase']
    print(db_name)
    app_user=request.user.username
    db_user = repository.get_db_user_for_app_user(app_user)
    db_manager_repository = repository.DBManagerRepository(db_user, db_password)
    create_db = db_manager_repository.delete_db_for_user(db_name)
    return redirect('/user/databases')
