from django.urls import path
from robots.views import add_robots

urlpatterns = [
    path('add_robot/', add_robots, name='index'),
]