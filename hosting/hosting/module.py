# -*- coding: utf-8 -*-

from django_python3_ldap.utils import format_search_filters

def gidNumber_search_filters(ldap_fields):
    # Add in simple filters.
    ldap_fields["gidNumber"] = "2000"
    # Call the base format callable.
    search_filters = format_search_filters(ldap_fields)
    # Advanced: apply custom LDAP filter logic.
    # search_filters.append("(|(memberOf=groupA)(memberOf=GroupB))")
    # All done!
    return search_filters
