import ldap

def ldap_search(UID):
	## The next lines will also need to be changed to support your search requirements and directory
	baseDN = "dc=sergio,dc=gonzalonazareno,dc=org"
	searchScope = ldap.SCOPE_SUBTREE
	## retrieve all attributes - again adjust to your needs - see documentation for more options
	retrieveAttributes = None
	searchFilter = 'uid=%s'%(UID)

	try:
		ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
		result_set = []
		while 1:
			result_type, result_data = l.result(ldap_result_id, 0)
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

## first you must open a connection to the server
try:
	l = ldap.open("172.22.200.116")
	## searching doesn't require a bind in LDAP V3.  If you're using LDAP v2, set the next line appropriately
	## and do a bind as shown in the above example.
	# you can also set this to ldap.VERSION2 if you're using a v2 directory
	# you should  set the next option to ldap.VERSION2 if you're using a v2 directory
	l.protocol_version = ldap.VERSION3
except ldap.LDAPError, e:
	print e
	# handle error however you like

uid=raw_input("Introduce un UID a buscar: ")

busqueda=ldap_search(uid)

print busqueda
