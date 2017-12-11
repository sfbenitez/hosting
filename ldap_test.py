########## initialize connection ###############################################

import ldap
con = ldap.initialize('ldap://172.22.200.116')

# At this point, we're connected as an anonymous user
# If we want to be associated to an account
# you can log by binding your account details to your connection

# AUTENTICACON
#con.simple_bind_s("cn=admin,dc=example,dc=com", "my_password")

########## performing a simple ldap query ####################################
def ldap_search(UID):
    ldap_base = "dc=sergio,dc=gonzalonazareno,dc=org"
    query = "(uid=%s)"%(UID)
    result = con.search_s(ldap_base, ldap.SCOPE_SUBTREE, query)

    return result

# ########## adding (a user) ####################################################
# # make sure all input strings are str and not unicode
# # (it doesn't like unicode for some reason)
# # each added attribute needs to be added as a list
#
# dn = "uid=maarten,ou=people,dc=example,dc=com"
# modlist = {
#            "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"],
#            "uid": ["maarten"],
#            "sn": ["De Paepe"],
#            "givenName": ["Maarten"],
#            "cn": ["Maarten De Paepe"],
#            "displayName": ["Maarten De Paepe"],
#            "uidNumber": ["5000"],
#            "gidNumber": ["10000"],
#            "loginShell": ["/bin/bash"],
#            "homeDirectory": ["/home/maarten"]}
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

uid=raw_input("Introduce un UID a buscar: ")
busqueda=ldap_search(uid)
print busqueda
