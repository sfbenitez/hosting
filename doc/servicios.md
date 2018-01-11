# Configuración de los servicios.

## PostgreSQL
-----------
### Instalación del servidor PostgreSQL
```
apt install postgresql
```
Debemos habilitar el acceso a PostgreSQL a través de un socket TCP. Para ello editamos el fichero de configuración /etc/postgresql/X.X/main/pg_hba.conf, y añadimos la siguiente linea.
```
host    all             all             10.0.5.2/24            md5
```
Creación del usuario y la base de datos que usará la aplicación.
```
CREATE ROLE admin PASSWORD 'password' LOGIN CREATEROLE CREATEDB;
CREATE DATABASE db_hosting OWNER admin;
```
Todos los usuarios de la aplicación utilizan un rol de PostgreSQL para ver las bases de datos de las cuales son propietarios.
```
CREATE ROLE viewdatabases;
GRANT SELECT ON pg_database TO viewdatabases;
GRANT SELECT ON pg_authid TO viewdatabases;
```



FTP
------------------------------------------------------
All ftp users will have as home base directory '/srv/hosting/'. We configure proftpd to use
PostgreSQL as auth backend.

We need the proftpd module for PostgreSQL.
```
apt install proftpd proftpd-mod-pgsql
```
Configuring DefaultRoot of ftp users and enabling pgsql module.

File /etc/proftpd/proftpd.conf
```
DefaultRoot ~%u
# Activating PostgreSQL Auth conf
Include /etc/proftpd/sql.conf
```
File /etc/proftpd/modules.conf, discoment this lines.
```
#Activating PG module
LoadModule mod_sql.c
LoadModule mod_sql_postgres.c
```
File /etc/proftpd/sql.conf, add the next configuration.
```
Configure the PostgreSQL Auth.
SQLBackend      postgres
# Connection info: dbname=proftp host=localhost user=proftp_user pass=usuario
SQLConnectInfo proftp@localhost proftp_user usuario
# Hashes soported
SQLAuthTypes Crypt Plaintext
# table=ftpuser, columns to search
SQLUserInfo ftpuser username passwd uid gid homedir shell
# table=ftpgroup, columns to search
SQLGroupInfo ftpgroup groupname gid member
# activating SQL backend
SQLEngine on
# Autenticate users and groups
SQLAuthenticate users groups

# Create Home on demand using a defined skel, this directory contain a html template.
CreateHome on skel /etc/proftpd/skel/hosting
```

The next step is create the database writed and the users and groups tables. With a PostgreSQL super user, create the new role and the database.

```
create role proftp_user password 'usuario' login;
create database proftp owner proftp_user;
```

Connect as proftp_user and create the users and groups tables
```
CREATE TABLE ftpgroup (
  groupname varchar(16) NOT NULL default '',
  gid integer NOT NULL default '2000' primary key,
  members varchar(16) NOT NULL default '');

CREATE TABLE ftpuser (
  username varchar(32) NOT NULL default '',
  passwd varchar(32) NOT NULL default '',
  uid smallint NOT NULL primary key,
  gid smallint NOT NULL default '2000' REFERENCES ftpgroup (gid),
  homedir varchar(255) NOT NULL default '',
  shell varchar(16) NOT NULL default '/sbin/nologin');
```

We need to configure a especific connection on PostgreSQL.
File /etc/postgresql/9.5/main/pg_hba.conf
```
# proftpd specific connection
host    all          all     127.0.0.1/32            md5
```

Quota tables

```
CREATE TABLE quotalimits (
  name VARCHAR(32) NOT NULL,
  quota_type VARCHAR(8) NOT NULL
    CHECK (quota_type IN ('user', 'group', 'class', 'all')),
  per_session BOOLEAN NOT NULL,
  limit_type VARCHAR(4) NOT NULL
    CHECK (limit_type IN ('soft', 'hard')),
  bytes_in_avail FLOAT NOT NULL,
  bytes_out_avail FLOAT NOT NULL,
  bytes_xfer_avail FLOAT NOT NULL,
  files_in_avail INT8 NOT NULL,
  files_out_avail INT8 NOT NULL,
  files_xfer_avail INT8 NOT NULL
  );
CREATE TABLE quotatallies (
  name VARCHAR(32) NOT NULL,
  quota_type VARCHAR(8) NOT NULL
    CHECK (quota_type IN ('user','group','class','all')),
  bytes_in_used FLOAT NOT NULL,
  bytes_out_used FLOAT NOT NULL,
  bytes_xfer_used FLOAT NOT NULL,
  files_in_used INT8 NOT NULL,
  files_out_used INT8 NOT NULL,
  files_xfer_used INT8 NOT NULL
  );
```
