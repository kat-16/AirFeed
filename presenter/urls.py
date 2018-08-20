from django.conf.urls import url
from presenter import views

urlpatterns = [
	url(r'^$', views.dashboard, name='presenter_dashboard'),
]
