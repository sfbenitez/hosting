# -*- coding: utf-8 -*-

from django_python3_ldap.utils import format_search_filters

def gidNumber_search_filters(ldap_fields):

    search_filters = format_search_filters(ldap_fields)
    # admin gid: 2001, common users gid = 2000
    search_filters.append("(|(gidNumber=2000)(gidNumber=2001))")

    return search_filters
