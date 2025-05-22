from django import template
from ..models import ReactionType

register = template.Library()

@register.simple_tag
def get_reaction_types():
    return ReactionType.objects.all()