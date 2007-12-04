from django.views.generic.list_detail import object_list
from django.http import Http404
import datetime, time

def sorted_paginated_authored_archived_list(request, model, base_url, username=None, sort_field=None, paginate_by=10, filter=None, extra_context=None, template_name=None, year=None, month=None, day=None):
    username = request.REQUEST.get('by', username)
    sort_field = request.REQUEST.get('sort_by', sort_field)
    paginate_by = request.REQUEST.get('paginate_by', paginate_by)
    by_url = ''
    sort_by_url = ''
    paginate_by_url = ''
    if hasattr(model, 'published_objects'):
        queryset = model.published_objects.all()
    else:
        queryset = model.objects.all()
    if filter:
        queryset = queryset.filter(**filter)
    if year != None:
        if month != None:
            if day != None:
                try:
                    date = datetime.date(*time.strptime(year+month+day, '%Y'+'%b'+'%d')[:3])
                except ValueError:
                    raise Http404
                base_url = base_url + year + "/" + month + "/" + day + "/"
                queryset = queryset.filter(pub_date__gte=datetime.datetime.combine(date, datetime.time.min)).filter(pub_date__lte=datetime.datetime.combine(date, datetime.time.max))
            else:
                try:
                    date = datetime.date(*time.strptime(year+month, '%Y'+'%b')[:3])
                except ValueError:
                    raise Http404
                first_day = date.replace(day=1)
                if first_day.month == 12:
                    last_day = first_day.replace(year=first_day.year + 1, month=1)
                else:
                    last_day = first_day.replace(month=first_day.month + 1)
                base_url = base_url + year + "/" + month + "/"
                queryset = queryset.filter(pub_date__gte=first_day).filter(pub_date__lte=last_day)
        else:
            base_url = base_url + year + "/"
            queryset = queryset.filter(pub_date__year=year)
    if username != None:
        by_url = "by=%s" % username
        queryset = queryset.filter(user__username=username)
    if sort_field != None:
        sort_by_url = "sort_by=%s" % sort_field
        queryset = queryset.order_by(sort_field)
    if paginate_by != 10:
        paginate_by_url = "paginate_by=%s" % paginate_by
    base_url = base_url + "?" + by_url + "&" + paginate_by_url
    sort_url = base_url + "&" + sort_by_url
    if extra_context:
        extra_context.update(dict(sort_field=sort_field, base_url=base_url, sort_url=sort_url))
    else:
        extra_context = dict(sort_field=sort_field, base_url=base_url, sort_url=sort_url)
    return object_list(request, queryset=queryset, paginate_by=int(paginate_by), extra_context=extra_context, template_name=template_name)
