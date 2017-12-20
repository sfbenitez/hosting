from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login

def index(request):
	context={'next':"/"}
	if 'next' in request.GET:
		context={'next':request.GET["next"]}
	if request.method=="POST":
		user = authenticate(username=request.POST["username"], password=request.POST["password"])
		if user is None:
			context={'error':True}
		else:
			login(request, user)
			return redirect('/user/dashboard')
	return render(request, 'login.html',context)

@login_required(login_url='/')
def salir(request):
    logout(request)
    return redirect('/')

# def index(request):
#     tittle='Título'
#     variabledefuncion='Prueba'
#     context = {
#         'variabledehtml' : variabledefuncion,
#         'tittle' : tittle,
#     }
#     return render(request, '/static/login.html', context)
#
# def dashboard(request):
#     tittle='Dashboard'
#     variabledefuncion='Prueba'
#     context = {
#         'variabledehtml' : variabledefuncion,
#         'tittle' : tittle,
#     }
#     return render(request, '/static/dashboard.html', context)
