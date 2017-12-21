from django.shortcuts import render

def index(request):
    tittle='Dashboard'
    sidebaractive='active'
    topmenu='current'
    context = {
        'tittle' : tittle,
        'activedashboard' : sidebaractive,
    }
    return render(request, 'index.html', context)

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
