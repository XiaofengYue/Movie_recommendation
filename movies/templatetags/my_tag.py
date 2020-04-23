from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def multi(x,y):
    return x*y

@register.simple_tag
def startag(a,b,c,d,e):
    if a+b+c+d+e != 0:
        return round((a*5+b*4+c*3+d*2+e)*2/(a+b+c+d+e),1)
    return 0

@register.simple_tag
def starround(a,b,c,d,e):
    if a+b+c+d+e != 0:
        return "rating" + str(round((a*5+b*4+c*3+d*2+e)/(a+b+c+d+e))) + "-t"
    return "rating0-t"