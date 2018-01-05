<VirtualHost *:80>

	ServerName {{servername}}
	ServerAdmin sergioferretebenitez@hosting4all.org
	DocumentRoot {{documentroot}}

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/{{servername}}-access.log combined

</VirtualHost>
