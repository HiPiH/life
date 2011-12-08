from django import template
register = template.Library()

def reprobject(val):
    return repr(val)

def dirobject(val):
    return dir(val)

register.filter('repr', reprobject)
register.filter('dir', dirobject)