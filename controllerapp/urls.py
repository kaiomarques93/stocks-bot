from django.urls import path
from . import views

urlpatterns = [
    path('run_bot/', views.run_bot, name='run_bot'),
    path('hello/', views.say_hello, name='hello world'),
]
