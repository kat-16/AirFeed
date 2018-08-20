from django.urls import path, include
from administrator import views
from django.conf.urls import url
#import eventcoord

urlpatterns = [
	url(r'^$', views.main_panel, name='admin_main_panel'),
]
