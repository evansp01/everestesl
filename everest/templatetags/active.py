from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def active(request, url, **kwargs):
    if request.path == reverse(url, kwargs=kwargs):
        return "active"
    return ""
