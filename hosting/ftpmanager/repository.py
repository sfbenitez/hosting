# -*- coding: utf-8 -*-
import os
import uuid
from ftplib import FTP, all_errors
from hosting.models import AppUserFtpUserRelation
import psycopg2
from users.admins import conector


class FtpManagerRepository(object):
    def __init__(self, ftp_user, ftp_password):
        self.conn = conector.FTPConector._initialize_ftp_connection(ftp_user, ftp_password)

    def mk_rem_dirs(self, pwd, path):
        self.conn.cwd(pwd)
        path_splitted = path.split('/')
        for path_part in path_splitted:
            self.conn.mkd(path_part)
            self.conn.cwd(path_part)

        pwd = self.conn.pwd()
        return pwd

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

    def delete_file(self, pwd, file_name):
        self.conn.cwd(pwd)
        self.conn.delete(file_name)

class ManageFTPUser(object):
    def __init__(self):
        self.conn = conector.PGConector._initialize_ftp_db_connection()

    def _make_user_relations(self, app_user, ftp_user):
        AppUserFtpUserRelation.objects.create(app_user=app_user, ftp_user=ftp_user)

    def _get_last_ftp_user_uid(self):
        cur = self.conn.cursor()
        cur.execute("select uid from ftpuser order by uid desc;")
        lastuid = cur.fetchone()[0]
        cur.close()
        return int(lastuid)

    def _create_quota_for_ftp_user(self, ftp_user, is_premium):
        if is_premium == False:
            #common user quota limit
            ftp_quota = 50728640 # 50MB
        else:
            #premium user quota limit
            ftp_quota = 300728640 # 300MB
        cur = self.conn.cursor()
        cur.execute("""insert into quotalimits values('{}', 'user','t', 'hard', {},0,0,0,0,0);""".format(ftp_user, ftp_quota))
        self.conn.commit()
        cur.close()

    def create_ftp_user_for_app_user(self, app_user, ftp_user, ftp_password, is_premium):
        self._make_user_relations(app_user, ftp_user)
        self._create_quota_for_ftp_user(ftp_user, is_premium)
        ftp_user_uid = self._get_last_ftp_user_uid() + 1;
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

    def get_quota_used(self, ftp_user):
        cur = self.conn.cursor()
        cur.execute("""select l.bytes_in_avail, u.bytes_in_used from quotalimits l join quotatallies u on l.name = u.name where l.name = '{}'""".format(ftp_user))
        quota_used = cur.fetchone()
        cur.close()
        self.conn.close()
        return quota_used

# class FTP_user_password():
#
#     def __init__(self, username, password):
#         self.username = username
#         self.pw_hash = sha256_crypt.encrypt(password)
#
#     def verify(self, password):
#         return sha256_crypt.verify(password, self.pw_hash)

def get_ftp_user_for_app_user(user):
    try:
        user_data = AppUserFtpUserRelation.objects.get(app_user=user)
        ftp_user = user_data.ftp_user
        return ftp_user
    except:
        return ""
