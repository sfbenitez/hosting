import psycopg2

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
