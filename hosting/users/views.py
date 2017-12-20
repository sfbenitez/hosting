from django.shortcuts import render

def index(request):
    tittle='Dashboard'
    variabledefuncion='Prueba'
    context = {
        'variabledehtml' : variabledefuncion,
        'tittle' : tittle,
    }
    return render(request, 'index.html', context)
