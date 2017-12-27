from hosting.models import AppUserDbUserRelation
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class CreateDBUser(object):
    def __init__(self):
        self.conn = self._initialize_db_connection()

    def _initialize_db_connection(self):
        if not hasattr(self, 'conn'):
            return psycopg2.connect(dbname='db_hosting',
                                    host='10.0.5.2',
                                    user='admin',
                                    password='usuario')
        return self.conn

    def _make_user_relations(self, app_user, db_user):
        AppUserDbUserRelation.objects.create(app_user=app_user, db_user=db_user)


    def create_db_user_for_app_user(self, app_user, db_user, db_password):
        self._make_user_relations(app_user, db_user)
        cur = self.conn.cursor()
        cur.execute("""create role {}
                    password '{}' login createdb
                    in role viewdatabases""".format(db_user, db_password))
        cur.close()
        self.conn.commit()
        self.conn.close()



def get_db_user_for_app_user(user):
    user_data = AppUserDbUserRelation.objects.get(app_user=user)
    db_user = user_data.db_user
    return db_user

class DBManagerRepository(object):

    def __init__(self, db_user, db_password):
        self.conn = self._initialize_db_connection(db_user, db_password)

    def _initialize_db_connection(self, db_user, db_password):
        if not hasattr(self, 'conn'):
            return psycopg2.connect(dbname='postgres',
                                    host='10.0.5.2',
                                    user=db_user,
                                    password=db_password)
        return self.conn

    def get_db_names_for_user(self, username):
        cur = self.conn.cursor()
        cur.execute("""select datname
            from pg_database
            join pg_authid on datdba = pg_authid.oid
            and rolname = '{}'""".format(username))
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        return data

    def create_new_db_for_user(self, db_user, db_name):
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = self.conn.cursor()
        self.db_name="{}_{}".format(db_user,db_name)
        try:
            cur.execute("""create database {}""".format(self.db_name))
        except:
            return "Database already exist"
        cur.close()
        self.conn.close()
        return self.db_name

    def delete_db_for_user(self, db_name):
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = self.conn.cursor()
        cur.execute("""drop database {}""".format(db_name))
        cur.close()
        self.conn.close()
        return db_name
