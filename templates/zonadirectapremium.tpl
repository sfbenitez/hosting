$TTL	86400
@	IN	SOA	minnie.hosting4all.org. root.hosting4all.org. (
	1				; serial
	21600		; Refresh (6 hours)
	3600		; Retry (1 hour)
	604800	; Expire (1 week)
	21600 )	; Negative Cache TTL (6 hours)

	NS	minnie.hosting4all.org.
	MX  10  minnie.hosting4all.org.

$ORIGIN {{user}}.org
minnie	IN A 172.22.200.116
www	IN CNAME minnie
ftp IN CNAME minnie
postgresql IN CNAME minnie
