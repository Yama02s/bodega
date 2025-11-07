from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='es_panol')
def es_panol(user):
    return user.groups.filter(name='Pañol').exists()

@register.filter(name='es_admin')
def es_admin(user):
    return user.groups.filter(name='Administrador').exists() or user.is_superuser