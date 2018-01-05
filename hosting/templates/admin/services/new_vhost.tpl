<VirtualHost *:80>

	ServerName {{server_name}}
	ServerAdmin sergioferretebenitez@hosting4all.org
	DocumentRoot {{document_root}}

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/{{server_name}}-access.log combined

</VirtualHost>
