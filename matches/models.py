from django.contrib.auth.models import User
from django.db import models
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
		return ", ".join(self.players.values_list("user__username", flat=True))

	class Meta:
		verbose_name_plural = "matches"
		ordering = ["-id"]

	def __unicode__(self):
		return unicode(self.id)
