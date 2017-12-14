# -*- coding: utf-8 -*-
import ldap
import os
import jinja2
from passlib.hash import sha256_crypt
from ldap import modlist

# conexion con ldap
con = ldap.initialize('ldap://172.22.200.116')
# autenticacion con ldap
con.simple_bind_s("cn=admin,dc=sergio,dc=gonzalonazareno,dc=org", "usuario")


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

#### buscar informacion de un UID en el ldap
# uid=raw_input("Introduce un UID a buscar: ")
# busqueda=ldap_search(uid)
# print busqueda

#### buscar si usuario existe
# uid=raw_input("Introduce un UID a buscar: ")
# busqueda=ldap_search(uid)
# if len(busqueda)!=0:
#     print 'usuario existe'
# else:
#     print 'puede crearse el usuario %s' %(uid)
#     #añadir pasos de la creacion del usuario

def ldap_newuser(v_uid,v_sn,v_givenName,v_uidNumber,v_mail,v_userpass,v_homeDirectory):

	dn = "uid="+v_uid+",ou=People,dc=sergio,dc=gonzalonazareno,dc=org"
	modlist = { # addModList transforms your dictionary into a list that is conform to ldap input.
	           "objectClass": ["top","inetOrgPerson", "posixAccount", "person"],
	           "uid": [v_uid],
	           "sn": [v_sn],
	           "givenName": [v_givenName],
	           "uidNumber": [v_uidNumber],
			   "cn": ["ftpuser"],
	           "gidNumber": ["3000"],
	           "mail": [v_mail],
	           "userPassword": [v_userpass],
	           "loginShell": ["/bin/bash"],
	           "homeDirectory": [v_homeDirectory]
	          }

	try:
		result = con.add_s(dn, ldap.modlist.addModlist(modlist))
	except ldap.LDAPError, e:
		print e

#### añadir usuario al ldap
# dictprueba = {'v_uid': 'prueba','v_sn': 'python','v_givenName': 'prueba python','v_uidNumber': '5002','v_mail': 'example@gmail.com','v_userpass': 'pass','v_homeDirectory': '/var/www/hosting/python'}
# ldap_newuser(**dictprueba)


def ldap_deluser(v_uid):

	dn = "uid="+v_uid+",ou=People,dc=sergio,dc=gonzalonazareno,dc=org"
	con.delete_s(dn)

#### borrar usuario ldap


def ldap_changepass(v_uid,v_old,v_new):

	dn = "uid="+v_uid+",ou=People,dc=sergio,dc=gonzalonazareno,dc=org"
	old_value = {"userPassword": [v_old]}
	new_value = {"userPassword": [v_new]}

	modlist = ldap.modlist.modifyModlist(old_value, new_value)
	try:
		con.modify_s(dn, modlist)
	except ldap.LDAPError, e:
		print e

##### cambiar contraseña usuario ldap
#
# ldap_changepass("prueba","newpass","newppas2")


# Se creará el directorio personal del usuario, este directorio será el DocumentRoot del servidor web. En este directorio se tendrá que crear una página web de bienvenida.

### crear directorio

#if not os.path.exists('/srv/hosting/usuario'):
#     os.mkdir('/srv/hosting/usuario')


##### creacion template jinja2

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

# # crear tempalte
#
# context = {
#     'servername': 'www.prueba.com',
#     'documentroot': '/var/www/prueba'
# }
#
# result = render('templates/virtualhost.tpl', context)
# print(result)

# comprobar esto para guardar el documento como fichero
# http://jinja.pocoo.org/docs/dev/api/#jinja2.environment.TemplateStream.dump


# ########## creacion de contraseña #################################################

class Create_password():

    def __init__(self, username, password):
        self.username = username
        self.pw_hash = sha256_crypt.encrypt(password)

    def verify(self, password):
        return sha256_crypt.verify(password, self.pw_hash)

# username=raw_input("Introduce un nombre de usuario: ")
# userpass=raw_input("Introduce la contraseña del usuario: ")
#
# #generacion de contraseña
# new_pass = Create_password(username,userpass)
#
# print "verificar si la contraseña es %s" %(username)
# print(new_pass.verify(userpass))

### T O D O

# crear pagina web bienvenida



# Se creará un nuevo usuario virtual para el acceso por FTP. El administrador decidirá la política para generar la contraseña. Dicha contraseña generada tendrá que visualizarse por pantalla. La contraseña será guardada en la base de datos encriptada.



# Se creará un nuevo usuario en el gestor de base de datos mysql, se debe llamar mynombredeusuario, la contraseña que se genere para mysql debe ser distinta a la generada para la gestión del FTP y también se debe mostrar.




# Se creará una nueva zona nombrededominio.com en el servidor DNS bind9 con las zonas de resolución directa e inversa que permitan conocer los distintos nombres (www,ftp, mysql, ...)



# creacion de cuota
#http://somebooks.es/9-6-cuotas-de-disco/
