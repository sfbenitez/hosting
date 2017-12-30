# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import repository
from django.http import Http404
import os

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
	dirs, files, pwd = conn.get_dir_details(path)
	base_name = '/user/ftpmanager/directory'
	previouspath = base_name + os.path.dirname(pwd)
	nextpath = base_name + pwd
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
	if ftp_password == ftp_password2:
		init_create_ftp_user = repository.ManageFTPUser()
		init_create_ftp_user.create_ftp_user_for_app_user(app_user,
															ftp_user,
															ftp_password)
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

	return redirect('dir_details', path = directory_to_upload)
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
