# Deployment process

Python 3 virtual environment
------------------------------------------------------
Create and initiate virtual environment
```
apt install virtualenv
virtualenv --python=/usr/bin/python3 /home/ubuntu/venv
source /home/ubuntu/venv
```
Get proyect and install requirements
```
apt install git
git clone https://github.com/juanmacobo/hosting4all.git
cd hosting4all/
pip install -r requirements.txt
```

PostgreSQL Backend
------------------------------------------------------
Configure database backend on **hosting/settings.py**
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

Apache2
------------------------------------------------------
Config WSGI module for the web application

Installing web server and wsgi-py3 version. We are using p3 virtualenv.
```
apt install apache2 libapache2-mod-wsgi-py3
```
