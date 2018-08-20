from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

@login_required
def dashboard(request):
    """Dashboard for presenter."""
    pass
