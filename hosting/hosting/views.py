# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from users.admins import repository
from users.admins.ftprepository import ManageFTPUser
from users.admins.dbrepository import CreateDBUser

def register(request):
	domain = request.POST["domain"]
	givenname = request.POST["givenname"]
	surname = request.POST["surname"]
	email = request.POST["email"]
	app_user = request.POST["app_user"]
	app_password = request.POST["app_password"]
	ftp_user = request.POST["ftp_user"]
	ftp_password = request.POST["ftp_password"]
	db_user = request.POST["db_user"]
	db_password = request.POST["db_password"]
	premium = request.POST["premium"]
	# Create FTP User
	ftp_repository = ManageFTPUser()
	ftp_repository.create_ftp_user_for_app_user(app_user,
												ftp_user,
												ftp_password,
												premium)
	# Create DB User
	db_repository = CreateDBUser()
	db_repository.create_db_user_for_app_user(app_user, db_user, db_password)

	# Create App LDAP User
	if premium == 'False':
	# common users gidNumber
		gidNumber = 2000
	else:
	# premium users gidNumber
		gidNumber = 2001

	user_repository = repository.UsersRepository()
	password_hash = user_repository.get_pwhash_for_user(app_password)
	uidNumber = user_repository.get_uidNumber_for_user()
	# LDAP User Dictionary
	user = {}
	user['uid'] = app_user
	user['objectclass'] = ['top', 'inetOrgPerson', 'person', 'posixAccount']
	user['user_attributes'] = {
		'cn': app_user,
		'uid': app_user,
		'uidNumber': uidNumber,
		'gidNumber': gidNumber,
		'userPassword': password_hash,
		'homeDirectory': '/srv/hosting/' + app_user,
		'sn': surname,
		'mail': email,
		'givenName': name}
	user_repository.register_user(user)

	# Create new domain
	dom_manager = repository.ManageDomains(domain, app_user)
	dom_manager.new_domain()

	# Auth, login and redirect new user
	user = authenticate(username=app_user, password=app_password)
	login(request, user)
	if premium == 'False':
		return redirect('/user/dashboard')
	else:
		request.session["premium"] = True
		return redirect('/user/dashboard')


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
