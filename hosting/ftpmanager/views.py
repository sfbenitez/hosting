from django.shortcuts import render, redirect
from . import repository
from django.http import Http404
import os

def index(request):
	# path='/'
	ftp_user='sfbenitez'
	ftp_password='usuario'
	conection = repository.FtpManagerRepository(ftp_user,ftp_password)
	dirs, files, pwd  = conection._get_dir_details('/')
	return render(request, "filemanager.html", {
		'dirs':dirs,
		'files':files,
		'pwd':pwd
		})

def dir_details(request, path):
	print(path)
	ftp_user='sfbenitez'
	ftp_password='usuario'
	conection = repository.FtpManagerRepository(ftp_user,ftp_password)
	dirs, files, pwd = conection._get_dir_details(path)
	base_name = '/user/ftpmanager'
	previouspath = base_name + os.path.dirname(pwd)
	nextpath = base_name + pwd
	return render(request, "filemanager.html", {
		'dirs':dirs,
		'files':files,
		'pwd':pwd,
		'nextpath':nextpath,
		'previouspath':previouspath,
		})
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
