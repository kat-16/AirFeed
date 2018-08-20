from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Redirects respective user to their dashboard
@login_required
def auth_test(request):
    user = request.user
    if user.is_superuser:
        return HttpResponseRedirect(reverse('admin_main_panel'))
    if user.is_ecoord:
        return HttpResponseRedirect(reverse('coord_main_panel'))
    if user.is_presenter:
        return HttpResponseRedirect(reverse('presenter_dashboard'))
