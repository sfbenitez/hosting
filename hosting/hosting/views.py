from django.shortcuts import render

def index(request):
    tittle='Título'
    variabledefuncion='Prueba'
    context = {
        'variabledehtml' : variabledefuncion,
        'tittle' : tittle,
    }
    return render(request, 'login.html', context)

def dashboard(request):
    tittle='Dashboard'
    variabledefuncion='Prueba'
    context = {
        'variabledehtml' : variabledefuncion,
        'tittle' : tittle,
    }
    return render(request, 'dashboard.html', context)
