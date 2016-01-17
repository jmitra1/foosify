from django.db import models
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

	def get_players(self):
		players = self.players.values()
		string = ""
		first = True
		for player in players:
			if first:
				first = False
			else:
				string += ", "
			string += "<a href='@" + player["slug"] + "'>"
			string += player["slug"]
			string += "</a>"

		#return ", ".join(self.players.values_list("user__username", flat=True))
		return string

	class Meta:
		verbose_name_plural = "matches"
		ordering = ["-id"]

	def __unicode__(self):
		return unicode(self.id)
