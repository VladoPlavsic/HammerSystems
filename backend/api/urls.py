from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('/token/refresh', views.refresh_token, name='api:token_refresh'),
    path("/auth", views.auth, name="api:auth"),
    path("/verify", views.verify, name="api:verify"),
    path("/profile", views.profile, name="api:profile"),
    path("/add/friend", views.add_friend, name="api:add-friend")
]