from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Player

# Create your views here.
@login_required
def profile(request,player_id):
	# A simple player profile.
	player = get_object_or_404(Player, pk=player_id)
	return render(request, "profile.html", {"player": player})
