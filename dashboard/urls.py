from django.conf.urls import url
from dashboard import views
#import eventcoord
from django.urls import path

app_name = 'dashboard'
urlpatterns = [
	url(r'^$', views.view_dashboard, name='view_dashboard'),
]
