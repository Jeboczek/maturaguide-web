from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Question)
admin.site.register(Subject)
admin.site.register(AnswerCategory)

# Answers
admin.site.register(AnswerAZ)
admin.site.register(AnswerAZWithContent)
admin.site.register(AnswerTrueFalse)
admin.site.register(AnswerWithContent)