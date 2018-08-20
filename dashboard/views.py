from django.shortcuts import get_object_or_404, render
from event.models import Event, Question
from dashboard.forms import NewQuestionForm
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
# Create your views here.


# Create your questions here.
# def add_question(request, event_id):
#     """Add new question"""
#    new_question_form = NewQuestionForm()
#    return render(request, 'dashboard/dashboard.html', {})

@login_required
def view_dashboard(request, event_id):
    """dashboard for coordinator."""
    print("dashboardcall")
    new_question_form = NewQuestionForm()
    event = get_object_or_404(Event, pk=event_id)
    # add try catch part
    questions_list = event.question_set.all()
    return render(request, 'dashboard/dashboard.html', {'event_id': event_id, 'questions_list': questions_list ,'form': new_question_form})

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


@login_required
def visualisation_data(request, event_id):
    questions_queryset = Question.objects.filter(event_id=event_id )
    questions = {
    }
    for question in questions_queryset:
        questions[question.id] = model_to_dict(question)

    for i in questions.keys():
        question = questions[i]
        print(question)
        choices_queryset = Choice.objects.filter(question_id=question['id'])
        choices = [model_to_dict(choice) for choice in choices_queryset]
        questions[i]["choices"] = choices

    return JsonResponse(questions, safe=False)
