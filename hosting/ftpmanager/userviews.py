# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import repository
from django.http import Http404
import os
from passlib.hash import md5_crypt

@login_required
def index(request):
	# HTML Content
	title='FTP Manager'
	sidebaractive='active'
	topmenu='current'
	context = {
		'title' : title,
		'activeftpmanager' : sidebaractive,
		'currenttopmenu' : topmenu,
	}
	app_user=request.user.username
	ftp_user = repository.get_ftp_user_for_app_user(app_user)
	if ftp_user == "":
		context["ftp_user_not_exist"] = True
		return render(request, "filemanager.html", context)
	else:
		context["ftp_user_exist"] = True
		context["ftp_user"] = ftp_user
		if 'ftp_password' in request.session:
			del request.session['ftp_password']
		return render(request, "filemanager.html", context)


@login_required
def dir_details(request, path):
	# HTML Content
	title='FTP Directory'
	sidebaractive='active'
	topmenu='current'
	context = {
		'title' : title,
		'activeftpmanager' : sidebaractive,
		'currenttopmenu' : topmenu,
	}
	app_user=request.user.username
	ftp_user = repository.get_ftp_user_for_app_user(app_user)
	if 'ftp_password' not in request.session:
		ftp_password = request.POST['password']
		request.session['ftp_password'] = ftp_password
	else:
		ftp_password = request.session['ftp_password']

	try:
		conn = repository.FtpManagerRepository(ftp_user,ftp_password)
		context['user_ftp_authenticated'] = True
	except:
		context['password_error'] = True
		context['ftp_user'] = ftp_user
		return render(request, "filemanager.html", context)
	# Get ftp details
	dirs, files, pwd = conn.get_dir_details(path)
	# quota details
	init_ftp_manage = repository.ManageFTPUser()
	quota = init_ftp_manage.get_quota_used(ftp_user)
	quota_limit = int(quota[0] / 1024 / 1024) # MB
	quota_used = int(quota[1] / 1024 / 1024) # MB
	quota_percent = int((quota_used * 100) / quota_limit)
	base_name = '/user/ftpmanager/directory'
	previouspath = base_name + os.path.dirname(pwd)
	nextpath = base_name + pwd

	# Fill context
	context['quota_limit'] = quota_limit
	context['quota_used'] = quota_used
	context['quota_percent'] = quota_percent
	context['ftp_user'] = ftp_user
	context['dirs'] = dirs
	context['files'] = files
	context['pwd'] = pwd
	context['nextpath'] = nextpath
	context['previouspath'] = previouspath
	context['prefixpassword'] = ftp_password[:2]

	return render(request, "filemanager.html", context)

@login_required
def new_ftp_user(request):
	app_user=request.user.username
	ftp_user = request.POST['username']
	ftp_password = request.POST['password']
	ftp_password2 = request.POST['password2']
	is_premium = request.session.get('premium', False)
	if ftp_password == ftp_password2:
		init_create_ftp_user = repository.ManageFTPUser()
		init_create_ftp_user.create_ftp_user_for_app_user(app_user,
															ftp_user,
															ftp_password,
															is_premium)

	# 	except:
	# 		return render(request, "filemanager.html", {'user_taken' : True})
	else:
		return render(request, "filemanager.html", {'password_not_confirm' : True})

	return index(request)

@login_required
def upload_file(request):
	app_user=request.user.username
	ftp_user = repository.get_ftp_user_for_app_user(app_user)
	ftp_password = request.POST['password']
	directory_to_upload = request.POST['pwd']
	file_name = request.FILES['file'].name
	file_content = request.FILES['file'].file
	conn = repository.FtpManagerRepository(ftp_user,ftp_password)
	conn.upload_file(directory_to_upload, file_name, file_content)

	return dir_details(request, path = directory_to_upload)

@login_required
def delete_file(request):
	app_user=request.user.username
	ftp_user = repository.get_ftp_user_for_app_user(app_user)
	ftp_password = request.POST['password']
	current_directory = request.POST['pwd']
	file_name = request.POST['filename']
	conn = repository.FtpManagerRepository(ftp_user,ftp_password)
	conn.delete_file(current_directory, file_name)

	return dir_details(request, path = current_directory)

@login_required
def make_rem_dir(request):
	app_user=request.user.username
	ftp_user = repository.get_ftp_user_for_app_user(app_user)
	ftp_password = request.POST['password']
	directory_where_make_dirs = request.POST['pwd']
	dir_name = request.POST['dirname']

	conn = repository.FtpManagerRepository(ftp_user,ftp_password)
	new_dir = conn.mk_rem_dirs(directory_where_make_dirs, dir_name)

	return dir_details(request, path = new_dir)

#
# def download(request, file):
# 	print(file)
# 	conection = Conecta()
# 	if file not in conection.list():
# 	    index(request)
# 	try:
# 		print('estoy dentro')
# 		return render(request, "filemanager.html", {
# 		'lista':conection.chdir(file),
# 		})
# 	except:
# 		conection.download(file)
# 		return redirect("/")

# def chgdir(request, file):
#

#em construção
# def upload(request):
# 	if request.method == 'POST':
# 		arquivo = request.FILES['file']
# 		#file = open(arquivo,'rb')
# 		conection = Conecta()
# 		print(dir(arquivo))
# 		print(arquivo.file)
# 		conection.upload(arquivo)
# 		return redirect("/")
# 	return render(request, "core/upload.html")
