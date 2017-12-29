# -*- coding: utf-8 -*-
import os
from ftplib import FTP, all_errors
from hosting.models import AppUserFtpUserRelation
import psycopg2


class FtpManagerRepository(object):
    def __init__(self, ftp_user, ftp_password):
        self.conn = self._start_ftp_connection(ftp_user, ftp_password)

    def _start_ftp_connection(self, ftp_user, ftp_password):
        self.url='10.0.5.2'
        self.conn = FTP(self.url, user=ftp_user, passwd=ftp_password)
        return self.conn

    def get_dir_details(self,path):
        # Connection must be open!
        try:
            print(path)
            self.conn.cwd(path)
            pwd = self.conn.pwd()
            lines = []
            self.conn.retrlines('LIST ' + pwd, lines.append)
            dirs = {}
            files = {}
            for line in lines:
                words = line.split()
                if len(words) < 6:
                    continue
                if words[-2] == '->':
                    continue
                if words[0][0] == 'd':
                    dirs[words[-1]] = 0
                elif words[0][0] == '-':
                    files[words[-1]] = int(words[-5])
            return dirs, files, pwd
        except all_errors:
            print('error')

    def upload_file(self, pwd, file_name, file_content):
        self.conn.cwd(pwd)
        self.conn.storbinary('STOR ' + os.path.basename(file_name),
                                file_content)


class ManageFTPUser(object):
    def __init__(self):
        self.conn = self._initialize_ftp_db_connection()

    def _initialize_ftp_db_connection(self):
        if not hasattr(self, 'conn'):
            return psycopg2.connect(dbname='proftp',
                                    host='10.0.5.2',
                                    user='proftp_user',
                                    password='usuario')
        return self.conn

    def _make_user_relations(self, app_user, ftp_user):
        AppUserFtpUserRelation.objects.create(app_user=app_user, ftp_user=ftp_user)


    def _get_last_ftp_user_uid(self):
        cur = self.conn.cursor()
        cur.execute("select uid from ftpuser order by uid desc;")
        lastuid = cur.fetchone()[0]
        cur.close()
        return int(lastuid)

    # def _create_ftp_dir_for_user(self, app_user):
    #     basedir = '/srv/hosting/'
    #     ftp_dir = basedir + app_user
    #     os.mkdir(ftp_dir)
    #     os.chown(ftp_dir, self.ftp_user_uid, 2000)
    #     print("Directorio creado")
    #     return ftp_dir

    def create_ftp_user_for_app_user(self, app_user, ftp_user, ftp_password):
        self._make_user_relations(app_user, ftp_user)
        ftp_user_uid = self._get_last_ftp_user_uid() + 1;
        # ftp_user_workdir = self._create_ftp_dir_for_user(app_user)
        basedir = '/srv/hosting/'
        ftp_user_workdir = basedir + app_user
        cur = self.conn.cursor()
        cur.execute("""insert into ftpuser values
                    ('{}','{}', {}, 2000,
                    '{}','/bin/bash');
                """.format(ftp_user, ftp_password, ftp_user_uid, ftp_user_workdir))
        self.conn.commit()
        cur.close()
        self.conn.close()

def get_ftp_user_for_app_user(user):
    try:
        user_data = AppUserFtpUserRelation.objects.get(app_user=user)
        ftp_user = user_data.ftp_user
        return ftp_user
    except:
        return ""
