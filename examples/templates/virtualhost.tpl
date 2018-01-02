<VirtualHost *:80>

	ServerName {{servername}}
	ServerAdmin webmaster@localhost
	DocumentRoot {{documentroot}}

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

</VirtualHost>
