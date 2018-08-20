from django import forms
from django.forms import ModelForm
from event.models import Event, QuestionType

class EventForm(forms.Form):
	event_name = forms.CharField(max_length=200)
	date_event = forms.DateTimeField()
	duration = forms.IntegerField()
	presenter = forms.EmailField()
	description = forms.CharField(widget=forms.Textarea)

class NewQuestionForm(forms.Form):
	question_text = forms.CharField(max_length=200)
	is_active = forms.BooleanField(widget=forms.CheckboxInput, required=False)
	is_mandatory = forms.BooleanField(widget=forms.CheckboxInput, required=False)
	question_type = forms.ModelChoiceField(queryset = QuestionType.objects.all())
