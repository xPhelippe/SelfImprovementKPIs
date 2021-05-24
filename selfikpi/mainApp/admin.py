from django.contrib import admin
from .models import Person, Question, Survey, TextResponse, QuestionAnswer

# Register your models here.


admin.site.register(Person)
admin.site.register(Question)
admin.site.register(Survey)
admin.site.register(TextResponse)
admin.site.register(QuestionAnswer)