from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index, name='web:index'),
    path("auth", views.auth, name="web:auth"),
    path("profile", views.profile, name="web:profile"),
]

handler404 = 'web.views.handler404'