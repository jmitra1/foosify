from django.http import Http404
from django.shortcuts import render
from .models import Player

# Create your views here.
def profile(request,username):
	# A simple player profile.
	# player = get_object_or_404(Player, pk=player_id)
	try:
		player = Player.objects.filter(user__username=username).get()
	except Player.DoesNotExist:
		raise Http404("Player '" + username + "' does not exist.")
	return render(request, "players/profile.html", {"player": player})
