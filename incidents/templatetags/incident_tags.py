from django import template
from incidents.taxonomy import HARM_CATEGORIES

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def get_harm_categories(harm_type=None):
    if harm_type:
        return [(k, v) for k, v, t in HARM_CATEGORIES if t == harm_type]
    return [(k, v) for k, v, t in HARM_CATEGORIES]


@register.filter
def harm_type(category_key):
    """Returns the harm type (psychological/tangible/other) for a given category key."""
    for k, v, t in HARM_CATEGORIES:
        if k == category_key:
            return t
    return "other"
