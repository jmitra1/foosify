from django import forms
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Match
from .forms import MatchForm

# Create your views here.
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
	return render(request, "match.html", {"form": form})
