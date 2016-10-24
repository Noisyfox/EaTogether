import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def courier_name(value):
    m = re.match(r"^cid_(?P<owner>.+?)_(?P<courier>.+)$", value)
    return m.group('courier')
