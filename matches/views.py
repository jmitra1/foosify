from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import Match

# Create your views here.
class CreateMatch(CreateView):
	model = Match
	fields = ["players"]
