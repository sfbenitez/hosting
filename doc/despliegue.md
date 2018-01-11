# Despliegue del proyecto Django "hosting".

## Python 3 virtual environment
------------------------------------------------------
Al estar utilizando la última versión de Django (2.0), para el despliegue de la aplicación necesitamos un entorno virtual de Python 3.
Empezamos por crear el entorno virtual e inicializarlo.
```
apt install virtualenv
virtualenv --python=/usr/bin/python3 /home/ubuntu/venv
source /home/ubuntu/venv
```

Con el entorno virtual activado, podemos instalar los requisitos del proyecto.
```
apt install git
git clone https://github.com/juanmacobo/hosting4all.git
cd hosting4all/
pip install -r requirements.txt
```

## Configuración de las conexiones con los servidores.
------------------------------------------------------
### Conector.py

Todas las conexiones necesarias para la aplicación, de los servidores LDAP, FTP y PostgreSQL, las encontramos en el fichero [users.admins.conector](../hosting/users/admins/conector.py)

### Fichero Settings

#### Auth Backend

Para la autenticación de la aplicacón usamos como backend un servidor LDAP. Los datos necesarios para la autenticación están especificados en
el fichero [**hosting.settings**](../hosting/hosting/settings.py)
```
# LDAP conn string
LDAP_AUTH_URL = "ldap://172.22.200.127:389"
LDAP_AUTH_USE_TLS = False
# The LDAP search base for looking up users.
LDAP_AUTH_SEARCH_BASE = "ou=People,dc=sergio,dc=gonzalonazareno,dc=org"
# The LDAP class that represents a user.
LDAP_AUTH_OBJECT_CLASS = "inetOrgPerson"
# User model fields mapped to the LDAP
# attributes that represent them.
LDAP_AUTH_USER_FIELDS = {
    "username": "uid",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
    # "is_superuser": "gidNumber",
}
# A tuple of django model fields used to uniquely identify a user.
LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",)
```

## PostgreSQL Backend
------------------
Como base de datos principal, la aplicación utiliza una base de datos PostgreSQL, la configuración de conexión con este backend se encuentra en [**hosting/settings.py**](../hosting/hosting/settings.py)
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_hosting',
        'USER': 'admin',
        'PASSWORD': 'usuario',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Apache2
------------------------------------------------------
Actualmemte, la aplicación está desplegada en un servidor Apache2(v2.4). A continuación se muestra un ejemplo de configuración para un servidor virtual, usando el módulo wsgi para Python 3, de Apache.

### Directorios

Debemos localizar en que directorio hemos creado el entorno virtual, ya que debemos especificarlo en el fichero de configuración del servidor virtual. Además de decidir un directorio que utilizaremos como directorio raíz para dicho servidor virtual.

En este caso, hemos creado el entorno virtual en el directorio /home/ferrete/venv y hemos decidido usar como directorio raiz para la aplicación /var/www/hosting.

### Paquetes necesarios

Necesitaremos el servidor web y el módulo wsgi compatible con Python3.
```
apt install apache2 libapache2-mod-wsgi-py3
```
### Usuario específico para la aplicación
-------------------------------------
Nuestra aplicación utiliza herramientas del sistema que solo un usuario privilegiado podría utilizar, como recargar la configuración del servidor apache o la del servidor dns bind9. Por ello decidido crear un usuario específico para la aplicación (usuario: hosting), todos los procesos wsgi de nuestro proyecto se ejecutaran con ese usuario. Esta configuración la indicaremos en el servidor virtual.

Las tareas que debe realizar el usuario de la aplicación son las siguientes:
  * Recargar la configuración del servidor apache.
  * Activar servidores virtuales adicionales en el servidor apache.
  * Recargar la configuración del servidor de nombres BIND9.

Para asignar los privilegios que permitan al usuario "hosting", realizar las tareas anteriores, hemos utilizado sudo. Creamos los enlaces simbólicos de los binarios que utilizará el usuario hacia el directorio /usr/local/bin.
```
ln -s /usr/sbin/a2ensite /usr/local/bin/
ln -s /usr/sbin/apachectl /usr/local/bin/
ln -s /usr/sbin/rndc /usr/local/bin/
```
Hemos añadido al fichero sudoers del sistema las siguientes lineas.
```
hosting ALL = NOPASSWD: /usr/local/bin/apachectl graceful
hosting ALL = NOPASSWD: /usr/local/bin/rndc reload
hosting ALL = NOPASSWD: /usr/local/bin/a2ensite
```

Además de asignar privilegios sobre los binarios necesarios, será necesario otorgar privilegios de escritura en el directorio /etc/apache/sites-available. Para que la aplicación pueda crear los servidores virtuales de los usuarios. Esto podemos hacerlo de varias maneras, en este caso, decidimos asignar como grupo propietario de ese directorio, al grupo hosting, y otorgar privilegios de escritura a dicho grupo.

```
chown :hosting /etc/apache2/sites-available
chmod g+w /etc/apache2/sites-available
```
## BIND9
La aplicación crea nombres de dominio, solicitados por los usuarios de la aplicación. El servidor DNS que hemos usado es BIND9.

### Instalación
```
apt install bind9
```
### Privilegios del usuario "hosting"
Hemos creado el fichero /etc/bind/named.conf.hosting, en el cual añadiremos las nuevas zonas de dominio de los usuarios. Este fichero, lo incluiremos a la configuración de bind.

```
touch /etc/bind/named.conf.hosting
chown bind:hosting /etc/bind/named.conf.hosting
chmod 660 /etc/bind/named.conf.hosting
```
Lo añadimos a la configuración de Bind a través del fichero /etc/bind/named.conf.
```
include "/etc/bind/named.conf.options";
include "/etc/bind/named.conf.local";
include "/etc/bind/named.conf.default-zones";
include "/etc/bind/named.conf.hosting";
```
