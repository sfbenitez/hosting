from django.shortcuts import render, redirect
from .models import Conecta
from django.http import Http404
import os

def index(request):
	conection = Conecta()
	return render(request, "filemanager.html", {
		'lista':conection.list(),
		})

def download(request, file):
	print(file)
	conection = Conecta()
	if file not in conection.list():
	    index(request)
	try:
		print('estoy dentro')
		return render(request, "filemanager.html", {
		'lista':conection.chdir(file),
		})
	except:
		conection.download(file)
		return redirect("/")

# def chgdir(request, file):
#

#em construção
def upload(request):
	if request.method == 'POST':
		arquivo = request.FILES['file']
		#file = open(arquivo,'rb')
		conection = Conecta()
		print(dir(arquivo))
		print(arquivo.file)
		conection.upload(arquivo)
		return redirect("/")
	return render(request, "core/upload.html")
