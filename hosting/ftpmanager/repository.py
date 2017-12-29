import os
from django.db import models
from ftplib import FTP, all_errors


class FtpManagerRepository(object):
    def __init__(self, ftp_user, ftp_password):
        self.conn = self._start_ftp_connection(ftp_user, ftp_password)

    def _start_ftp_connection(self, ftp_user, ftp_password):
        self.url='10.0.5.2'
        self.conn = FTP(self.url, user=ftp_user, passwd=ftp_password)
        return self.conn

    def _get_dir_details(self,path):
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
