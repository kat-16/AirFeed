from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from fil_auth.models import CustomUser
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
@login_required
def main_panel(request):
	user = request.user
	if user.is_superuser:
		ecoord_list = CustomUser.objects.all().filter(is_ecoord = True)
		return render(request, 'administrator/adminpanel.html', { 'ecoordlist' : ecoord_list})
