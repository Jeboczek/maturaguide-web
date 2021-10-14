from django.contrib import admin
from .models import *

admin.site.register(Question)
admin.site.register(Subject)
admin.site.register(QuestionCategory)
admin.site.register(Answer)
admin.site.register(Explanation)
admin.site.register(StudySource)
admin.site.register(Excercise)