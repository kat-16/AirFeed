from django.contrib import admin

# Register your models here.
from .models import Event, QuestionType, Question, Choice

admin.site.register(Event)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuestionType)

