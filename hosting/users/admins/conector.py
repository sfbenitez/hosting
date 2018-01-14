from ldap3 import Server, Connection, ALL
from ftplib import FTP, all_errors
import psycopg2

### LDAP Conector
class LdapConector(object):

    def initialize_ldap_connection():
        host = '10.0.5.2'
        ldap_user = ''
        ldap_password = ''
        server = Server(host, get_info=ALL)
        conn = Connection(server, ldap_user, ldap_password, auto_bind=True)
        return conn

    def rebind_to_ldap_auth_connection(conn, ldap_auth_user_password):
        # DN Auth user
        ldap_auth_user = 'cn=admin,dc=sergio,dc=gonzalonazareno,dc=org'
        conn.rebind(ldap_auth_user, ldap_auth_user_password)
        return conn

    def rebind_to_ldap_auto_auth_connection(conn):
        # DN Auth user
        ldap_auth_user = 'cn=admin,dc=sergio,dc=gonzalonazareno,dc=org'
        ldap_auth_user_password = 'usuario'
        conn.rebind(ldap_auth_user, ldap_auth_user_password)
        return conn

### FTP Conector
class FTPConector(object):

    def _initialize_ftp_connection(ftp_user, ftp_password):
        # host="172.22.200.127"
        conn = FTP('10.0.5.2', user=ftp_user, passwd=ftp_password)
        conn.set_pasv(False)
        return conn

### Postgresql Conector
class PGConector(object):

    def _initialize_ftp_db_connection():
        return psycopg2.connect(dbname='proftp',
                                host='10.0.5.2',
                                user='proftp_user',
                                password='usuario')

    def _initialize_hosting_db_connection():
        return psycopg2.connect(dbname='db_hosting',
                                host='10.0.5.2',
                                user='admin',
                                password='usuario')

    def _initialize_db_connection(db_user, db_password):
        return psycopg2.connect(dbname='postgres',
                                host='10.0.5.2',
                                user=db_user,
                                password=db_password)
