from django.shortcuts import render

def index(request):
    tittle='Título'
    variabledefuncion='Prueba'
    context = {
        'variabledehtml' : variabledefuncion,
        'tittle' : tittle,
    }
    return render(request, 'login.html', context)
