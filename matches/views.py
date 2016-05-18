from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse
from .models import Match

# Create your views here.
class CreateMatch(CreateView):
	model = Match
	fields = ["players"]
	def get_success_url(self):
		return reverse("match_lobby", args=(self.object.id,))

class UpdateMatch(UpdateView):
	model = Match
	fields = ["winners", "losers"]
	template_name_suffix = "_update_form"

class MatchList(ListView):
	model = Match
