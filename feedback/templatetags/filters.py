from django import template

register = template.Library()


@register.simple_tag
def has_feedback(offering, user):
	return offering.has_feedback(user)
