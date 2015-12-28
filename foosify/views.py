from django import forms
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from matches.models import Match, MatchForm
from players.models import Player
from django.contrib.auth.models import User

@login_required
def index(request):
	# The main view for the app.
	matches = Match.objects.all()
	return render(request, "foosify/index.html", {"matches": matches})

@login_required
def player_profile(request,player_id):
	# A simple player profile.
	player = get_object_or_404(Player, pk=player_id)
	return render(request, "foosify/player.html", {"player": player})

@login_required
def new_match(request):
	# Form for creating a new match.
	if request.method == "POST":
		# Create the form object with the post data.
		form = MatchForm(request.POST)
		if form.is_valid():
			# If the form is valid, create a match with submitted data.
			match = Match()
			match.save()
			match.players = form.cleaned_data["players"]
			match.save()
			return redirect("index")
	else:
		form = MatchForm()
	return render(request, "foosify/match.html", {"form": form})
