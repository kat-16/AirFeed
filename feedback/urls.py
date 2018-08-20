from django.urls import path
from feedback import views
#import eventcoord
urlpatterns = [
	path('<slug:event_id>', views.feedback, name='receive_feedback'),
]
