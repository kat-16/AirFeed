from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from event.models import Event, Question, QuestionType,Choice
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from event.forms import EventForm, NewQuestionForm
from dashboard.views import view_dashboard
from feedback.models import Room
import uuid
import json
from django.http import JsonResponse
from event.utils import active_questions_json
from feedback.utils import get_room_or_error
from registration.backends.default.views import RegistrationView
# Create your views here.


@user_passes_test(lambda u: u.is_ecoord)
@login_required
def create_event(request):
    """Create a new event."""
    new_event_form = EventForm()
    if request.method == 'POST':
        response_new_event_form = EventForm(request.POST)
        if response_new_event_form.is_valid():
            # print(response_new_event_form.cleaned_data)
            presenter = response_new_event_form.cleaned_data['presenter']
            event_name = response_new_event_form.cleaned_data['event_name']
            date_event = response_new_event_form.cleaned_data['date_event']
            duration = response_new_event_form.cleaned_data['duration']
            coordinator = request.user
            description = response_new_event_form.cleaned_data['description']
            event = Event.objects.create(event_name=event_name, timestamp=date_event,
                                 duration=duration, presenter=presenter, coordinator=coordinator, description=description)

            Room.objects.create(title = event.id)
            request.POST = request.POST.copy()
            # print(request.POST)
            print(request.user.idf)
            request.POST["email"] = presenter
            request.POST["password1"] = request.user.idf
            request.POST["password2"] = request.user.idf
            return RegistrationView.as_view()(request)
            # return HttpResponseRedirect(reverse('coord_main_panel'))

        else:
            error_message='Please fill the details again'
            return render(request, 'event/new_event_form.html', {'form': new_event_form})

    return render(request, 'event/new_event_form.html', {'form': new_event_form})


@user_passes_test(lambda u: u.is_ecoord)
@login_required
def edit_event(request, event_id):
    """Edit event."""
    event_details = Event.objects.get(pk=event_id)
    event_data = {	'event_name': event_details.event_name,
                   'date_event': event_details.timestamp,
                   'duration': event_details.duration,
                   'description': event_details.description}
    descriptionfield = event_details.description

    populated_form = EventForm(event_data, initial=event_data)

    if request.method == 'POST':
        changed_event_details = EventForm(request.POST)
        if changed_event_details.is_valid():
            event_name = changed_event_details.cleaned_data['event_name']
            date_event = changed_event_details.cleaned_data['date_event']
            duration = changed_event_details.cleaned_data['duration']
            coordinator = request.user
            description = changed_event_details.cleaned_data['description']
            Event.objects.filter(pk=event_id).update(event_name=event_name, timestamp=date_event,
                                                     duration=duration, coordinator=coordinator, description=description)
            print("saved event")
            return HttpResponseRedirect(reverse('coord_main_panel'))

    return render(request, 'event/edit_event.html', {'form': populated_form})


@login_required
def view_event(request, event_id):
    """View event details."""
    pass


@login_required
def show_event_qr(request, event_id):
    """View Qr code for event."""

    event = Event.objects.get(pk=event_id)
    return render(request, 'event/qr.html', {'event': event})


@login_required
def view_dashboard(request, event_id):
    print("eventcall")
    questions_list = Event.question_set.get(pk=event_id)
    print(questions_list)
    return HttpResponseRedirect(reverse('view_dashboard', kwargs={'questions_list': questions_list}))


@user_passes_test(lambda u: u.is_ecoord)
@login_required
def add_question(request, event_id):
    print("working****************************************************************************************************")
    if request.method == 'POST' and request.is_ajax():
        question_type = request.POST.get('question_type')
        question_type_name = QuestionType.objects.get(pk=question_type)
        question_text = request.POST.get('question_name')
        is_active = request.POST.get('is_active')
        is_mandatory = request.POST.get('is_mandatory')
        choice_list = request.POST.get('choice_list')
        if len(choice_list) == 0:
            return JsonResponse({'status':'Error','message':"Sale dhang se bharle."}, status=500)
        choice_list = json.loads(choice_list)
        question = Question.objects.create(question_text=question_text, event_id=event_id, is_active=is_active, is_mandatory=is_mandatory,
            question_type=question_type_name)

        for each in choice_list:
            choice = Choice(choice_text=each, question= question)
            choice.save()
        return HttpResponseRedirect(reverse('view_dashboard', kwargs={"event_id":event_id}))
    else:
        new_question_form = NewQuestionForm()
        return render(request, 'event/addquestion.html', {'form': new_question_form})

@login_required
def toggle_status(request, question_id):
    print("toggle")
    print(request.method)
    if request.method == 'POST' and request.is_ajax():
        print("accesd")
        print(question_id)
        try:
            question = Question.objects.get(pk=question_id)
            if question.is_active:
                Question.objects.filter(pk=question_id).update(is_active=False)
            else:
                Question.objects.filter(pk=question_id).update(is_active=True)

            ## Send new questions to users using websockets
            room = get_room_or_error(question.event_id, request.user)
            print(room)
            print(active_questions_json(question.event_id))
            room.send_message(active_questions_json(question.event_id), request.user, 0)

            return JsonResponse({'status': 'Success', 'msg': 'save successfully'})
        except Question.DoesNotExist:
            return JsonResponse({'status':'Error','message':"Sale dhang se bharle."}, status=500)
    else:
        return JsonResponse({'status':'Error','message':"Sale dhang se bharle."}, status=500)


def update_vote_count(request):
    if request.method=='POST' and request.is_ajax():
        choice_list = json.loads(request.POST.get('choice_list'))
        if len(choice_list) == 0:
            return JsonResponse({'status':'Error','message':"Sale dhang se bharle."}, status=500)
        for choice in choice_list:
            selected_choice = Choice.objects.get(pk=int(choice))
            selected_choice.vote_count+=1
            selected_choice.save()
        return JsonResponse({'status': 'Success', 'msg': 'voted successfully'})
