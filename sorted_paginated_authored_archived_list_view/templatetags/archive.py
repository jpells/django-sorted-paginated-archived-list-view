from django import template
import datetime
from django.template import Library
from django.db.models import get_model
from django.template import resolve_variable

register = Library()

class ArchiveYearNode(template.Node):
    def __init__(self, model, date_field):
        self.model = get_model(*model.split('.'))
        self.date_field = date_field
    def render(self, context):
        context['archive_years'] = self.model.objects.all().dates(self.date_field,'year','DESC')
        return ''

class ArchiveMonthNode(template.Node):
    def __init__(self, model, date_field, year):
        self.model = get_model(*model.split('.'))
        self.date_field = date_field
        self.year = year
    def render(self, context):
        year = resolve_variable(self.year, context)
        context['archive_months'] = self.model.objects.filter(pub_date__year=year.year).dates(self.date_field,'month','DESC')
        return ''

def do_archive_years(parser, token):
    try:
        tag_name, model, date_field = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires two arguments" % token.contents.split()[0]
    return ArchiveYearNode(model, date_field)

def do_archive_months(parser, token):
    try:
        tag_name, model, date_field, year = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires three arguments" % token.contents.split()[0]
    return ArchiveMonthNode(model, date_field, year)

register.tag('archive_years', do_archive_years)
register.tag('archive_months', do_archive_months)
