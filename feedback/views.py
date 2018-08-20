from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import get_token

from feedback.models import Room
from event.models import Event

def feedback(request, event_id):
    """Feedback page to receive feedback using WebSockets."""
    # Get a list of rooms, ordered alphabetically
    csrf = get_token(request)
    rooms = Room.objects.order_by("title")
    event = Event.objects.get(id=event_id)
    ctx_dict = {"rooms": rooms, "event":event , "csrf" : csrf}
    return render(request, "feedback/feedback.html", ctx_dict)
