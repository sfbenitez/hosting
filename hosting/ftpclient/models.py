import os
from django.db import models
from ftplib import FTP

class Conecta(object):
	"""docstring for Conecta"""
	def __init__(self):
		self.url = "10.0.5.2"
		self.handler = FTP(self.url, user='sfbenitez', passwd='usuario')
		self.urldown = "/home/ferrete/Descargas/"

	def list(self):
		lista = []
		a = self.handler.nlst()
		for f in a:
			lista.append(f)
		return lista

	def chdir(self,file):
		print(os.path.dirname(file))
		self.handler.cwd(os.path.dirname(file))
		lista2 = []
		a = self.handler.nlst()
		for h in a:
			lista2.append(h)
		return lista2

	def get_dir_details(path):
		# Connection must be open!
		try:
			lines = []
			self.handler.retrlines('LIST ' + path, lines.append)
			dirs = {}
			files = {}
			for line in lines:
				words = line.split()
				if len(words) < 6:
					continue
				if words[-2] == '->':
					continue
				if words[0][0] == 'd':
					dirs[words[-1]] = 0
				elif words[0][0] == '-':
					files[words[-1]] = int(words[-5])
				return dirs, files
		except ftplib.all_errors:
			print('error')


	def download(self, file):
		self.urldown = "/home/ferrete/Descargas/"
		print(file)
		Dfile = open(self.urldown + file, 'wb')
		self.handler.retrbinary('RETR ' + file, Dfile.write)
		Dfile.close()
		return True

	# def upload(self, file):
	# 	self.handler.storbinary('STOR ' + str(file), open(file, 'rb'), 1024)
	# 	return True
