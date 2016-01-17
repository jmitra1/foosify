from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import Match

# Create your views here.
class CreateMatch(CreateView):
	model = Match
	fields = ["players"]

class MatchList(ListView):
	model = Match
