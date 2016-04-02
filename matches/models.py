from django.db import models
from django.contrib.auth.models import User
from players.models import Player
import datetime
import trueskill

# Create your models here.
class Match(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	end_date = models.DateTimeField(auto_now=True)
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

	def update_player_skill_values(self):
		""
		# winner1_rating = trueskill.Rating(winners[0].rating_mu, winners[0].rating_sigma)
		# match_rating_result = trueskill.rate([(winner1,winner2),(loser1,loser2)])
		# player.rating_mu = match_rating_result[0][0].mu
		# player.rating_sigma = match_rating_result[0][0].sigma

	def save(self, *args, **kwargs):
		# if winners exist (add this condition)...
		self.update_player_skill_values()
		super(Model, self).save(*args, **kwargs)

	class Meta:
		verbose_name_plural = "matches"
		ordering = ["-id"]

	def __unicode__(self):
		return unicode(self.id)
