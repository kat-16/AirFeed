from django.urls import path
from django.conf.urls import url
from event import views as event_views
from dashboard import views as dashboard_views

urlpatterns = [
	url(r'^create/$', event_views.create_event, name='create_event'),
	path('<str:event_id>/edit/', event_views.edit_event, name='edit_event'),
	path('<str:event_id>/details/', event_views.view_event, name='view_event'),
	path('<str:event_id>/qr/',event_views.show_event_qr, name='view_event_qr'),
	path('<str:event_id>/dashboard/',dashboard_views.view_dashboard, name='view_dashboard'),
	path('<str:event_id>/dashboard/questions/',dashboard_views.visualisation_data, name='get_visualisation_data'),
	path('<str:event_id>/dashboard/addquestion/',event_views.add_question, name='add_question'),
	path('toggleactive/<str:question_id>/',event_views.toggle_status, name='toggle_status'),
	url(r'^question/vote/$',event_views.update_vote_count, name='update_vote_count'),
]
