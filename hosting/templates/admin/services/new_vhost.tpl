<VirtualHost *:80>

	ServerName {{server_name}}
	ServerAdmin sergioferretebenitez@hosting4all.org
	DocumentRoot {{document_root}}
	<Directory {{document_root}}/>
        Require all granted
	</Directory>
	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/{{server_name}}-access.log combined

</VirtualHost>
