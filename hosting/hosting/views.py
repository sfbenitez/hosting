# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from users.admins import repository

def register(request):
	request.POST["domain"]
	request.POST["givenname"]
	request.POST["surname"]
	request.POST["email"]
	request.POST["app_user"]
	request.POST["app_password"]
	request.POST["ftp_user"]
	request.POST["ftp_password"]
	request.POST["db_user"]
	request.POST["db_password"]
	request.POST["premium"]

	return render(request,'register.html')

def singin(request):
	context={'next':"/"}
	if 'next' in request.GET:
		context={'next':request.GET["next"]}
	if request.method=="POST":
		username = request.POST["username"]
		user = authenticate(username=request.POST["username"], password=request.POST["password"])
		if user is None:
			context={'error':True}
		else:
			login(request, user)
			user_repository = repository.UsersRepository()
			common_users, premium_users = user_repository.get_users()
			admin_users = user_repository.get_admins()
			if username not in admin_users:
				if username not in premium_users:
					return redirect('/user/dashboard')
				else:
					request.session["premium"] = True
					return redirect('/user/dashboard')
			else:
				request.session["admin"] = True
				return redirect('/admin/dashboard')


	return render(request, 'login.html', context)

@login_required(login_url='/')
def salir(request):
    logout(request)
    return redirect('/')
