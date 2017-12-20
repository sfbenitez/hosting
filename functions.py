import os
import psycopg2
import urllib, hashlib

def test_connection(sql_query, user, password):
 cur = None
 connstring = 'dbname=db_hosting host=172.22.200.116 user=%s password=%s' %(user, password)
 try:
  connect = psycopg2.connect(connstring)
  print sql_query
  try:
   cur = connect.cursor()
   cur.execute(sql_query)
   resultado = cur.fetchone()
  except:
   return false
  finally:
   if cur is not None:
    cur.close()
  return resultado
 except Exception, e:
  abort(401, "Sorry, acces denied.")


def selectall(sql_query, v_user, v_password):
 cur = None
 connstring = 'dbname=db_hosting host=172.22.200.116 user=%s password=%s' %(v_user, v_password)
 try:
  connect = psycopg2.connect(connstring)
  print sql_query
  try:
   cur = connect.cursor()
   cur.execute(sql_query)
   resultado = cur.fetchall()
  except:
   return false
  finally:
   if cur is not None:
    cur.close()
  return resultado
 except Exception, e:
  abort(400, "Sorry, bad request.")


def database_insert(sql_query, v_user, v_password):
 cur = None
 connstring = 'dbname=db_hosting host=172.22.200.116 user=%s password=%s' %(v_user, v_password)
 try:
  connect = psycopg2.connect(connstring)
  print sql_query
  try:
   cur = connect.cursor()
   cur.execute(sql_query)
   resultado = cur.statusmessage
   connect.commit()
  except Exception , e:
   print 'ERROR:', e[0]
   if cur is not None:
    connect.rollback()
  finally:
   if cur is not None:
    cur.close()
  return cur.statusmessage
 except Exception, e:
  print "Sorry, bad request."

def test_userexist(user):
 cur = None
 v_useradmin = 'admin'
 v_passwordadmin = 'usuario'
 v_hostdb = '172.22.200.116'
 v_db = 'db_hosting'
 connstring = 'dbname=%s host=%s user=%s password=%s' %(v_db, v_hostdb, v_useradmin, v_passwordadmin)
 sql_query = "SELECT user_user FROM users WHERE user_user = '%s'" %(user)
 try:
  connect = psycopg2.connect(connstring)
  print sql_query
  try:
   cur = connect.cursor()
   cur.execute(sql_query)
   resultado = cur.fetchone()
  except:
   return false
  finally:
   if cur is not None:
    cur.close()
  return resultado
 except Exception, e:
  abort(401, "Sorry, acces denied.")

def addnewuser(v_user, v_password, v_name, v_mail, v_date):
 newuser_createrole(v_user, v_password)
 newuser_insertuser(v_user, v_name, v_mail, v_date)
 setcoockie('s_user',v_user)
 setcoockie('s_password',v_password)
 setcoockie('s_name', v_name)

def newuser_createrole(v_user, v_password):
 cur = None
 v_useradmin = 'admin'
 v_passwordadmin = 'usuario'
 v_hostdb = '172.22.200.116'
 v_db = 'db_hosting'
 connstring = "dbname=%s host=%s user=%s password=%s" %(v_db, v_hostdb, v_useradmin, v_passwordadmin)
 createrole = "create role \"%s\" password '%s' login in role pupilgroup;" %(v_user, v_password)
 try:
  connect = psycopg2.connect(connstring)
  print createrole
  try:
   cur = connect.cursor()
   cur.execute(createrole)
   resultado = cur.statusmessage
   connect.commit()
  except Exception , e:
   print 'ERROR:', e[0]
   if cur is not None:
    connect.rollback()
  return cur.statusmessage
 except Exception, e:
  abort(400, "Sorry, bad request.")

def newuser_insertuser(v_user, v_name, v_mail, v_date ):
 cur = None
 v_useradmin = 'admin'
 v_passwordadmin = 'usuario'
 v_hostdb = '172.22.200.116'
 v_db = 'db_hosting'
 connstring = "dbname=%s host=%s user=%s password=%s" %(v_db, v_hostdb, v_useradmin, v_passwordadmin)
 adduser = "insert into users values ('%s', '%s', '%s', to_date('%s', 'DD/MM/YYYY'), '%s');" %(v_user, v_name, v_mail, v_date, '2')
 try:
  connect = psycopg2.connect(connstring)
  print adduser
  try:
   cur = connect.cursor()
   cur.execute(adduser)
   resultado = cur.statusmessage
   connect.commit()
  except Exception , e:
   print 'ERROR:', e[0]
   if cur is not None:
    connect.rollback()
  return cur.statusmessage
 except Exception, e:
  abort(400, "Sorry, bad request.")


def setcoockie(key, value):
 # session = environ['beaker.session']
 s = request.environ['beaker.session']
 s[key]=value

def getcoockie(key):
 s = request.environ['beaker.session']
 if key in s:
  return s[key]
 else:
  abort(401, "Sorry, acces denied.")

def deletecoockie():
 s = request.environ['beaker.session']
 s.delete()
