from ldap3 import Server, Connection, ALL


class UsersRepository(object):
    def __init__(self):
        self.conn = LdapConector.initialize_ldap_connection()



    def _ldap_query(self):
        ldap_base = 'dc=sergio,dc=gonzalonazareno,dc=org'
        filter_pattern = '(objectclass=person)'
        attr_list = ['uid', 'gidNumber']
        self.conn.search(ldap_base, filter_pattern, attributes=attr_list)
        return self.conn.entries

    def get_users(self):
        users = self._ldap_query()
        # user types
        common_users = []
        premium_users = []
        for i in users:
            if i.gidNumber.value == 2000:
                common_users.append(i.uid.value)
            elif i.gidNumber.value == 2001:
                premium_users.append(i.uid.value)
        return common_users, premium_users

### LDAP Conector
class LdapConector(object):

    def initialize_ldap_connection():
        host = '10.0.5.2'
        ldap_user = ''
        ldap_password = ''
        server = Server(host, get_info=ALL)
        conn = Connection(server, ldap_user, ldap_password, auto_bind=True)
        return conn
