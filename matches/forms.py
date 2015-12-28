from django.forms import ModelForm
from .models import Match

# Make a basic ModelForm for creating new matches.
class MatchForm(ModelForm):
	class Meta:
		model = Match
		fields = ["players"]
