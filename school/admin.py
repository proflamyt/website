from django.contrib import admin
from .models import  *

# Register your models here.


admin.site.register(Topics)
admin.site.register(Course_Description)
admin.site.register(Profile)
admin.site.register(Tutor)
admin.site.register(Premium)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuizTakers)
admin.site.register(Answer)
admin.site.register(Response)
admin.site.register(User)