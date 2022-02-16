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
