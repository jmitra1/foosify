"""foosify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from matches.views import CreateMatch, UpdateMatch, MatchList
from players.views import PlayerDetail

urlpatterns = [
	url(r"^$", MatchList.as_view()),
    url(r"^@(?P<slug>[-\w]+)", PlayerDetail.as_view()),
    url(r"^match/new", login_required(CreateMatch.as_view(success_url="/"))),
    url(r"^match/(?P<pk>\d+)", login_required(UpdateMatch.as_view(success_url="#"))),
    url(r"^accounts/", include("allauth.urls")),
    url(r"^admin", include(admin.site.urls)),
]
