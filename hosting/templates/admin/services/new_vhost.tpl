<VirtualHost *:80>

	ServerName {{server_name}}
	ServerAdmin sergioferretebenitez@hosting4all.org
	DocumentRoot {{document_root}}
	<Directory {{document_root}}/>
        Require all granted
	</Directory>
  <Location /awstats/>
  	AuthName "Use your H4a username for access to web stats"
    AuthType Basic
    AuthBasicProvider ldap
    AuthLDAPURL "ldap://localhost/ou=People,dc=sergio,dc=gonzalonazareno,dc=org?uid?sub?(objectClass=*)"
    Require ldap-user {{app_user}}
  </Location>
  ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/{{server_name}}-access.log combined
</VirtualHost>
