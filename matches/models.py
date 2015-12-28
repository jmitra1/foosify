from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from players.models import Player
import datetime

# Create your models here.
class Match(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	players = models.ManyToManyField(Player, related_name="matches")
	winners = models.ManyToManyField(Player, related_name="match_winners")
	losers = models.ManyToManyField(Player, related_name="match_losers")
	# quality = models.IntegerField()

	def get_player_names(self):
		player_name_list = []
		for player in self.players.all():
			player_name_list.append(player.user.username)
		return ", ".join(player_name_list)

	class Meta:
		verbose_name_plural = "matches"
		ordering = ["-id"]

	def __unicode__(self):
		return unicode(self.id)

# Make a basic ModelForm for creating new matches.
class MatchForm(ModelForm):
	class Meta:
		model = Match
		fields = ["players"]
