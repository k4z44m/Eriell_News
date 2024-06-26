from blog.models import Category
from django import template

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()
