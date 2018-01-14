from . import conector
from django.template.loader import render_to_string
from hosting import models
import os
from libgravatar import Gravatar

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

    def register_user(self, user):
        # App user
        auth_conn = conector.LdapConector.rebind_to_ldap_auto_auth_connection(self.conn)
        # That comma is really important
        user_dn = 'uid=' + user['uid'] + ',' + self.ldap_users_base
        auth_conn.add(user_dn, user['objectclass'], user['user_attributes'])
        auth_conn.unbind()


    def _delete_app_user(self, ldap_auth_user_password, user):
        auth_conn = conector.LdapConector.rebind_to_ldap_auth_connection(self.conn, ldap_auth_user_password)
        # That comma is really important
        user_dn = 'uid=' + user + ',' + self.ldap_users_base
        auth_conn.delete(user_dn)
        auth_conn.unbind()

    # def delete_user(self):


class ManageDomains(object):
    def __init__(self, domain, app_user):
        self.domain = domain
        self.app_user = app_user
        #DNS Values
        self.zonefile = 'db.' + self.domain
        self.zoneconffile = '/etc/bind/named.conf.local'
        self.zonefile_dir = '/var/cache/bind/'
        self.zonetemplate = 'admin/services/new_zone.tpl'
        #Apache Values
        self.vhostfile_dir = '/etc/apache2/sites-available/'
        self.apache_log_dir = '/var/log/apache2/'
        self.vhosttemplate = 'admin/services/new_vhost.tpl'
        self.document_root = '/srv/hosting/' + self.app_user
        #awstats values
        self.awstats_dir = '/etc/awstats/'
        self.awstatstemplate = 'admin/services/awstats.tpl'

    def _reload_services(self):
        # Needed
        # ln -s /usr/sbin/a2ensite /usr/local/bin/
        # ln -s /usr/sbin/apachectl /usr/local/bin/
        # ln -s /usr/sbin/rndc /usr/local/bin/
        # visudo
        # hosting ALL = NOPASSWD: /usr/local/bin/apachectl graceful
        # hosting ALL = NOPASSWD: /usr/local/bin/rndc reload
        # hosting ALL = NOPASSWD: /usr/local/bin/a2ensite
        os.system('sudo /usr/local/bin/apachectl graceful')
        os.system('sudo /usr/local/bin/rndc reload')

    def _activate_vhost(self):
        os.system('sudo /usr/local/bin/a2ensite {}'.format(self.domain))

    def _create_awstats_db(self):
        os.system('sudo /usr/lib/cgi-bin/awstats.pl -config=www.{} -update'.format(self.domain))

    def _mk_vhost_config_file(self):
        context = {}
        context['server_name'] = 'www.' + self.domain
        context['document_root'] = self.document_root
        context['app_user'] = self.app_user
        vhostfile = self.domain + '.conf'
        open(self.vhostfile_dir + vhostfile, "w").write(render_to_string(self.vhosttemplate, context))

    def _mk_awstats_config_file(self):
        context = {}
        context['server_name'] = 'www.' + self.domain
        context['logfile'] = self.apache_log_dir + context['server_name'] + '-access.log'
        awstatsfile = 'awstats.' + context['server_name'] + '.conf'
        open(self.awstats_dir + awstatsfile, "w").write(render_to_string(self.awstatstemplate, context))
        self._create_awstats_db()

    def _mk_dom_config_file(self):
        context = {}
        context['domain'] = self.domain
        open(self.zonefile_dir + self.zonefile, "w").write(render_to_string(self.zonetemplate, context))

    def _del_dom_from_dns_config(self):
        zonasdns = open(self.zoneconffile).readlines()
        start = zonasdns.index("""zone \"{}\"\n""".format(self.domain))
        final = start + 5
        del(zonasdns[start:final])
        open(self.zoneconffile, 'w').writelines(zonasdns)

    def _add_dom_to_dns_config(self):
        zonasdns = open(self.zoneconffile,"a")
        zona="""zone "%s" \n{\n\ttype master;\n\tfile "%s";\n};\n""" %(self.domain,self.zonefile)
        zonasdns.write(zona)
        zonasdns.close()

    def _make_app_user_domain_relation(self):
        models.appuserdomains.objects.create(app_user=self.app_user,domain_name=self.domain)

    def new_domain(self):
        self._mk_vhost_config_file()
        self._mk_dom_config_file()
        self._add_dom_to_dns_config()
        self._make_app_user_domain_relation()
        self._activate_vhost()
        self._reload_services()
        self._mk_awstats_config_file

def get_users_domains(app_user):
    user_domains = models.appuserdomains.objects.all()
    domain_list = []
    for i in user_domains:
        if i.app_user == app_user:
            domain_list.append(i.domain_name)
    return domain_list

def get_users_avatar(app_user_mail):
    print(app_user_mail.lower())
    gravatar_mail = Gravatar(app_user_mail.lower())
    avatar_url = gravatar_mail.get_image(size=150, default='http://www.charliejsanchez.com/wp-content/uploads/2017/12/default.jpg')
    return avatar_url
