from __future__ import division
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save

# This is my player model. There are many like it, but this one is mine.
# It extends the main User class and adds trueskill and stats-related fields.
class Player(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	rating_mu = models.FloatField(default=25)
	rating_sigma = models.FloatField(default=8.33333)

	def get_wins(self):
		return self.matches.filter(winners=self)

	def win_rate(self):
		wins = self.get_wins().count()
		matches = self.matches.count()
		try:
			return round((wins / matches) * 100, 1)
		except ZeroDivisionError:
			return 0.0

	def __unicode__(self):
		return self.user.username

# Create a new player when a new User registers.
@receiver(post_save, sender=User)
def create_player(sender, **kwargs):
	instance = kwargs.get("instance")
	created = kwargs.get("created", False)
	if created:
		new_player = Player()
		new_player.user = instance
		new_player.save()

# Update your stats when a new Match is saved.
