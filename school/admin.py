from django.contrib import admin

# Register your models here.
 

from .models import  Cimage, Novel,Genre, Course , Tutor, Course_Description,Select_course,Profile,Feedback, Course_category
admin.site.register(Cimage)
admin.site.register(Select_course)
admin.site.register(Novel)
admin.site.register(Genre)
admin.site.register(Course)
admin.site.register(Course_Description)
admin.site.register(Profile)
admin.site.register(Feedback)
admin.site.register(Course_category)
admin.site.register(Tutor)