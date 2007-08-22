from django import template

register = template.Library()

class PaginateBy:
    def __init__(self, number, display_page):
	self.number = number 
	self.display_page = display_page

def paginateby(context, interval=10, displayed=10):
    paginate_by = []
    for i in range(1, displayed+1):
    	number = i * interval
    	display_page = True
        if context["hits"] < (number * (context["page"] - 1)):
            display_page = False
        paginate_by.append(PaginateBy(number, display_page))
    return {
        "page": context["page"],
	    "paginate_by": paginate_by,
    	"link_url": context["sort_url"],
    }

register.inclusion_tag("sorted_paginated_authored_archived_list_view/paginateby.html", takes_context=True)(paginateby)
