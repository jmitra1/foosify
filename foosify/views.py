from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from matches.models import Match

@login_required
def index(request):
	# The main view for the app.
	matches = Match.objects.all()
	return render(request, "foosify/index.html", {"matches": matches})
