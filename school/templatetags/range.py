from xml.dom import registerDOMImplementation
from django import template

register = template.Library()
@register.filter(name='times')
def times(number):
	return range(1, number+1)


@register.filter(name='zip')
def zip_list(a,b):
	c = []
	for i in b:
		c.append(i.course_name.sel)
	return zip(a,c)

@register.filter(name='per')
def percentage(a,b):
	return int(a/b*100)

@register.filter(name='has_object')
def check(user, object):
	print(user)
	return user.registered_courses.filter(id=object).exists()
