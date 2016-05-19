from __future__ import division
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify

# This is my player model. There are many like it, but this one is mine.
# It extends the main User class and adds trueskill and stats-related fields.
class Player(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	slug = models.SlugField(editable=False)
	rating_mu = models.FloatField(default=25)
	rating_sigma = models.FloatField(default=8.33333)

	def get_wins(self):
		wins = self.matches.filter(winners=self).count()
		if wins > 0:
			return wins
		else:
			return 0

	def get_losses(self):
		return self.matches.count() - self.get_wins().count()

	def win_rate(self):
		wins = self.get_wins().count()
		matches = self.matches.count()
		try:
			return round((wins / matches) * 100, 1)
		except ZeroDivisionError:
			return 0.0

	# Sets the slug to the username when you save the Player. Will break
	# if you change the User's username without saving the Player.
	def save(self, *args, **kwargs):
		self.slug = slugify(self.user.username)
		super(Player, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.user.username

# Create a new player when a new User registers.
@receiver(post_save, sender=User)
def create_player(sender, **kwargs):
	instance = kwargs.get("instance")
	created = kwargs.get("created", False)
	if created:
		new_player = Player()
	else:
		new_player = instance.player
	new_player.user = instance
	new_player.slug = slugify(instance.username)
	new_player.save()
