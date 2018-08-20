from event.models import Event, Question, Choice
import json
from django.forms.models import model_to_dict



def active_questions_json(event_id):
    active_questions_queryset = Question.objects.filter(is_active=True, event_id=event_id )
    active_questions = [model_to_dict(question) for question in active_questions_queryset]
    for i in range(len(active_questions)):
        question = active_questions[i]
        choices_queryset = Choice.objects.filter(question_id=question['id'])
        choices = [model_to_dict(choice) for choice in choices_queryset]
        active_questions[i]["choices"] = choices

    # print(active_questions)
    return active_questions
