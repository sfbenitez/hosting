from . import conector
from django.template.loader import render_to_string

class UsersRepository(object):
    def __init__(self):
        self.ldap_users_base = 'ou=People,dc=sergio,dc=gonzalonazareno,dc=org'
        self.conn = conector.LdapConector.initialize_ldap_connection()

    def _ldap_query(self):
        filter_pattern = '(objectclass=person)'
        attr_list = ['uid', 'gidNumber', 'uidNumber']
        self.conn.search(self.ldap_users_base, filter_pattern, attributes=attr_list)
        return self.conn.entries

    def get_admins(self):
        users = self._ldap_query()
        admin_users = []
        for user in users:
            if user.gidNumber.value == 2050:
                admin_users.append(user.uid.value)
        return admin_users

    def get_users(self):
        users = self._ldap_query()
        # user types
        common_users = []
        premium_users = []

        for user in users:
            if user.gidNumber.value == 2000:
                common_users.append(user.uid.value)
            elif user.gidNumber.value == 2001:
                premium_users.append(user.uid.value)
        return common_users, premium_users

    def get_uidNumber_for_user(self):
        users = self._ldap_query()
        uidNumber_list = []
        for user in users:
            uidNumber_list.append(user.uidNumber.value)
        uidNumber_list.sort()
        last_uid = uidNumber_list[-1] + 1
        return int(last_uid)

    def get_pwhash_for_user(self, textplain_passwd):
        # Only needed for that
        from passlib.hash import ldap_salted_sha1
        password_hash = ldap_salted_sha1.encrypt(textplain_passwd)
        return password_hash

    def create_user(self, ldap_auth_user_password, user):
        # App user
        auth_conn = conector.LdapConector.rebind_to_ldap_auth_connection(self.conn, ldap_auth_user_password)
        # That comma is really important
        user_dn = 'uid=' + user['uid'] + ',' + self.ldap_users_base
        auth_conn.add(user_dn, user['objectclass'], user['user_attributes'])
        auth_conn.unbind()


    def delete_user(self, ldap_auth_user_password, user):
        auth_conn = conector.LdapConector.rebind_to_ldap_auth_connection(self.conn, ldap_auth_user_password)
        # That comma is really important
        user_dn = 'uid=' + user + ',' + self.ldap_users_base
        auth_conn.delete(user_dn)
        auth_conn.unbind()


class ManageDomains(object):

    def _mk_dom_config_file(zonefile, context):
        zonefile_dir = '/var/cache/bind/'
        template = 'admin/dns/new_zone.tpl'
        open(zonefile_dir + zonefile, "w").write(render_to_string(template, context))

    def _new_free_domain(self, domain, app_user):
        context = {}
        context['domain'] = domain
        context['app_user'] = app_user
        self._mk_dom_config_file(zonefile, context)
        path = '/etc/bind/named.conf.local'
        zonasdns = open(path,"a")
        zonefile='db.' + domain
        zona='//{}\nzone "{}" {\n type master;\n file "{}.db";}\n;\n//{}\n'.format(app_user,domain,zonefile,app_user)
        zonasdns.write(zona)
        zonasdns.close()
    #
    # def _del_domain(domain, app_user):
    #     lines = open(path).readlines()
    #     blockstart = lines.index(block + "\n")
    #     print blockstart
    #     blockend = blockstart+6
    #     print blockend
    #     del(lines[blockstart:blockend])
    #     open(path, 'w+').writelines(lines)
