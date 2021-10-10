from django.contrib import admin
from .models import *

admin.site.register(Question)
admin.site.register(Subject)
admin.site.register(QuestionCategory)
admin.site.register(QuestionTag)
admin.site.register(Explanation)

# Answers
admin.site.register(AnswerAZ)
admin.site.register(AnswerAZWithContent)
admin.site.register(AnswerTrueFalse)
admin.site.register(AnswerWithContent)