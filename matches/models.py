from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
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
		print "\n Skill updated! \n"
		# Get the winner rating objects and store them in a tuple.
		winner_ratings = []
		for winner in self.winners.all():
			winner_ratings.append(
				trueskill.Rating(winner.rating_mu, winner.rating_sigma)
			)
		winner_ratings = tuple(winner_ratings,)
		print winner_ratings

		# Get the loser rating objects and store them in a tuple.
		loser_ratings = []
		for loser in self.losers.all():
			loser_ratings.append(
				trueskill.Rating(loser.rating_mu, loser.rating_sigma)
			)
		loser_ratings = tuple(loser_ratings,)

		# Then get the new ratings from the match.
		match_rating_result = trueskill.rate([winner_ratings, loser_ratings])

		# Then update the winners and losers based on the returned ratings.
		i = 0
		for winner in self.winners.all():
			winner.rating_mu = match_rating_result[0][i].mu
			winner.rating_sigma = match_rating_result[0][i].sigma
			winner.save(update_fields=["rating_mu", "rating_sigma"])
			i += 1
		i = 0
		for loser in self.losers.all():
			loser.rating_mu = match_rating_result[1][i].mu
			loser.rating_sigma = match_rating_result[1][i].sigma
			loser.save(update_fields=["rating_mu", "rating_sigma"])
			i += 1

	def save(self, *args, **kwargs):
		# Check if self exists before attempting to update, so as to only update
		# skill values on the second save, and to have players to update.
		super(Match, self).save()
		if self.pk is not None and self.winners.count() > 0 and self.losers.count() > 0:
			self.update_player_skill_values()

	class Meta:
		verbose_name_plural = "matches"
		ordering = ["-id"]

	def __unicode__(self):
		return unicode(self.id)
