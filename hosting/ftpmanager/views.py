from django.shortcuts import render, redirect
from . import repository
from django.http import Http404
import os
from .forms import FTPUploadFileForm

def index(request):
	# path='/'
	app_user=request.user.username
	ftp_user = repository.get_ftp_user_for_app_user(app_user)
	print(ftp_user)
	ftp_password='usuario'
	conection = repository.FtpManagerRepository(ftp_user,ftp_password)
	dirs, files, pwd  = conection.get_dir_details('/')
	return render(request, "filemanager.html", {
		'dirs':dirs,
		'files':files,
		'pwd':pwd
		})

def dir_details(request, path):
	print(path)
	app_user=request.user.username
	ftp_user = repository.get_ftp_user_for_app_user(app_user)
	print(ftp_user)
	ftp_password = 'usuario'
	conn = repository.FtpManagerRepository(ftp_user,ftp_password)
	dirs, files, pwd = conn.get_dir_details(path)
	base_name = '/user/ftpmanager/directory'
	previouspath = base_name + os.path.dirname(pwd)
	nextpath = base_name + pwd
	return render(request, "filemanager.html", {
		'dirs':dirs,
		'files':files,
		'pwd':pwd,
		'nextpath':nextpath,
		'previouspath':previouspath,
		})

def new_ftp_user(request):
	app_user=request.user.username
	ftp_user = 'sfbenitez_ftp'
	ftp_password = 'usuario'
	init_create_ftp_user = repository.CreateFTPUser()
	init_create_ftp_user.create_ftp_user_for_app_user(app_user,
													ftp_user,
													ftp_password)
	return index(request)

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
