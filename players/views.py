from django.views.generic.detail import DetailView
from .models import Player

# Create your views here.
class PlayerDetail(DetailView):
	model = Player
