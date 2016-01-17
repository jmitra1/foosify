from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from .models import Match

# Create your views here.
class CreateMatch(CreateView):
	model = Match
	fields = ["players"]

class UpdateMatch(UpdateView):
	model = Match
	fields = ["winners", "losers"]
	template_name_suffix = "_update_form"

class MatchList(ListView):
	model = Match
