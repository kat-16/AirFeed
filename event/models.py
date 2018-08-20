from django.db import models
from fil_auth.models import CustomUser
import uuid
# Create your models here.

class Event(models.Model):
    """
    Events Model
    """
    id = models.CharField(primary_key=True, max_length=200, default=str(uuid.uuid4()), editable=False)
    event_name = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    duration = models.IntegerField()
    coordinator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    presenter = models.EmailField(default="admin@bhardefeedback.com")
    description = models.CharField(max_length=1000)


class QuestionType(models.Model):
    question_type = models.CharField(max_length=100)
    def __str__(self):
        return self.question_type


class Question(models.Model):
    question_text = models.CharField(max_length=500, null=False)
    event = models.ForeignKey(Event, null=False, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    is_mandatory = models.BooleanField(default=False)
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)


class Choice(models.Model):
    """There will be three type of choices->
    multi-select,single choice&rating corresponding to any question_id.
    """
    choice_text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
