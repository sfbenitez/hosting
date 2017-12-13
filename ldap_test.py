# -*- coding: utf-8 -*-
########## initialize connection ###############################################
import ldap
import os
import jinja2
from passlib.hash import sha256_crypt

con = ldap.initialize('ldap://172.22.200.116')

# At this point, we're connected as an anonymous user
# If we want to be associated to an account
# you can log by binding your account details to your connection

# AUTENTICACON
#con.simple_bind_s("cn=admin,dc=example,dc=com", "my_password")

########## performing a simple ldap query ####################################
def ldap_search(UID):

	baseDN = "dc=sergio,dc=gonzalonazareno,dc=org"
	searchScope = ldap.SCOPE_SUBTREE
	## retrieve all attributes - again adjust to your needs - see documentation for more options
	retrieveAttributes = None
	searchFilter = 'uid=%s'%(UID)

	try:
		ldap_result_id = con.search(baseDN, searchScope, searchFilter, retrieveAttributes)
		result_set = []
		while 1:
			result_type, result_data = con.result(ldap_result_id, 0)
			if (result_data == []):
				break
			else:
				## here you don't have to append to a list
				## you could do whatever you want with the individual entry
				## The appending to list is just for illustration.
				if result_type == ldap.RES_SEARCH_ENTRY:
					result_set.append(result_data)
		resultado = result_set
	except ldap.LDAPError, e:
		print e

        return resultado

# ########## adding (a user) ####################################################
# # make sure all input strings are str and not unicode
# # (it doesn't like unicode for some reason)
# # each added attribute needs to be added as a list
#
# dn = "uid=maarten,ou=people,dc=example,dc=com"
# modlist = {
#            "objectClass": ["top","inetOrgPerson", "posixAccount", "person"],
#            "uid": ["maarten"],
#            "sn": ["De Paepe"],
#            "givenName": ["Maarten"],
#            "cn": ["Maarten De Paepe"],
#            "displayName": ["Maarten De Paepe"],
#            "uidNumber": ["5000"],
#            "gidNumber": ["10000"],
#            "mail": ["example@gmail.com"],
#            "userPassword": ["10{SHA}hRNsecv5/ja7nQXQY5xwwmXBjTc=000"],
#            "loginShell": ["/bin/bash"],
#            "homeDirectory": ["/var/www/hosting/usuario"]}
#           }
# # addModList transforms your dictionary into a list that is conform to ldap input.
# result = con.add_s(dn, ldap.modlist.addModlist(modlist))
#
# ########## modifying (a user, or in this case, the user's password) ##########
# # this works a bit strange.
# # in a rel. database you just give the new value for the record you want to change
# # here you need to give an old/new pair
#
# dn = "uid=maarten,ou=people,dc=example,dc=com"
# # you can expand this list with whatever amount of attributes you want to modify
# old_value = {"userPassword": ["my_old_password"]}
# new_value = {"userPassword": ["my_new_password"]}
#
# modlist = ldap.modlist.modifyModlist(old_value, new_value)
# con.modify_s(dn, modlist)
#
# ########## deleting (a user) #################################################
# dn = "uid=maarten,ou=people,dc=example,cd=com"
# con.delete_s(dn)


# ########## buscar informacion de un UID en el ldap #################################################

# uid=raw_input("Introduce un UID a buscar: ")
# busqueda=ldap_search(uid)
# print busqueda

# ########## pasos de creacion de nuevo usuario #################################################
# Si el usuario o el nombre del dominio existen, no se continua.

# uid=raw_input("Introduce un UID a buscar: ")
# busqueda=ldap_search(uid)
# if len(busqueda)!=0:
#     print 'usuario existe'
# else:
#     print 'puede crearse el usuario %s' %(uid)
#     #añadir pasos de la creacion del usuario

# Se creará el directorio personal del usuario, este directorio será el DocumentRoot del servidor web. En este directorio se tendrá que crear una página web de bienvenida.

# crear directorio

#if not os.path.exists('/srv/hosting/usuario'):
#     os.mkdir('/srv/hosting/usuario')

# añadir DocumentRoot al fichero virtualhost

# ########## creacion template jinja2  #################################################

# def render(tpl_path, context):
#     path, filename = os.path.split(tpl_path)
#     return jinja2.Environment(
#         loader=jinja2.FileSystemLoader(path or './')
#     ).get_template(filename).render(context)
#
# context = {
#     'servername': 'www.prueba.com',
#     'documentroot': '/var/www/prueba'
# }
#
# result = render('templates/virtualhost.tpl', context)
#
# print(result)

# comprobar esto para guardar el documento como fichero
# http://jinja.pocoo.org/docs/dev/api/#jinja2.environment.TemplateStream.dump

# crear pagina web bienvenida

# Se creará un nuevo virtual hosting (www.nombrededomino.com) con el DocumentRoot apuntando al directorio personal que anteriormente hemos instalado.

# Se creará un nuevo usuario virtual para el acceso por FTP. El administrador decidirá la política para generar la contraseña. Dicha contraseña generada tendrá que visualizarse por pantalla. La contraseña será guardada en la base de datos encriptada.

# ########## creacion de contraseña #################################################

# class Create_password():
#
#     def __init__(self, username, password):
#         self.username = username
#         self.pw_hash = sha256_crypt.encrypt(password)
#
#     def verify(self, password):
#         return sha256_crypt.verify(password, self.pw_hash)
#
# username=raw_input("Introduce un nombre de usuario: ")
# userpass=raw_input("Introduce la contraseña del usuario: ")
#
# #generacion de contraseña
# new_pass = Create_password(username,userpass)
#
# print "verificar si la contraseña es %s" %(username)
# print(new_pass.verify(userpass))


# Se creará un nuevo usuario en el gestor de base de datos mysql, se debe llamar mynombredeusuario, la contraseña que se genere para mysql debe ser distinta a la generada para la gestión del FTP y también se debe mostrar.



# Se creará una nueva zona nombrededominio.com en el servidor DNS bind9 con las zonas de resolución directa e inversa que permitan conocer los distintos nombres (www,ftp, mysql, ...)


# creacion de cuota
#http://somebooks.es/9-6-cuotas-de-disco/
