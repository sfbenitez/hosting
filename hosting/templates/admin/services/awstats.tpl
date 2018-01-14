Include "/etc/awstats/awstats.conf"

LogFile="{{logfile}}"
LogFormat=1
SiteDomain="{{server_name}}"
HostAliases="{{server_name}}"
LoadPlugin="tooltips"
LoadPlugin="graphgooglechartapi"
