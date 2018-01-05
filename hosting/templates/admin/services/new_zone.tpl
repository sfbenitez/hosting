$TTL	86400
@	IN	SOA	pandora.hosting4all.org. root.hosting4all.org. (
	1				; serial
	21600		; Refresh (6 hours)
	3600		; Retry (1 hour)
	604800	; Expire (1 week)
	21600 )	; Negative Cache TTL (6 hours)

	NS	pandora.hosting4all.org.
	MX  10  pandora.hosting4all.org.

$ORIGIN {{domain}}.
pandora	IN A 10.0.5.2
www	IN CNAME pandora
ftp IN CNAME pandora
postgresql IN CNAME pandora
