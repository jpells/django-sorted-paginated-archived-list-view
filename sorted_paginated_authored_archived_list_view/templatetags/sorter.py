from django import template
import string

register = template.Library()

def sorter(context, field_name='', link_name=''):
    sort_field = context["sort_field"]
    ascending = False
    descending = False
    if sort_field:
        if string.find(sort_field, field_name) >= 0:
            if sort_field[0] == '-':
                descending = True
            else:
                ascending = True
    return {
        "field_name": field_name,
        "link_name": link_name,
        "link_url": context["base_url"],
        "ascending": ascending,
        "descending": descending,
        "MEDIA_URL": context["MEDIA_URL"],
        "page": context["page"]
    }

register.inclusion_tag("sorted_paginated_authored_archived_list_view/sorter.html", takes_context=True)(sorter)
