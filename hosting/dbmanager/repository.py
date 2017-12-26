from hosting.models import UserRelations
import psycopg2


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

    def create_db_user_for_app_user(self, app_user, db_user, db_password):
        try:
            UserRelations.objects.create(app_user=app_user, bd_user=db_user)
        except Exception:
            print(Exception)

        cur = self.conn.cursor()
        cur.execute("""create role {}
                    password '{}' login createdb
                    in role viewdatabases""".format(db_user, db_password))
        cur.close()
        self.conn.commit()
        self.conn.close()



def get_db_user_for_app_user(user):
    user_data = UserRelations.objects.get(app_user=user)
    db_user = user_data.bd_user
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
