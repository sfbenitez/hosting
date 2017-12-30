# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from ldap3 import Server, Connection, ALL


def index(request):
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
			server = Server('10.0.5.2', get_info=ALL)
			conn = Connection(server, 'cn=admin,dc=sergio,dc=gonzalonazareno,dc=org', 'usuario', auto_bind=True)
			admin_gid = '2001'
			is_admin = conn.search('dc=sergio,dc=gonzalonazareno,dc=org', '(&(uid={})(gidNumber={}))'.format(username, admin_gid))
			if is_admin == False:
				return redirect('/user/dashboard')
			else:
				request.session["admin"] = True
				return redirect('/user/dashboard')


	return render(request, 'login.html', context)

@login_required(login_url='/')
def salir(request):
    logout(request)
    return redirect('/')
