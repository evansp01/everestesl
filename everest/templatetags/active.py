from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def active(request, url):
    print request.path
    print url
    if request.path ==  reverse(url):
        return "active"
    return ""
