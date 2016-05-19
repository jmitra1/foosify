from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
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
		return string

	def update_player_skill_values(self):
		winner_ratings = []
		for winner in self.winners.all():
			winner_ratings.append(
				trueskill.Rating(winner.rating_mu, winner.rating_sigma)
			)
		winner_ratings = tuple(winner_ratings)

		loser_ratings = []
		for loser in self.losers.all():
			loser_ratings.append(
				trueskill.Rating(loser.rating_mu, loser.rating_sigma)
			)
		loser_ratings = tuple(loser_ratings)

		match_rating_result = trueskill.rate([winner_ratings, loser_ratings])

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

	class Meta:
		verbose_name_plural = "matches"
		ordering = ["-id"]

	def __unicode__(self):
		return unicode(self.id)

@receiver(m2m_changed)
def update_rankings_on_m2m_change(sender, instance, action, **kwargs):
	# Calculating the ranking changes for each match requires the M2M
	# relationships to already be added, which occurs after save (even
	# post_save). This event will fire a few times: once when the site is first
	# created and the players selected, and twice on update (for winners and
	# losers). This will work when the match winners/losers are first selected,
	# however, if you edit a match this will double count the rating changes.
	print sender, instance, action
	if action == "post_add":
		if instance.winners.count() > 0 and instance.losers.count() > 0:
			instance.update_player_skill_values()
